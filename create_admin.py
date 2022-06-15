from getpass import getpass

from database.database import SessionLocal
from database.models import admin
from router.account import get_hash_pwd

def admin_exist(admin_id):
    """
        Checks weather the user already exists.
    """
    session = SessionLocal()
    admin_obj = session.query(admin).filter(admin.admin_id == admin_id).first()
    if admin_obj:
        return True
    return False


def create_admin():
    """
        Creates an admin account for the website.
    """
    print("===============================================")
    print("\n Create a new AdminID (only in numbers)\n eg :1234")
    admin_id = input("Enter AdminId : ")
    passwd = getpass()
    confirm = getpass("Confirm : ")

    if passwd != confirm :
        print("password miss-match")
        return ""

    if admin_exist(admin_id):
        print("Admin Id already exist")
        return ""

    hash_pwd = get_hash_pwd(passwd)
    admin_obj = admin(admin_id = admin_id,password =hash_pwd)

    session = SessionLocal()
    session.add(admin_obj)
    session.commit()
    session.close()
    return ''


if __name__ == "__main__":
    create_admin()
