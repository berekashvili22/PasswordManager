from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField, DateField, validators, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from passwordmanager.models import User


class RegistrationForm(FlaskForm):
    first_name = StringField('სახელი',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა'),
                                 Length(min=2, max=20, message='ველის სიგრძე უნდა იყოს 2-20 სიმბოლომდე სიგრძის')])
    last_name = StringField('გვარი',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა'),
                                 Length(min=4, max=25, message='ველის სიგრძე უნდა იყოს 2-25 სიმბოლომდე სიგრძის')])
    email = StringField('ელ-ფოსტა',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა'),
                                 Email()])
    password = PasswordField('პაროლი',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა'),])
    confirm_password = PasswordField('გაიმეორეთ პაროლი',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა'),
                                 EqualTo('password', message='ველი უნდა ემთხვეოდეს თქვენს პაროლს')])
    submit = SubmitField('დარეგისტრირდი')

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
    username = StringField('მომხარებლის სახელი',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა')])
    email = StringField('ელ-ფოსტა',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა'), Email()])
    password = StringField('პაროლი',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა')])
    site = StringField('საიტის/აპლიკაციის სახელი',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა')])
    submit = SubmitField('დამატება')

    class Meta:
            def render_field(self, field, render_kw):
                render_kw.setdefault('required', False)
                return super().render_field(field, render_kw)


class GeneratePassword(FlaskForm):
    password_rng = IntegerField('ზომა')
    symbols = BooleanField('სიმბოლოები(@#$%..)')
    numbers = BooleanField('ციფრები(123456..)')
    uppercase = BooleanField('დიდი ასოები(ABCDE..)')
    submit = SubmitField('დააგენერირე')


class UpdateAccount(FlaskForm):
    username = StringField('მომხარებლის სახელი',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა')])
    email = StringField('ელ-ფოსტა',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა'), Email()])
    password = StringField('პაროლი',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა')])
    site = StringField('საიტის/აპლიკაციის სახელი',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა')])
    submit = SubmitField('დამატება')

    class Meta:
            def render_field(self, field, render_kw):
                render_kw.setdefault('required', False)
                return super().render_field(field, render_kw)
    


class UpdateProfile(FlaskForm):
    first_name = StringField('სახელი',
         validators=[DataRequired(message='ველის შევსება სავალდებულოა'), Length(min=2, max=20)])
    last_name = StringField('გვარი',
         validators=[DataRequired(message='ველის შევსება სავალდებულოა'), Length(min=4, max=20)])
    email = StringField('ელ. ფოსტა',
         validators=[DataRequired(message='ველის შევსება სავალდებულოა'), Email(message='ელ-ფოსტა არასწორია')])
    submit = SubmitField('განახლება')
    
    def validate_first_name(self, first_name):
         if first_name.data != current_user.first_name:
               pass     
                            
    def validate_email(self, email):
         if email.data != current_user.email:
               user = User.query.filter_by(email=email.data).first()       
               if user:
                    raise ValidationError('მსგავსი ელ. ფოსტა უკვე გამოყენებულია')

    class Meta:
        def render_field(self, field, render_kw):
            render_kw.setdefault('required', False)
            return super().render_field(field, render_kw)  

class RequestResetform(FlaskForm):
    email = StringField('ელ. ფოსტა',
         validators=[DataRequired(message='ველის შევსება სავალდებულოა'), Email(message='ელ-ფოსტა არასწორია')])
    submit = SubmitField('გაგზავნა')

    def validate_email(self, email):
            if User:
                user = User.query.filter_by(email=email.data).first()
                if user is None:
                    raise ValidationError('მსგავსი ელ. ფოსტით ექაუნთი ვერ მოიძებნა')
    

class ResetPassworForm(FlaskForm):
    password = PasswordField('პაროლი',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა'),])
    confirm_password = PasswordField('გაიმეორეთ პაროლი',
                                validators=[DataRequired(message='ველის შევსება სავალდებულოა'),
                                 EqualTo('password', message='ველი უნდა ემთხვეოდეს თქვენს პაროლს')])
    submit = SubmitField('შეცვლა')