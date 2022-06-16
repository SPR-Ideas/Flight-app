from multiprocessing.managers import BaseManager
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.routing import APIRouter
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from requests import session
from starlette.responses import JSONResponse , RedirectResponse
from pydantic import BaseModel

from database.models import admin, flight

from .account import (
    get_all_flights, templates,Request,
    HTMLResponse,SECRET,
    SessionLocal,Response,
    pwd_context ,timedelta,
    OAuth2PasswordRequestForm
    )


url_route_admin = APIRouter()
manager_admin = LoginManager(SECRET,"/admin-token",use_cookie=True,use_header=True)


class DeleteFlightPD(BaseModel):
    flight_id : int
    status : str




@url_route_admin.get('/admin-logout', response_class=HTMLResponse)
def protected_route(request: Request,):
    resp = RedirectResponse(url="/admin-login", status_code=302)
    manager_admin.set_cookie(resp, "")
    return resp




@url_route_admin.get("/admin-login",response_class=HTMLResponse )
def admin_login(request:Request):
    """
        It renders the admin login HTML page.
    """
    return templates.TemplateResponse(
        "admin-login.html",
        {
            "request": request
        }
    )


@url_route_admin.post('/admin-token')
def login( response: Response, data: OAuth2PasswordRequestForm = Depends()):
    """ It Checks the userdata form and give Oauth token."""
    admin_id= data.username
    password = data.password

    user = query_user(admin_id)
    if not user:
        # raise InvalidCredentials Exceptions.
        raise InvalidCredentialsException

    matches_passwd = pwd_context.verify(password,user.password)

    if not matches_passwd:
        # If password matches raises Invalid credentials.
        raise InvalidCredentialsException

    access_token = manager_admin.create_access_token(
        data={'sub': admin_id},
        expires = timedelta(hours = 12)
    )

    # It set the Token in cookies for the user.

    manager_admin.set_cookie(response, access_token)
    return {'token': access_token}



@manager_admin.user_loader
def query_user(admin_id: str):
    """
        Get a user from the db

    param user_id:
        E-Mail of the user
    return:
        None or the user object
    """
    session = SessionLocal()
    user_object = session.query(admin).filter(admin.admin_id == admin_id).first()

    if user_object:
        return user_object
    return None



def login( response: Response, data: OAuth2PasswordRequestForm = Depends()):
    """ It Checks the userdata form and give Oauth token."""
    admin_id= data.username
    password = data.password

    user = query_user(admin_id)
    if not user:
        # raise InvalidCredentials Exceptions.
        raise InvalidCredentialsException

    matches_passwd = pwd_context.verify(password,user.password)

    if not matches_passwd:
        # If password matches raises Invalid credentials.
        raise InvalidCredentialsException

    access_token = manager_admin.create_access_token(
        data={'sub': admin_id},
        expires = timedelta(hours = 12)
    ).decode()

    # It set the Token in cookies for the user.

    manager_admin.set_cookie(response, access_token)
    return {'token': access_token}



@url_route_admin.get("/admin-panel" , response_class=HTMLResponse)
def admin_panel( request : Request , admin_instance = Depends(manager_admin) ):
    " It renders the admin-panel HTML page."
    return templates.TemplateResponse(
        "admin.html",
        {
            "request" : request,
            "admin" : admin_instance,
            "flights":get_all_flights()

        }
    )


@url_route_admin.get('/admin-logout', response_class=HTMLResponse)
def protected_route(request: Request,):
    resp = RedirectResponse(url="/admin-login", status_code=302)
    manager_admin.set_cookie(resp, "")
    return resp

def delete_flight(id):
    session = SessionLocal()
    session.query(flight).filter(flight.id==id).delete()
    session.commit()
    session.close()

@url_route_admin.post("/delete-flight")
def delet_flight(DF : DeleteFlightPD):
    delete_flight(DF.flight_id)
    return "done"

class Flight_Pd(BaseModel):
    flight_name : str
    seat : int
    time : str
    from_place : str
    tplace : str

def create_flight_instance(fl):
    session = SessionLocal()

    flight_object = flight(
        flight_Name = fl["flight_name"],
        seat = fl["seat"],
        time = fl["time"],
        from_place = fl["from_place"],
        to_place = fl["to_place"]
    )
    session.add(flight_object)
    session.commit()
    session.close()

@url_route_admin.post("/create-flight",status_code=201)
async def create_flight(flight_pd : Request):
    a  = await flight_pd.json()
    print(a)
    create_flight_instance(a)

    return {
        "status_code":201
    }


