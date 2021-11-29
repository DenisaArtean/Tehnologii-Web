
from app_config import login_manager, db
import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(120),nullable=False,unique=False)
  last_name = db.Column(db.String(120),nullable=False,unique=False)
  email = db.Column(db.String(80),nullable=False,unique=True)
  password = db.Column(db.String(120),nullable=False)
  date_creation = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
