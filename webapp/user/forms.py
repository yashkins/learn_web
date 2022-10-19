from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length

from webapp.user.models import Users

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    remember_me = BooleanField('Запомнить меня', default=True, render_kw={"class": "form-check-input"})
    submit = SubmitField('Отправить!', render_kw={"class":"btn btn-primary"})

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField('Электронная почта', validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')], render_kw={"class": "form-control"})
    submit = SubmitField('Отправить!', render_kw={"class":"btn btn-primary"})

    def validate_username(self, username):
        count_user = Users.query.filter_by(username=username.data).count()
        if count_user:
            raise ValidationError("Пользователь с таким именем уже существует")

    def validate_email(self, email):
        count_user = Users.query.filter_by(email=email.data).count()
        if count_user:
            raise ValidationError('Пользователь с такой эл. почтой уже зарегистрирован')
            
class EditProfileForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class":"form-control"})
    email = StringField('Электронная почта', validators=[DataRequired(), Email()], render_kw={"class":"form-control"})
    about_me = TextAreaField('Обо мне', validators=[Length(min=0, max=140)], render_kw={"class":"form-control"})
    submit = SubmitField('Сохранить', render_kw={"class":"btn btn-primary"})

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm,self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        count_user = Users.query.filter(Users.username==username.data, Users.username.notin_([self.original_username])).count()
        if count_user:
            raise ValidationError("Пользователь с таким именем уже существует")

    def validate_email(self, email):
        count_user = Users.query.filter(Users.email==email.data, Users.email.notin_([self.original_email])).count()
        if count_user:
            raise ValidationError('Пользователь с такой эл. почтой уже зарегистрирован')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Укажите вашу электронную почту', validators=[DataRequired(), Email()], render_kw={'class':'form-control'})
    submit = SubmitField('Отправить', render_kw={'class':'btn btn-primary'})

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Введите новый пароль',validators=[DataRequired()],render_kw={'class':'form-control'})
    password2 = PasswordField('Повторите пароль',validators=[DataRequired(),EqualTo('password')],render_kw={'class':'form-control'})
    submit = SubmitField('Сохранить', render_kw={'class':'btn btn-primary'})

    