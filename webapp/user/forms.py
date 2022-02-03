from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

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
            