
from flask.app import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os



app = Flask(__name__, template_folder='templates', static_folder='CSS')

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/shop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(12).hex()


db = SQLAlchemy(app)


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
