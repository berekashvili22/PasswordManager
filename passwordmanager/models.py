from passwordmanager import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    accounts = db.relationship('Account', backref='owner', lazy=True)

    def __rerp__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_username = db.Column(db.String(20))
    account_email = db.Column(db.String(120))
    account_password = db.Column(db.String(60), nullable=False)
    account_site = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __rerp__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}', '{self.type}', '{self.date_added}')"