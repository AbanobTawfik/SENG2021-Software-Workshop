from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '29q8j34t1982h'
login_manager = LoginManager()
login_manager.init_app(app)

import database
