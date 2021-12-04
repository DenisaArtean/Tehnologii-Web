from flask import jsonify,make_response
from flask import render_template
from flask import redirect, url_for, request, flash 
from flask_login import login_user, current_user, logout_user, login_required


from form import RegisterForm
from models import Users

from passlib.hash import sha256_crypt
from app_config import app, db, login_manager

def getlist():
    user = Users.query.filter_by(email=current_user.email).first()
    my_list = user.Roles.split(",")
    return my_list

@app.route('/', methods=['POST','GET'])
@app.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
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
                return redirect(url_for('dashboard'))

            else:
                error = "Invalid Password"
                return render_template('Login.html', error=error)

        else:
            error = "Invalid email"
            return render_template('Login.html', error=error)

    return render_template('Login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

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

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('Dashboard.html')

@app.route('/products')
@login_required
def products():
    return render_template('Products.html')

@app.route('/delivery')
@login_required
def delivery():
    return render_template('Delivery.html')

@app.route('/expenses')
@login_required
def expenses():
    return render_template('Expenses.html')

@app.route('/salesreport')
@login_required
def salesreport():
    return render_template('SalesReport.html')

@app.route('/staff')
@login_required
def staff():
    return render_template('Staff.html')

@app.route('/store', methods=['POST','GET'])
@login_required
def store():
    #store = Store.query.all()
    #if request.method == 'POST':
      #  type = request.form.get('type')
     #   name = request.form.get('name')
       # address = request.form.get('address')
      #  add = Store(type=type, name=name, address=address, user_id=current_user)
      #  db.session.add(add)
      #  db.session.commit()
    return render_template('Store.html', store=store)

if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='127.0.0.1',  # Establishes the host, required for repl to detect the site
		port=5000  # Randomly select the port the machine hosts on.
	)
