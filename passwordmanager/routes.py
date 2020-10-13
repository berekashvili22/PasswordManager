from flask import render_template, url_for, flash, redirect
from passwordmanager import app, db, bcrypt
from passwordmanager.forms import RegistrationForm, LoginForm, AddPassword, GeneratePassword
from passwordmanager.models import User, Account
from flask_login import login_user, current_user, logout_user, login_required
import secrets



@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return 'about_page'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()

        flash(f'გილოცავ {form.first_name.data}! თქვენ წარმატებით გაიარეთ რეგისტრაცია', 'flash-success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('ავტორიზაცია წარმატებით განხორციელდა', 'flash-success')
            return redirect(url_for('account'))
        else:
            flash('ელ-ფოსტა ან პაროლი არასწორია , გთხოვთ ცადოთ თავიდან', 'flash-fail')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('თქვენ გამოხვედით სისტემიდან', 'flash-fail')
    return redirect(url_for('login'))


@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = AddPassword()
    return render_template('account.html', form=form)


@app.route('/generate_password', methods=['POST', 'GET'])
@login_required
def generate_password():
    form = GeneratePassword()

    password = secrets.token_urlsafe(form.password_rng.data)

    return render_template('generate.html', password=password, form=form)

