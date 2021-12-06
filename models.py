
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
  staff = db.relationship('Staff',cascade="all,delete",backref='staff_store', lazy=True)
  expenses = db.relationship('Expenses',cascade="all,delete",backref='expenses_store', lazy=True)
  products = db.relationship('Products',cascade="all,delete",backref='products_store', lazy=True)
  delivery = db.relationship('Delivery',cascade="all,delete",backref='delivery_store', lazy=True)



class Staff(db.Model):
  staff_id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(255), nullable=False,unique=False)
  last_name = db.Column(db.String(255), nullable=False,unique=False)
  job = db.Column(db.String(255), nullable=False,unique=False)
  start_date = db.Column(db.Date, nullable=False,unique=False)
  end_date = db.Column(db.String, nullable=False,unique=False)
  store_id = db.Column(db.Integer,db.ForeignKey('stores.store_id'))

class Expenses(db.Model):
  expense_id = db.Column(db.Integer, primary_key=True)
  type = db.Column(db.String(255), nullable=False,unique=False)
  date = db.Column(db.Date, nullable=False,unique=False)
  amount = db.Column(db.Float, nullable=False,unique=False)
  store_id = db.Column(db.Integer,db.ForeignKey('stores.store_id'))

class Products(db.Model):
  product_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False,unique=False)
  barcode = db.Column(db.String(255), nullable=False,unique=True)
  quantity = db.Column(db.Integer, nullable=False,unique=False)
  price = db.Column(db.Float, nullable=False,unique=False)
  store_id = db.Column(db.Integer,db.ForeignKey('stores.store_id'))

class Delivery(db.Model):
  delivery_id = db.Column(db.Integer, primary_key=True)
  company = db.Column(db.String(255), nullable=False,unique=False)
  quantity = db.Column(db.Integer, nullable=False,unique=False)
  date = db.Column(db.Date, nullable=False,unique=False)
  store_id = db.Column(db.Integer,db.ForeignKey('stores.store_id'))



