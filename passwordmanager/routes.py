from flask import render_template, url_for, flash, redirect, request, abort
from passwordmanager import app, db, bcrypt
from passwordmanager.forms import RegistrationForm, LoginForm, AddAccount, GeneratePassword, UpdateAccount
from passwordmanager.models import User, Account
from flask_login import login_user, current_user, logout_user, login_required
import secrets, random, string



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

    return render_template('account.html')


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
    hex_color = f'#{random.randint(0, 0xff_ff_ff):06x}' #generates rand hex color
    accounts = Account.query.all()
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

    return redirect(url_for('my_accounts'))