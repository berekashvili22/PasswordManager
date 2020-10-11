from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    first_name = StringField('სახელი',
                                validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('გვარი',
                                validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('ელ-ფოსტა',
                                validators=[DataRequired(), Email()])
    password = PasswordField('პაროლი',
                                validators=[DataRequired(),])
    confirm_password = PasswordField('გაიმეორეთ პაროლი',
                                validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('რეგისტრაცია')

class LoginForm(FlaskForm):
    email = StringField('ელ-ფოსტა',
                                validators=[DataRequired(), Email()])
    password = PasswordField('პაროლი',
                                validators=[DataRequired(),])
    remember = BooleanField('დამახსოვრება')
    submit = SubmitField('შესვლა')

