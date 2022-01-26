from flask import Blueprint, Flask, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user 
from webapp.user.models import Users
from webapp.user.forms import LoginForm

blueprint = Blueprint('user', __name__, url_prefix='/user')

@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = 'Авторизация' 
    login_form = LoginForm()
    return render_template('login.html', page_title=title, form = login_form)   

@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter(Users.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы успешно зашли на сайт')
            return redirect(url_for('news.index'))

    flash('Неверное имя пользователя или пароль')
    return redirect(url_for('user.login'))

@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('news.index'))  