from flask_login import UserMixin
from sqlalchemy import Column, String, Boolean
from sqlalchemy.types import CHAR
from base import Base

class User(Base):
    
    __tablename__ = 'USERS'
    id = Column(String(25), primary_key=True)
    username = Column(String(200))
    email = Column(String(250))
    passwordhash = Column(CHAR(128))
    active = Column(Boolean())

    def __init__(self, email, username, passwordhash, id, active=True):
        self.email = email
        self.username = username
        self.passwordhash = passwordhash
        self.id = id
        self.active = active

    @property
    def is_active(self):
        return self.active

    @property
    def is_authenticated(self):
        return True #FIX

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get_username(self):
        return self.username


class LikedClips (Base):
    
    __tablename__ = "LIKEDCLIPS"
    id = Column(String(25), primary_key = True)
    clip_id = Column(String(25))
    user_id = Column(String(25))
    
    def __init__(self, id, clip_id, user_id):
        self.id = id;
        self.clip_id = clip_id;
        self.user_id = user_id;


class HistoryClips (Base):
    
    __tablename__ = "HISTORY"
    id = Column(String(25), primary_key = True)
    clip_id = Column(String(25))
    user_id = Column(String(25))
    
    def __init__(self, id, clip_id, user_id):
        self.id = id;
        self.clip_id = clip_id;
        self.user_id = user_id;




def AnonUser(AnonymousUserMixin):
    def __init__(self, id):
        self.id = id
