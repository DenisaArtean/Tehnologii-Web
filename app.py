from re import S
from flask import jsonify,make_response
from flask import render_template
from flask import redirect, url_for, request, flash, g
from flask_login import login_user, current_user, logout_user, login_required
import flask_login
from flask_paginate import Pagination
from sqlalchemy.orm import session
from flask import session as sessi


from form import RegisterForm
from models import Users, Stores, Staff, Expenses, Products, Delivery, Sales
from passlib.hash import bcrypt
from app_config import app, db, login_manager
from sqlalchemy import func, extract
from datetime import date, timedelta
import json
from decimal import Decimal





def getlist():
    user = Users.query.filter_by(email=current_user.email).first()
    my_list = user.Roles.split(",")
    return my_list

#-------------------------------------------------------------------------------------------------------------------------------LOG IN---------


#def index():
 #   if not sessi.get("email"):
  #      return redirect(url_for('login'))
   # return render_template('Layout.html')

@app.route('/', methods=['POST','GET'])
@app.route('/login', methods=['POST','GET'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    #if request.cookies.get('useremail') & request.cookies.get('userpass'):
     #   if(sha256_crypt.verify(request.cookies.get('useremail'), current_user.email) & sha256_crypt.verify(request.cookies.get('userpass'), current_user.password)):
      #      user=Users.query.filter_by(email=current_user.email).first()
       #      login_user(user)

    if request.method == 'POST':
        # Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']

        user=Users.query.filter_by(email=email).first()
        if user:

            passwordd=Users.query.filter_by(email=email).first()
            if bcrypt.verify(password_candidate, passwordd.password):
                login_user(user)
                return redirect(url_for('dashboard'))

                #flash('You are now logged in', 'success')
                #resp = make_response(redirect(url_for('dashboard')))
                #resp.set_cookie('useremail', (bcrypt.hash(str(email))))
                #sessi["email"] = email
                #resp.set_cookie('userpass', (bcrypt.hash(str(password_candidate))))
                #return resp

            else:
                error = "Invalid Password"
                return render_template('Login.html', error=error)

        else:
            error = "Invalid email"
            return render_template('Login.html', error=error)

    return render_template('Login.html')


#-------------------------------------------------------------------------------------------------------------------------------LOG OUT---------


@app.route('/logout')
@login_required
def logout():
    sessi["email"] = None
    logout_user()
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie('storeID')
    resp.delete_cookie('useremail')
    resp.delete_cookie('userpass')
    return resp

#-------------------------------------------------------------------------------------------------------------------------------SIGN UP---------


@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = bcrypt.hash(str(form.password.data))
        addd = Users(first_name=first_name, last_name=last_name, email=email, password= password)
        db.session.add(addd)
        db.session.commit()
        flash('You are now registered', 'success')
        return redirect(url_for('login'))
    return render_template('SignUp.html', form=form)

#------------------------------------------------------------------------------------------------------------------------------DASHBOARD---------


@app.route('/dashboard')
@login_required
def dashboard():
    store = request.cookies.get('storeID')
    sales = Sales.query.filter(Sales.store_id == store).filter(func.date(Sales.date) > date.today()-timedelta(days=7)).all()
    sum = 0
    for i in sales:
        sum = sum + i.sales

    staff = Staff.query.filter(Staff.store_id == store).filter(Staff.end_date == "-").all()
    count_staff = 0
    for j in staff:
        count_staff = count_staff + 1
    

    products = Products.query.filter(Products.store_id == store).all()
    count_products = 0
    for k in products:
        count_products = count_products + k.quantity

    expenses = Expenses.query.filter(Expenses.store_id == store).filter(func.date(Expenses.date) > date.today()-timedelta(days=30)).all()
    exp = 0
    for l in expenses:
        exp = exp + l.amount
 
    context = {
        "weekly": sum,
        "expenses": exp,
        "products": count_products,
        "staff": count_staff
    }

    dates = db.session.query(db.func.sum(Sales.sales), Sales.date).group_by(Sales.date).order_by(Sales.date).filter(extract('year', Sales.date)==extract('year', date.today())).filter(Sales.store_id == store).all()

    dates_sales = []
    sales_by = []
    for amount, datee in dates:
        dates_sales.append(datee.strftime("%y-%m-%d"))
        sales_by.append(amount)


    s = db.session.query(db.func.sum(Sales.sales), extract('month', Sales.date)).group_by(extract('year', Sales.date), extract('month', Sales.date)).order_by(extract('year', Sales.date)).filter(extract('year', Sales.date)==extract('year', date.today())).filter(Sales.store_id == store).all()
    dates_month_sales = []
    sales_by_1 = []
    for amount1, month in s:
        dates_month_sales.append(int(month))
        sales_by_1.append(amount1)


    em = db.session.query(db.func.sum(Expenses.amount), extract('month', Expenses.date)).group_by(extract('year', Expenses.date), extract('month', Expenses.date)).order_by(extract('year', Expenses.date)).filter(extract('year', Expenses.date)==extract('year', date.today())).filter(Expenses.store_id == store).all()
    dates_expenses = []
    expenses_by = []
    for amount2, month in em:
        dates_expenses.append(int(month))
        expenses_by.append(amount2)

    
    sa = db.session.query(db.func.sum(Sales.sales), extract('year', Sales.date)).group_by(extract('year', Sales.date)).order_by(extract('year', Sales.date)).filter(Sales.store_id == store).all()
    years_sales = []
    sales_by_2 = []
    for amount3, year in sa:
        years_sales.append(int(year))
        sales_by_2.append(amount3)

    ea = db.session.query(db.func.sum(Expenses.amount), extract('year', Expenses.date)).group_by(extract('year', Expenses.date)).order_by(extract('year', Expenses.date)).filter(Expenses.store_id == store).all()
    years_expenses = []
    expenses_by_1 = []
    for amount4, year in ea:
        years_expenses.append(int(year))
        expenses_by_1.append(amount4)

    return render_template('Dashboard.html', context = context, 
                            dates_sales = json.dumps(dates_sales), 
                            sales_by = json.dumps(sales_by),
                            dates_month_sales = json.dumps(dates_month_sales),
                            sales_by_1 = json.dumps(sales_by_1),
                            dates_expenses = json.dumps(dates_expenses),
                            expenses_by = json.dumps(expenses_by),
                            years_sales = json.dumps(years_sales),
                            sales_by_2 = json.dumps(sales_by_2),
                            years_expenses = json.dumps(years_expenses),
                            expenses_by_1 = json.dumps(expenses_by_1))


#----------------------------------------------------------------------------------------------------------------------------PRODUCTS---------


@app.route('/products', methods=['POST','GET'])
@login_required
def products():
    page = request.args.get('page', 1, type=int)
    store = request.cookies.get('storeID')
    products = Products.query.filter(Products.store_id == store).paginate(page = page, per_page = 5)
    if request.method == 'POST':
        name = request.form.get('name')
        barcode = request.form.get('barcode')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        add = Products(name = name, barcode = barcode, quantity = quantity, price = price, store_id = store)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for('products'))
    
    return render_template('Products.html', products=products)

@app.route("/updateproduct/<int:product_id>", methods=['POST','GET'])
@login_required
def update_product(product_id):
    product = Products.query.get(product_id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.barcode = request.form.get('barcode')
        product.quantity = request.form.get('quantity')
        product.price = request.form.get('price')
        db.session.commit()
        return redirect(url_for('products'))

    return render_template('update_product.html',product=product)

@app.route("/product/delete/<int:product_id>", methods=['POST'])
@login_required
def delete_product(product_id):
    product = Products.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('products'))


#-------------------------------------------------------------------------------------------------------------------------------DELIVERY---------


@app.route('/delivery', methods=['POST','GET'])
@login_required
def delivery():
    page = request.args.get('page', 1, type=int)
    store = request.cookies.get('storeID')
    delivery = Delivery.query.filter(Delivery.store_id == store).paginate(page = page, per_page = 5)
    if request.method == 'POST':
        company = request.form.get('company')
        quantity = request.form.get('quantity')
        date = request.form.get('date')
        add = Delivery(company = company, quantity = quantity, date = date, store_id = store)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for('delivery'))
    return render_template('Delivery.html', delivery=delivery)

@app.route("/updatedelivery/<int:delivery_id>", methods=['POST','GET'])
@login_required
def update_delivery(delivery_id):
    delivery = Delivery.query.get(delivery_id)
    if request.method == 'POST':
        delivery.company = request.form.get('company')
        delivery.quantity = request.form.get('quantity')
        delivery.date = request.form.get('date')
        db.session.commit()
        return redirect(url_for('delivery'))

    return render_template('update_delivery.html',delivery=delivery)

@app.route("/delivery/delete/<int:delivery_id>", methods=['POST'])
@login_required
def delete_delivery(delivery_id):
    delivery = Delivery.query.get(delivery_id)
    db.session.delete(delivery)
    db.session.commit()
    return redirect(url_for('delivery'))

#-------------------------------------------------------------------------------------------------------------------------------EXPENSES---------


@app.route('/expenses', methods=['POST','GET'])
@login_required
def expenses():
    page = request.args.get('page', 1, type=int)
    store = request.cookies.get('storeID')
    expenses = Expenses.query.filter(Expenses.store_id == store).paginate(page = page, per_page = 5)
    if request.method == 'POST':
        type = request.form.get('type')
        date = request.form.get('date')
        amount = request.form.get('amount')
        add = Expenses(type=type, date=date, amount=amount, store_id = store)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for('expenses'))
    return render_template('Expenses.html', expenses=expenses)

@app.route("/updateexpense/<int:expense_id>", methods=['POST','GET'])
@login_required
def update_expense(expense_id):
    expense = Expenses.query.get(expense_id)
    if request.method == 'POST':
        expense.type = request.form.get('type')
        expense.date = request.form.get('date')
        expense.amount = request.form.get('amount')
        db.session.commit()
        return redirect(url_for('expenses'))

    return render_template('update_expense.html',expense=expense)

@app.route("/expense/delete/<int:expense_id>", methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expenses.query.get(expense_id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('expenses'))


#-------------------------------------------------------------------------------------------------------------------------SALES REPORT---------


@app.route('/salesreport', methods=['POST','GET'])
@login_required
def salesreport():
    page = request.args.get('page', 1, type=int)
    store = request.cookies.get('storeID')
    sales = Sales.query.filter(Sales.store_id == store).paginate(page = page, per_page = 5)
    if request.method == 'POST':
        date = request.form.get('date')
        sales = request.form.get('sales')
        refunded = request.form.get('refunded')
        discounts = request.form.get('discounts')
        add = Sales(date = date, sales = sales, refunded = refunded, discounts = discounts, store_id = store)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for('salesreport'))
    return render_template('SalesReport.html', sales=sales)

@app.route("/updatesalesreport/<int:sales_id>", methods=['POST','GET'])
@login_required
def update_salesreport(sales_id):
    sales = Sales.query.get(sales_id)
    if request.method == 'POST':
        sales.date = request.form.get('date')
        sales.sales = request.form.get('sales')
        sales.refunded = request.form.get('refunded')
        sales.discounts = request.form.get('discounts')
        db.session.commit()
        return redirect(url_for('salesreport'))

    return render_template('update_sales_report.html',sales=sales)

@app.route("/salesreport/delete/<int:sales_id>", methods=['POST'])
@login_required
def delete_salesreport(sales_id):
    sales = Sales.query.get(sales_id)
    db.session.delete(sales)
    db.session.commit()
    return redirect(url_for('salesreport'))


#-------------------------------------------------------------------------------------------------------------------------------STAFF---------

@app.route('/staff', methods=['POST','GET'])
@login_required
def staff():
    page = request.args.get('page', 1, type=int)
    store = request.cookies.get('storeID')
    staff = Staff.query.filter(Staff.store_id == store).paginate(page = page, per_page = 5)
    if request.method == 'POST':
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        job = request.form.get('job')
        start_date = request.form.get('startdate')
        end_date = request.form.get('enddate')
        add = Staff(first_name=first_name, last_name=last_name, job=job, start_date=start_date, end_date=end_date, store_id = store)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for('staff'))
    return render_template('Staff.html', staff=staff)

@app.route("/updatestaff/<int:staff_id>", methods=['POST','GET'])
@login_required
def update_staff(staff_id):
    staff = Staff.query.get(staff_id)
    if request.method == 'POST':
        staff.first_name = request.form.get('firstname')
        staff.last_name = request.form.get('lastname')
        staff.job = request.form.get('job')
        staff.start_date = request.form.get('startdate')
        staff.end_date = request.form.get('enddate')
        db.session.commit()
        return redirect(url_for('staff'))

    return render_template('update_staff.html',staff=staff)

@app.route("/staff/delete/<int:staff_id>", methods=['POST'])
@login_required
def delete_staff(staff_id):
    staff = Stores.query.get(staff_id)
    db.session.delete(staff)
    db.session.commit()
    return redirect(url_for('staff'))

# --------------------------------------------------------------------------------------------------------------------------------STORE--------

@app.route('/stores', methods=['POST','GET'])
@login_required
def stores():
    page = request.args.get('page', 1, type=int)
    stores = Stores.query.filter(Stores.user_store == current_user).paginate(page = page, per_page = 5)
    if request.method == 'POST':
        type = request.form.get('type')
        name = request.form.get('name')
        address = request.form.get('address')
        add = Stores(type=type, name=name, address=address, user_store=current_user)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for('stores'))
    return render_template('Store.html', stores=stores)

@app.route("/store/select/<int:store_id>", methods=['POST','GET'])
@login_required
def select_store(store_id):
    print(store_id, type(store_id))
    store = Stores.query.get(store_id)
    resp = make_response(redirect(url_for('stores')))
    resp.set_cookie('storeID', str(store_id))

    return resp

@app.route("/updatestore/<int:store_id>", methods=['POST','GET'])
@login_required
def update_store(store_id):
    store = Stores.query.get(store_id)
    if request.method == 'POST':
        store.type = request.form.get('type')
        store.name = request.form.get('name')
        store.address = request.form.get('address')
        db.session.commit()
        return redirect(url_for('stores'))

    return render_template('update_store.html',store=store)

@app.route("/store/delete/<int:store_id>", methods=['POST'])
@login_required
def delete_store(store_id):
    store = Stores.query.get(store_id)
    db.session.delete(store)
    db.session.commit()
    return redirect(url_for('stores'))

#--------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='127.0.0.1',  # Establishes the host, required for repl to detect the site
		port=5000  # Randomly select the port the machine hosts on.
	)
