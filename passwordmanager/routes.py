import os
import secrets, random, string
from flask import render_template, url_for, flash, redirect, request, abort
from passwordmanager import app, db, bcrypt, mail
from passwordmanager.forms import (RegistrationForm, LoginForm, AddAccount, GeneratePassword,
                                   UpdateAccount, UpdateProfile, RequestResetform, ResetPassworForm)
from passwordmanager.models import User, Account
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

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

    return render_template('account.html')


@app.route('/account/<int:user_id>/update', methods=['GET', 'POST'])
@login_required
def user_update(user_id):
    user = User.query.get_or_404(user_id)
    if user != current_user:
        about(403)
    form = UpdateProfile()
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        db.session.commit() 
        flash('ინფორმაცია წარმატებით განახლდა', 'flash-success')
        return redirect(url_for('account'))   

    elif request.method == 'GET':
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.email.data = user.email

    return render_template('profile_update.html', form=form)


@app.route('/generate_password', methods=['POST', 'GET'])
@login_required
def generate_password():
    form = GeneratePassword()
    default_length = form.password_rng.data

    # password options
    LOWER_LETTERS = string.ascii_lowercase
    UPPER_LETTERS = string.ascii_uppercase
    NUMBERS = string.digits
    SYMBOLS = string.punctuation
    LENGHT = form.password_rng.data 
    K = LENGHT if LENGHT is not None else 0

    # password user option 
    wantSymbols = form.symbols.data
    wantNumbers = form.numbers.data
    wantUpper = form.uppercase.data

    PASSWORD_CHARACTERS = LOWER_LETTERS

    PASSWORD_CHARACTERS += SYMBOLS if wantSymbols is not False else ''
    PASSWORD_CHARACTERS += NUMBERS if wantNumbers is not False else ''
    PASSWORD_CHARACTERS += UPPER_LETTERS if wantUpper is not False else ''

    # convert PASSWORD_CHARACTERS from string to shuffled list
    PASSWORD_CHARACTERS = list(PASSWORD_CHARACTERS)
    random.shuffle(PASSWORD_CHARACTERS)

    #generate password
    random_password = random.choices(PASSWORD_CHARACTERS, k=K)
    random_password = ''.join(random_password)

    return render_template('generate.html', password=random_password, form=form, length=K)


@app.route('/my_accounts', methods=['POST', 'GET'])
@login_required
def my_accounts():
    hex_color = '#fafa33'
    # pagination
    page = request.args.get('page', 1, type=int)
    accounts = Account.query.filter_by(owner = current_user).paginate(page=page, per_page=6) 
    return render_template('my_accounts.html', accounts=accounts, color=hex_color)


@app.route('/add_account', methods=['POST', 'GET'])
@login_required
def add_account():
    form = AddAccount()
    if form.validate_on_submit():
        account = Account(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data,
            site = form.site.data,
            owner = current_user
        )
        db.session.add(account)
        db.session.commit()

        flash('ექაუნთი წარმატებით დაემატა !', 'flash-success')
        return redirect(url_for('my_accounts'))

   
    return render_template('add_account.html', form=form)


@app.route('/my_accounts/<int:account_id>')
@login_required
def account_show(account_id):
    account = Account.query.get_or_404(account_id)
    return render_template('account_show.html', account=account)


@app.route('/my_accounts/<int:account_id>/update', methods=['GET', 'POST'])
@login_required
def account_update(account_id):
    account = Account.query.get_or_404(account_id)
    if account.owner != current_user:
        about(403)
    form = AddAccount()
    if form.validate_on_submit():
        account.username = form.username.data
        account.email = form.email.data
        account.password = form.password.data
        account.site = form.site.data
        db.session.commit() 
        flash('ინფორმაცია წარმატებით განახლდა', 'flash-success')
        return redirect(url_for('account_show', account_id=account.id))   

    elif request.method == 'GET':
        form.username.data = account.username
        form.email.data = account.email
        form.password.data = account.password
        form.site.data = account.site

    return render_template('account_update.html', form=form)

@app.route('/my_accounts/<int:account_id>/delete', methods=['GET', 'POST'])
@login_required
def account_delete(account_id):
    account = Account.query.get_or_404(account_id)
    if account.owner != current_user:
        abort(403)
    db.session.delete(account)
    db.session.commit()
    flash('ექაუნთი წაიშალა ბაზიდან', 'flash-fail')
    return redirect(url_for('my_accounts'))

# send token to email
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Reqeust',
                   sender='tornike berekashvili',
                   recipients=[user.email])
    msg.body = f''' გადადით ლინკზე პაროლის აღსადგენად :
{url_for('reset_token', token=token, _external=True)}
'''
    mail.send(msg)


# send reset password token
@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetform()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('ლინკი წარმატებით გაიგზავნა, შეამოწმეთ თქვენი ელ. ფოსტა', 'flash-success')
        return redirect(url_for('login'))

    return render_template('reset_request.html', form=form)

# reset password
@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('ლინკის მოქმედების დრო ამოიწურა, გთხოვთ ცადოთ თავიდან', 'flash-fail')
        return redirect(url_for('reset_request'))

    form = ResetPassworForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'პაროლი წარმატებით შეიცვალა !', 'flash-success')
        return redirect(url_for('login'))

    return render_template('reset_password.html', form=form)








@app.route('/about')
def about():
    return render_template('about_us.html')

@app.route('/contact')
def contact():
    return render_template('contact_us.html')
