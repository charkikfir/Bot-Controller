import quart.flask_patch

from quart import Quart
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Quart(__name__)

app.config['SECRET_KEY'] = open("key.txt", 'r').read()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ids.db"

db = SQLAlchemy(app)
login_manager = LoginManager(app)

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from webcontroller import routes

