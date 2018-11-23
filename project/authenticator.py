from sqlalchemy import Column, Integer, String
from flask_login import LoginManager, login_user, current_user, login_required, logout_user, UserMixin
from server import login_manager
from base import Base, Session
import hashlib
from user import User, AnonUser

def set_password(id, password):
    #TODO: Maybe check if user is authenticated?
    session = Session()
    account = session.query(User).filter(User.id == id).first()
    if account == None:
        print("No account with id " + id)
        return False
    
    account.passwordhash = hashlib.sha512(password).hexdigest()
    session.commit()
    session.close()


def create_user(user_id, passwordhash, email):
    if storageSystem.user_exists(user_id):
        return 1                            # User Already Exists
    if storageSystem.email_exists(email):
        return 2                            # Email Already Exists                  
    return storageSystem.new_user(user_id, email, passwordhash)             # 3 if unable to create user
                                                                            # 0 if successful

def logged_in_now():
    return not current_user.is_anonymous

@login_manager.user_loader
def load_user(user_id):
    session = Session()
    account = session.query(User).filter(User.id==user_id).first()
    if account == None:
        session.close()
        print("No user stored for load_user(" + str(user_id) + ")")
        return AnonUser(user_id)
    session.close()
    return account

