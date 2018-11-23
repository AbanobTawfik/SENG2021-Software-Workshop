from server import app
import database
from flask import render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from user import User
import twitchmisc
from twitchclip import TwitchClip
import authenticator


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html",database=database)

@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":
        cliplink = request.form["ClipLink"]
        description = request.form["description"]
        tags = request.form["tags"]

        if "https://clips.twitch.tv/" in cliplink:
            cliplink = cliplink.replace("https://clips.twitch.tv/", "")
            bool = database.storageSystem.add_twitch_clip(cliplink)
            print("Added clip: " + str(bool))
        else:
            print("Bad clip")


    return render_template("upload.html")


@app.route("/clip/<clip_id>", methods=["GET"])
def clip(clip_id):

    clip = 0

    for i in database.all_clips:
        if clip_id == i.id:
            clip = i

    if current_user.is_authenticated:
        database.StorageSystem.add_to_history(database.storageSystem,clip.id,current_user.get_id())

    return render_template("clip.html", clip=clip, database=database)


@app.route("/categories", methods=["GET"])
def categories():
    rws = 2
    cls = 4
    data = twitchmisc.getTopCatagories(rws * cls)

    for i in range(rws * cls):
        data[i]["box_art_url"] = data[i]["box_art_url"].replace("{width}", "285")
        data[i]["box_art_url"] = data[i]["box_art_url"].replace("{height}", "380")

    print(data)

    return render_template("categories.html", data=data, rws=rws, cls=cls)


@app.route("/streamers", methods=["GET"])
def streamers():
    rws = 4
    cls = 4
    data = twitchmisc.getTopStreamers(rws * cls)

    ids = []
    for i in range(rws * cls):
        ids.append(data[i]["user_id"])

    print(ids)

    names = twitchmisc.getUsersInfo(ids)
    print(names)

    for i in range(rws * cls):
        data[i]["thumbnail_url"] = data[i]["thumbnail_url"].replace("{width}", "470")
        data[i]["thumbnail_url"] = data[i]["thumbnail_url"].replace("{height}", "270")
        data[i]["name"] = names[i]["display_name"]

    print(data)

    return render_template("streamers.html", data=data, rws=rws, cls=cls)


@app.route("/login", methods=["GET", "POST"])
def login():

    print(request.form)

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]
        rememberdetails = "rememberdetails" in request.form

        uid = database.storageSystem.email_to_id(email)

        print("UID: " + uid)

        if uid == None:
            print("Invalid email " + email)
            return generic_error("Invalid email", "The email address " + email + " isn't valid")
        elif database.check_password(uid, password, rememberdetails):
            return generic_error("Success", "Login success")
        else:
            return generic_error("Invalid password", "The login credentials are incorrect")

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":

        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        passwordconfirm = request.form["passwordconfirm"]
        if password != passwordconfirm:
            return generic_error("Password does not match", "Password does not match confirmation")

        result = database.storageSystem.new_user(email, username, password)
        if result == 1:
            return generic_error("Email already in use", "Email already in use")
        elif result != 0:
            return generic_error("Generic error", "Generic error")
        else:
            return redirect(url_for("index"))

    return render_template("signup.html")


def generic_error(title, body):
    return render_template("error.html", title=title, body=body)


@app.route("/search", methods=["GET", "POST"])
def search():
    searchstr = request.args.get("search")

    print(current_user.get_id())

    matchedclips = []
    for i in range(len(database.all_clips)):
        if searchstr.lower() in database.all_clips[i].title.lower() or searchstr.lower() in database.all_clips[i].creatordisplayname.lower() or searchstr.lower() in database.all_clips[i].gamename.lower():
            matchedclips.append(database.all_clips[i])

    print("Matched Clips: " + str(matchedclips))

    return render_template("search.html", searchstr=searchstr, matchedclips=matchedclips)


@app.route("/account", methods=["GET"])
def my_profile():
    return render_template("account.html")


@app.route("/liked", methods=["GET"])
def liked():

    historyclipids = database.StorageSystem.get_user_liked_clips(database.storageSystem, current_user.get_id())
    historyclips = twitchmisc.getClipObjects(historyclipids)
    return render_template("liked.html", historyclips = historyclips)

@app.route("/clip/postToLike.html/<clip_id>", methods=["GET"])
def post_to_like(clip_id):
    if current_user.is_authenticated:
        database.StorageSystem.add_to_liked_clips(database.storageSystem,clip_id,current_user.get_id())
        return redirect("/clip/" + clip_id)
    else:
        return generic_error("You need to be logged in to do that", "You need to be logged in to like a clip")


@app.route("/history", methods=["GET"])
@login_required
def history():

    historyclipids = database.StorageSystem.get_user_history(database.storageSystem, current_user.get_id())
    historyclips = twitchmisc.getClipObjects(historyclipids)

    return render_template("history.html", historyclips=historyclips)
