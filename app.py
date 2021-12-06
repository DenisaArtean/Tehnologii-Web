from flask import jsonify,make_response
from flask import render_template
from flask import redirect, url_for, request, flash, g
from flask_login import login_user, current_user, logout_user, login_required

from form import RegisterForm
from models import Users, Stores, Staff, Expenses
from passlib.hash import sha256_crypt
from app_config import app, db, login_manager


def getlist():
    user = Users.query.filter_by(email=current_user.email).first()
    my_list = user.Roles.split(",")
    return my_list

#-------------------------------------------------------------------------------------------------------------------------------LOG IN---------


@app.route('/', methods=['POST','GET'])
@app.route('/login', methods=['POST','GET'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    #if request.cookies.get('useremail') & request.cookies.get('userpass'):
     #   if(sha256_crypt.verify(request.cookies.get('useremail'), current_user.email) & sha256_crypt.verify(request.cookies.get('userpass'), current_user.password)):
      #      user=Users.query.filter_by(email=sha256_crypt.decrypt(request.cookies.get('useremail'))).first()
       #     login_user(user)
    if request.method == 'POST':
        # Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']

        user=Users.query.filter_by(email=email).first()
        if user:

            passwordd=Users.query.filter_by(email=email).first()
            if sha256_crypt.verify(password_candidate, passwordd.password):
                login_user(user)
                #flash('You are now logged in', 'success')
                resp = make_response(redirect(url_for('dashboard')))
                resp.set_cookie('useremail', sha256_crypt.encrypt(str(email)))
                resp.set_cookie('userpass', sha256_crypt.encrypt(str(password_candidate)))
                return resp

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
        password = sha256_crypt.encrypt(str(form.password.data))
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
    return render_template('Dashboard.html')


#----------------------------------------------------------------------------------------------------------------------------PRODUCTS---------


@app.route('/products')
@login_required
def products():
    return render_template('Products.html')


#-------------------------------------------------------------------------------------------------------------------------------DELIVERY---------


@app.route('/delivery')
@login_required
def delivery():
    return render_template('Delivery.html')

#-------------------------------------------------------------------------------------------------------------------------------EXPENSES---------


@app.route('/expenses', methods=['POST','GET'])
@login_required
def expenses():
    store = request.cookies.get('storeID')
    expenses = Expenses.query.filter(Expenses.store_id == store).all()
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


@app.route('/salesreport')
@login_required
def salesreport():
    return render_template('SalesReport.html')


#-------------------------------------------------------------------------------------------------------------------------------STAFF---------

@app.route('/staff', methods=['POST','GET'])
@login_required
def staff():
    store = request.cookies.get('storeID')
    staff = Staff.query.filter(Staff.store_id == store).all()
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
    stores = Stores.query.filter(Stores.user_store == current_user).all()
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
