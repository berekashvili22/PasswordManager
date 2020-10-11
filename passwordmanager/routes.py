from flask import render_template, url_for, flash, redirect
from passwordmanager import app
from passwordmanager.forms import RegistrationForm, LoginForm
from passwordmanager.models import User, Account



@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return 'about_page'

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'გილოცავ {form.first_name.data}! თქვენ წარმატებით გაიარეთ რეგისტრაცია', 'flash_success')
        return redirect(url_for('home'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'test@gmail.com' and form.password.data == 'test':
            flash(f'გილოცავთ ავტორიზაცია წარმატებით განხორციელდა', 'flash_success')
            return redirect(url_for('home'))
        else:
            flash('unsuccsesful', 'flash_fail')

    return render_template('login.html', form=form)


