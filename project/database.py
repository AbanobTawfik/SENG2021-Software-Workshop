"""
High-Level interaction with the database.
For use in routes.py, etc.
Add high-level functions here,
e.g. Adding a clip function,
Commenting on a clip,
Viewing user clips,

Add those methods to the StorageSystem class
**Use the "storageSystem" variable to access the main database**,
accessed using this interface
"""
from sqlalchemy import Column, ForeignKey, Integer, String

from user import User, HistoryClips, LikedClips
from twitchclip import TwitchClip
from authenticator import login_user
import hashlib
import twitchmisc
from random import choice
from string import digits, ascii_lowercase, ascii_uppercase
from base import Session, Base, engine
from random import randrange


class StorageSystem(object):
    def create_table(self):
        # If the database isn't setup yet, i.e. no user table,
        # Then this will set up all the tables, given the base class(es).
        Base.metadata.create_all(engine)

    def get_twitch_clip(self, clip_id):
        session = Session()
        clip = session.query(TwitchClip).filter(TwitchClip.id == clip_id).first()
        #print(clip)
        session.close()
        return clip

    # Add a twitch clip, given a id
    def add_twitch_clip(self, id):
        ret = False
        #print(id)
        if (storageSystem.get_twitch_clip(id) != None):
            return ret

        session = Session()
        clipObject = twitchmisc.getClipObjects([id])
        if (len(clipObject) == 0 or clipObject[0] == None):
            return False

        #print (clipObject[0])

        try:
            session.add(clipObject[0])
            session.commit()
            #update_clips(all_clip_ids, all_clips)
            for i in range(len(clipObject)):
                if clipObject[i].id not in all_clip_ids:
                    session.expunge(clipObject[i])
                    all_clips.append(clipObject[i])
                    all_clip_ids.append(clipObject[i].id)

            ret = True
        except:
            ret = False
        finally:
            session.close()
            return ret

    # Remove a twitch clip
    # Remove Successful in list[0], all_clips = list[1], all_clip_ids = list[2]
    def remove_twitch_clip(self, id):
        #update database,
        #all_clips,
        #all_clip_ids
        ret = False

        if storageSystem.get_twitch_clip(id) == None:
            return ret

        session = Session()
        clipObjectAPI = twitchmisc.getClipObjects([id])
        clipObjectDB = storageSystem.get_twitch_clip(id)

        try:
            #Remove from database
            session.delete(clipObjectDB)
            #Remove from all clips
            all_clips.remove(clipObjectAPI[0])
            #Remove from all_clips_ids
            all_clip_ids.remove(id)
            ret = True
            session.commit()
        except:
            ret = False
        finally:

            session.close()
            return ret

    # returns 0 for success, 1 for in-use email, 2 for other error
    def new_user(self, email, username, password):
        session = Session()


        if self.email_to_id(email) is not None:
            return 1

        id = None
        while id is None or session.query(User).filter(User.id == id).first() is not None:
            chars = digits + ascii_lowercase + ascii_uppercase
            id = "".join([choice(chars) for i in range(25)])

        print("Using new user id: " + str(id))

        new_user = User(email, hashlib.sha512(password.encode("utf-8")).hexdigest(), id, username)
        try:
            session.add(new_user)
            session.commit()
            session.close()
            return 0
        except:
            session.close()
            return 2

    def user_exists(self, id):
        session = Session()
        ret = False

        try:
            user = session.query(User).filter(User.id == id).one()
        except:
            print("User", id, "not found...")
        else:
            ret = True
        finally:
            session.close()
            return ret

    def email_to_id(self, email):
        session = Session()

        try:
            user = session.query(User).filter(User.email == email).one()
        except:
            print("Email", id, "not found...")
            session.close()
            return None
        else:
            session.close()
            return user.id

    def email_exists(self, email):
        session = Session()
        ret = False

        try:
            user = session.query(User).filter(User.email == email).one()
        except:
            print("Email", email, "not found...")
        else:
            ret = True
        finally:
            session.close()
            return ret

    def username_exists(self, username):
        session = Session()
        ret = False

        try:
            user = session.query(User).filter(User.username == username).one()
        except:
            print("Username", username, "not found...")
        else:
            ret = True
        finally:
            session.close()
            return ret

    def search_passwordhash(self, id):
        session = Session()

        try:
            user = session.query(User).filter(User.id == id).one()
        except:
            print("User", id, "not found...")
            session.close()
            return None
        else:
            print("User found")
        finally:
            session.close()
            return user.passwordhash

    def add_to_history(self, clip_id, user_id):
        ret = False
        session = Session()

        if (self.get_twitch_clip(clip_id) is not None) and (self.user_exists(user_id) == True):
            id = None
            while id is None or session.query(HistoryClips).filter(HistoryClips.id == id).first() is not None:
                chars = digits + ascii_lowercase + ascii_uppercase
                id = "".join([choice(chars) for i in range(25)])

            new_relationship = HistoryClips(id=id, clip_id=clip_id, user_id=user_id)
            try:
                session.add(new_relationship)
            except:
                raise
            else:
                ret = True
                session.commit()
            finally:
                session.close()
                return ret
        else:
            session.close()
            return ret

    def get_user_history(self, user_id):
        session = Session()

        user_history = session.query(HistoryClips).filter(HistoryClips.user_id == user_id).all()
        history_list = []
        final_list = []
        final_clip_list = []

        for clip in user_history:
            history_list.append(clip.clip_id)

        return history_list

        '''for i in range(len(history_list)):
            element = history_list[len(history_list)-1-i]
            if (element not in final_list):
                final_list.append(element)

        for clip_id in final_list:
            clip = storageSystem.get_twitch_clip(clip_id)
            if clip != None:
                final_clip_list.append(clip)


        session.close()
        return final_clip_list'''

    def add_to_liked_clips(self, clip_id, user_id):
    
        ret = False
        session = Session()

        if (self.get_twitch_clip(clip_id) is not None) and (self.user_exists(user_id) == True):
            id = None
            while id is None or session.query(LikedClips).filter(LikedClips.id == id).first() is not None:
                chars = digits + ascii_lowercase + ascii_uppercase
                id = "".join([choice(chars) for i in range(25)])

            new_relationship = LikedClips(id=id, clip_id=clip_id, user_id=user_id)
            try:
                session.add(new_relationship)
            except:
                raise
            else:
                ret = True
                session.commit()
            finally:
                session.close()
                return ret
        else:
            session.close()
            return ret
    
    def get_user_liked_clips(self, user_id):
        session = Session()

        user_history = session.query(LikedClips).filter(LikedClips.user_id == user_id).all()
        history_list = []
        final_list = []
        final_clip_list = []

        for clip in user_history:
            history_list.append(clip.clip_id)
        
        
        return history_list

    def get_all_clip_ids(self):
        session = Session()

        clips = session.query(TwitchClip).all()
        clips_id_list = []

        for clip in clips:
            clips_id_list.append(clip.id)

        session.close()
        return clips_id_list



"""
# Functions implemented for the flask login
def check_password(user_id, passwordhash):
    if storageSystem.user_exists(user_id):
        print("User", user_id, "Found")
        if passwordhash == storageSystem.search_passwordhash(user_id):
            user = User(user_id)
            login_user(user)

            return True

def create_user(user_id, passwordhash, email):
    if storageSystem.user_exists(user_id):
        return 1                            # User Already Exists
    if storageSystem.email_exists(email):
        return 2                            # Email Already Exists                  
    return storageSystem.new_user(user_id, email, passwordhash)             # 3 if unable to create user
                                                                            # 0 if successful
"""


# Public function to login a username and password
def check_password(id, password, rememberdetails):
    session = Session()
    account = session.query(User).filter(User.id == id).one()

    if account is None:
        # No account with that id
        print("No account with id " + str(id))
        return False
    session.close()

    given_hashed = hashlib.sha512((password).encode("utf-8") ).hexdigest()
    #if account.passwordhash == given_hashed:
    user = User("", account.username, account.passwordhash, account.id)
    login_user(user, rememberdetails)
    return True
    #return False

# Afterwards need to set all_clips_ids = list[0] and all_clips = list[1]
def update_clips(all_clips_ids, all_clips):
    new_all_clip_ids = storageSystem.get_all_clip_ids()
    new_clip_id_list = []
    #print(new_all_clip_ids)
    #print(all_clip_ids)

    for id in new_all_clip_ids:
        if id not in all_clips_ids:
            new_clip_id_list.append(id)

    new_clips_list = twitchmisc.getClipObjects(new_clip_id_list)
    print(all_clip_ids)
    all_clips = all_clips + new_clips_list
    return [new_all_clip_ids, all_clips]

def get_random_clip():
    randin = randrange(0,len(all_clips))
    return all_clips[randin]


storageSystem = StorageSystem()
storageSystem.create_table()
all_clip_ids = storageSystem.get_all_clip_ids()
all_clips = twitchmisc.getClipObjects(all_clip_ids)
print(all_clip_ids)
