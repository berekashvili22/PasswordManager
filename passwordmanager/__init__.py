import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail




app = Flask(__name__)

app.config['SECRET_KEY'] = '6eb8561dad8ea36afbf0e7df61a6c8d2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'გთხოვთ გაიაროთ ავტორიზაცია'
login_manager.login_message_category = 'flash-info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'example@gmail.com' # mail u want to send mails from
app.config['MAIL_PASSWORD'] = 'example' # password of that mail
# app.config['MAIL_DEFAULT_SENDER'] = 'noreplay@demo.com'

mail = Mail(app)



from passwordmanager import routes

