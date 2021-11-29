
from flask import render_template
from flask import redirect, url_for, request, flash 
from flask_login import login_user, current_user, logout_user, login_required


from form import RegisterForm
from models import User

from passlib.hash import sha256_crypt
from app_config import app, db, login_manager

@app.route('/')
@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        # Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']

        user=User.query.filter_by(email=email).first()
        if user:

            passwordd=User.query.filter_by(email=email).first()
            if sha256_crypt.verify(password_candidate, passwordd.password):
                login_user(user)
                #flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))

            else:
                error = "Invalid Password"
                return render_template('login.html', error=error)

        else:
            error = "Invalid email"
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form1 = RegisterForm(request.form)
    if request.method == 'POST' and form1.validate():
        first_name = form1.first_name.data
        last_name = form1.last_name.data
        email = form1.email.data
        password = sha256_crypt.encrypt(str(form1.password.data))
        addd = User(first_name=first_name, last_name=last_name, email=email, password= password)
        db.session.add(addd)
        db.session.commit()
        flash('You are now registered', 'success')
        return redirect(url_for('login'))
    return render_template('SignUp.html', form=form1)

@app.route('/dashboard')
def dashboard():
    return render_template('Dashboard.html')

@app.route('/products')
def products():
    return render_template('Products.html')

@app.route('/delivery')
def delivery():
    return render_template('Delivery.html')

@app.route('/expenses')
def expenses():
    return render_template('Expenses.html')

@app.route('/salesreport')
def salesreport():
    return render_template('SalesReport.html')

@app.route('/staff')
def staff():
    return render_template('Staff.html')

@app.route('/store')
def settings():
    return render_template('Store.html')

if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='127.0.0.1',  # Establishes the host, required for repl to detect the site
		port=5000  # Randomly select the port the machine hosts on.
	)
