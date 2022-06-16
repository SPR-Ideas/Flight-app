from fastapi import APIRouter , Request
from datetime import timedelta
from fastapi.templating import Jinja2Templates
from sqlalchemy import Column
from starlette.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from fastapi_login import LoginManager
from passlib.context import CryptContext
from database.database import SessionLocal
from database.models import flight, user ,booked_form
from fastapi_login.exceptions import InvalidCredentialsException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse ,JSONResponse ,RedirectResponse


user_app = APIRouter()
templates = Jinja2Templates(directory="templates")

SECRET = "f98e623de44d967238ee8dedc886860b65683b9ba0ce6efd"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
manager = LoginManager(SECRET, '/token' ,use_cookie=True ,use_header=True)


def get_hash_pwd(passwd):
    """Returns hased pwd."""
    return pwd_context.hash(passwd)


class UserPd(BaseModel):
    """ It is a pydantic model of user instance"""
    username : str
    name : str
    password : str
    location : str

class Flight_Pd(BaseModel):
    flight_name : str
    seat : int
    time : str
    from_place : str
    to_place : str

class BookTicketPd(BaseModel):
    flight_id :int
    user_id : int


@user_app.post("/login_user")
async def login_user(response: Response, data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password

    user_instance = query_user(username)

    if not user_instance:
        raise InvalidCredentialsException

    matches_passwd = pwd_context.verify(password,user_instance.password)

    if not matches_passwd:
        # If password matches raises Invalid credentials.
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data={'sub': username},
        expires = timedelta(hours = 12)
    )

    # It set the Token in cookies for the user.
    manager.set_cookie(response, access_token)
    return {'token': access_token}


@manager.user_loader
def query_user(username: str):
    """
    Get a user from the db
    :param user_id: E-Mail of the user
    :return: None or the user object
    """
    session = SessionLocal()
    user_object = session.query(user).filter(user.username == username).first()

    if user_object:
        return user_object
    return None


def create_user(user_instance):
    """It creat an user in db."""
    session = SessionLocal()
    hash_pwd = get_hash_pwd(user_instance.password)
    user_object = user(
        username = user_instance.username,
        name = user_instance.name ,
        password = hash_pwd,
        location = user_instance.location
    )
    session.add(user_object)
    session.commit()
    session.close()


@user_app.post("/create-user")
def create_user_by_route(user_instance : UserPd ):
    """It just creats an user and gives us status."""
    session = SessionLocal()
    username = user_instance.username
    exisiting_user = session.query(user).filter(user.username == username).first()
    if exisiting_user :
        return JSONResponse(status_code=401, content={
                "error":"1",            # Should be changed by exception.
                "msg":"username exist."
            } )

    create_user(user_instance)
    return JSONResponse(status_code=200,content= {
        "error" : "0",
        "msg" : "Success"
    }   )



@user_app.get("/login")
def login(request : Request):
        return templates.TemplateResponse(
        "login.html",{"request":request}
    )
    # return "HI"

@user_app.get("/register")
def login(request : Request):
        return templates.TemplateResponse(
        "register.html",{"request":request}
    )




@user_app.get('/logout', response_class=HTMLResponse)
def protected_route(request: Request,):
    resp = RedirectResponse(url="/login", status_code=302)
    manager.set_cookie(resp, "")
    return resp

def get_all_flights():
    session =  SessionLocal()
    flights_objects = session.query(flight).all()
    return flights_objects

def get_flight_by_id(flight_id):
    session =  SessionLocal()
    flights_object = session.query(flight).get(flight_id)
    return flights_object


def get_flights_booked_by_user(user_id):
    session = SessionLocal()
    booked_flights  = session.query(booked_form).filter(
    user_id == user_id
    ).all()
    l = []

    for i in booked_flights:
        if user_id == i.user_id:
            l.append(
            get_flight_by_id(i.flight_id)
        )

    return l


def get_flights_available_for_users(user_id):
    session = SessionLocal()
    all_flights = get_all_flights()
    flights_booked = get_flights_booked_by_user(user_id=user_id)
    temp = []
    for i in all_flights:
        if  i.id not in [k.id for k in flights_booked]:
            temp.append(i)
    return temp


@user_app.get("/",response_class=HTMLResponse)
def home(request:Request, user_instance = Depends(manager)):
    """
        Returns HomePage if user is autheticated,
        if not it redirect to login page.
    """


    return templates.TemplateResponse(
        "home.html",{
            "request":request,
            "user" : user_instance,
            "flights" : get_flights_available_for_users(user_instance.id),
            "flights_book" : get_flights_booked_by_user(user_instance.id)

        }
    )

def create_flight_instance(fl):
    session = SessionLocal()

    flight_object = flight(
        flight_Name = fl.flight_name,
        seat = fl.seat,
        time = fl.time,
        from_place = fl.from_place,
        to_place = fl.to_place
    )
    session.add(flight_object)
    session.commit()
    session.close()


def book_ticket_instance(flight_id, user_id):
    session = SessionLocal()
    ticket = booked_form(
        user_id = user_id,
        flight_id = flight_id
    )
    flight_obj = session.query(flight).get(flight_id)
    flight_obj.seat = flight_obj.seat -1
    session.add(flight_obj)
    session.add(ticket)

    session.commit()
    session.close()


# @user_app.post("/create-flight")
# def create_flight(flight_pd : Flight_Pd):
#     create_flight_instance(flight_pd)
#     return "Done"


@user_app.post("/book-ticket")
def book_ticket(book_ticket : BookTicketPd):
    """
        booking ticket
    """
    book_ticket_instance(book_ticket.flight_id,book_ticket.user_id)
    print("called")
    print(book_ticket.flight_id,book_ticket.user_id)
    return "done"



