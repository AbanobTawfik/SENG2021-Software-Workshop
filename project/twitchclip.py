import urllib
import json
from base import Base
from sqlalchemy import Column, String


class TwitchClip(Base):
    
    __tablename__ = "CLIPS"
    #If we encounter video id's longer than 25, extend this
    id = Column(String(50), primary_key=True)
    url = Column(String(1000))
    embedurl = Column(String(1000))
    

    def __init__(self, id, clipsdata, gamesdata, usersdata):
        corrcd = -1
        corrgd = -1
        corrud = -1

        for i in range(len(clipsdata)):
            if clipsdata[i]["id"] == id:
                corrcd = i
                break

        for i in range(len(gamesdata)):
            if gamesdata[i]["id"] == clipsdata[corrcd]["game_id"]:
                corrgd = i
                break

        for i in range(len(usersdata)):
            if usersdata[i]["id"] == clipsdata[corrcd]["creator_id"]:
                corrud = i

        if corrcd == -1 or corrgd == -1 or corrud == -1:
            print("Clip could not init with tuple: " + "(" + corrcd + "," + corrgd + "," + corrud + ")")

        self.id = id
        self.url = clipsdata[corrcd]["url"]
        self.embedurl = clipsdata[corrcd]["embed_url"]
        self.broadcasterid = clipsdata[corrcd]["broadcaster_id"]
        self.creatorid = clipsdata[corrcd]["creator_id"]
        self.videoid = clipsdata[corrcd]["video_id"]
        self.gameid = clipsdata[corrcd]["game_id"]
        self.language = clipsdata[corrcd]["language"]
        self.title = clipsdata[corrcd]["title"]
        self.viewcount = clipsdata[corrcd]["view_count"]
        self.createdat = clipsdata[corrcd]["created_at"]
        self.thumbnailurl = clipsdata[corrcd]["thumbnail_url"]

        self.gamename = gamesdata[corrgd]["name"]
        self.boxarturl = gamesdata[corrgd]["box_art_url"]

        self.creatorlogin = usersdata[corrud]["login"]
        self.creatordisplayname = usersdata[corrud]["display_name"]
        self.creatortype = usersdata[corrud]["type"]
        self.creatorbroadcastertype = usersdata[corrud]["broadcaster_type"]
        self.creatordescription = usersdata[corrud]["description"]
        self.creatorprofileimageurl = usersdata[corrud]["profile_image_url"]
        self.creatorofflineimageurl = usersdata[corrud]["offline_image_url"]
        self.creatorviewcount = usersdata[corrud]["view_count"]



