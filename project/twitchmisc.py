import json
import urllib
import twitchclip


def getTopCatagories(num):
    hdrdata = {
        "Client-ID": "vl3lrnpqqho6ueb5relemvuvymvdg7",
        "first": str(num)
    }
    req = urllib.request.Request("https://api.twitch.tv/helix/games/top", headers=hdrdata)
    response = urllib.request.urlopen(req)
    return json.loads(response.read())["data"]


def getTopStreamers(num):
    hdrdata = {
        "Client-ID": "vl3lrnpqqho6ueb5relemvuvymvdg7",
    }
    req = urllib.request.Request("https://api.twitch.tv/helix/streams?first=" + str(num), headers=hdrdata)
    response = urllib.request.urlopen(req)
    return json.loads(response.read())["data"]


def getUsersInfo(ids):
    hdrdata = {
        "Client-ID": "vl3lrnpqqho6ueb5relemvuvymvdg7",
    }

    url = "https://api.twitch.tv/helix/users?id=" + str(ids[0])
    for i in range(len(ids) - 1):
        url = url + "&id=" + str(ids[i + 1])

    req = urllib.request.Request(url, headers=hdrdata)
    response = urllib.request.urlopen(req)
    return json.loads(response.read())["data"]


def getClipsInfo(ids):
    hdrdata = {
        "Client-ID": "vl3lrnpqqho6ueb5relemvuvymvdg7"
    }

    url = "https://api.twitch.tv/helix/clips?id=" + str(ids[0])
    for i in range(len(ids) - 1):
        url = url + "&id=" + str(ids[i + 1])

    req = urllib.request.Request(url, headers=hdrdata)
    response = urllib.request.urlopen(req)
    return json.loads(response.read())["data"]


def getGamesInfo(ids):
    hdrdata = {
        "Client-ID": "vl3lrnpqqho6ueb5relemvuvymvdg7"
    }

    url = "https://api.twitch.tv/helix/games?id=" + str(ids[0])
    for i in range(len(ids) - 1):
        url = url + "&id=" + str(ids[i + 1])

    req = urllib.request.Request(url, headers=hdrdata)
    response = urllib.request.urlopen(req)
    return json.loads(response.read())["data"]


def getClipObjects(ids):

    if len(ids) == 0:
        return []

    clipids = ids
    gameids = []
    userids = []
    clipobjects = []

    clipsdata = getClipsInfo(clipids)

    if clipsdata == []:
        return []

    for i in range(len(clipids)):
        if clipsdata[i]["game_id"] not in gameids:
            gameids.append(clipsdata[i]["game_id"])

    gamesdata = getGamesInfo(gameids)

    if gamesdata == []:
        return []

    for i in range(len(clipids)):
        if clipsdata[i]["creator_id"] not in userids:
            userids.append(clipsdata[i]["creator_id"])

    usersdata = getUsersInfo(userids)

    if usersdata == []:
        return []

    for i in range(len(clipids)):
        clipobjects.append(twitchclip.TwitchClip(clipids[i], clipsdata, gamesdata, usersdata))

    return clipobjects
