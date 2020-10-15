from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField, DateField, validators, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from passwordmanager.models import User



class RegistrationForm(FlaskForm):
    first_name = StringField('სახელი',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა'), Length(min=2, max=20, message='ველის სიგრძე უნდა იყოს 2-20 სიმბოლომდე სიგრძის')])
    last_name = StringField('გვარი',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა'), Length(min=4, max=25, message='ველის სიგრძე უნდა იყოს 2-25 სიმბოლომდე სიგრძის')])
    email = StringField('ელ-ფოსტა',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა'), Email()])
    password = PasswordField('პაროლი',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა'),])
    confirm_password = PasswordField('გაიმეორეთ პაროლი',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა'), EqualTo('password', message='ველი უნდა ემთხვეოდეს თქვენს პაროლს')])
    submit = SubmitField('რეგისტრაცია')

    def validate_email(self, email):
            if User:
                user = User.query.filter_by(email=email.data).first()
                if user:
                    raise ValidationError('მსგავსი ელ-ფოსტა უკვე გამოყენებულია')
            
            
    class Meta:
        def render_field(self, field, render_kw):
            render_kw.setdefault('required', False)
            return super().render_field(field, render_kw)  

class LoginForm(FlaskForm):
    email = StringField('ელ-ფოსტა',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა'), Email()])
    password = PasswordField('პაროლი',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა')])
    remember = BooleanField('დამახსოვრება')
    submit = SubmitField('შესვლა')

    class Meta:
            def render_field(self, field, render_kw):
                render_kw.setdefault('required', False)
                return super().render_field(field, render_kw)


class AddAccount(FlaskForm):
    account_username = StringField('მომხარებლის სახელი',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა')])
    account_email = StringField('ელ-ფოსტა',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა'), Email()])
    account_password = StringField('პაროლი',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა')])
    account_site = StringField('საიტის/აპლიკაციის სახელი',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა')])
    submit = SubmitField('დამატება')

    class Meta:
            def render_field(self, field, render_kw):
                render_kw.setdefault('required', False)
                return super().render_field(field, render_kw)


class GeneratePassword(FlaskForm):
    password_rng = IntegerField('ზომა')
    submit = SubmitField('დააგენერირე')
    