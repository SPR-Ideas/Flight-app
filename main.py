from fastapi import FastAPI , Request
from database import models
from database.database import engine
from router.account import user_app , manager
from fastapi.staticfiles import StaticFiles
from router.admin import url_route_admin ,manager_admin
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
import uvicorn




SECRET = "f98e623de44d967238ee8dedc886860b65683b9ba0ce6efd"


models.Base.metadata.create_all(bind=engine)

# creating an instance of fastapi.
app = FastAPI()


class NotAuthenticatedException(Exception):
    """ Creating an custom exception classs. """
    pass

class NotAuthenticatedAdminException(Exception):
    """ Creating an custom exception classs. """
    pass


# Adding the routes to main routes.
app.include_router(user_app)
app.include_router(url_route_admin)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


app.mount("/static", StaticFiles(directory="static"), name="static")



manager.not_authenticated_exception = NotAuthenticatedException
manager_admin.not_authenticated_exception = NotAuthenticatedAdminException

@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    """
    Redirect the user to the login page if not logged in
    """
    return RedirectResponse(url='/login')


@app.exception_handler(NotAuthenticatedAdminException)
def auth_exception_handler_adim(request: Request, exc: NotAuthenticatedException):
    """
    Redirect the user to the login page if not logged in
    """
    return RedirectResponse(url='/admin-login')



if __name__ == "__main__":
    uvicorn.run(app)
