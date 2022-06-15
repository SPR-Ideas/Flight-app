
from enum import unique
from .database import Base  ,SessionLocal
from sqlalchemy import Column , Integer, String, Float

#create databasetabel by inheriting Base class

class user(Base):
    """
        User profile database.
    """
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True)
    username = Column(String,unique= True)
    name = Column(String)
    password = Column(String)
    location = Column(String)


class admin(Base):

    """Admin profile database."""
    __tablename__ = "admin"

    id = Column(Integer,primary_key=True)
    admin_id = Column(String,unique=True)
    password = Column(String)


class flight(Base):
    """Flight data base"""

    __tablename__ = "Flight"
    id = Column(Integer,primary_key = True)
    flight_Name = Column(String,unique=True)
    seat = Column(Integer)
    time = Column(String)
    from_place = Column(String)
    to_place = Column(String)



def get_all_user():
    """from sqlalchemy.orm import session
        It gets the all the user instance.
    """
    session = SessionLocal()
    user_objects = session.query(user).all()
    return user_objects
