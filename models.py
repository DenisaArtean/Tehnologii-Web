
from app_config import login_manager, db
import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#user_store = db.Table('user_store', db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
                        # db.Column('store_id', db.Integer, db.ForeignKey('store.store_id')))

class Users(db.Model, UserMixin):
  user_id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(120),nullable=False,unique=False)
  last_name = db.Column(db.String(120),nullable=False,unique=False)
  email = db.Column(db.String(255),nullable=False,unique=True)
  password = db.Column(db.String(120),nullable=False)
  date_creation = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
  store = db.relationship('Stores',cascade="all,delete",backref='user_store', lazy=True)

  def get_id(self):
      return (self.user_id)

class Stores(db.Model):
  store_id = db.Column(db.Integer, primary_key=True)
  type = db.Column(db.String(255), nullable=False,unique=False)
  name = db.Column(db.String(255), nullable=False,unique=False)
  address = db.Column(db.String(255), nullable=False,unique=False)
  ##store = db.relationship("user_store", secondary = user_store)
  user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'))



