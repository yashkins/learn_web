
from flask import Blueprint, Flask, render_template, flash, redirect, request, url_for
from flask_login import current_user, login_required, login_user, logout_user 
from webapp.mail import mail_for_reset_password
from webapp.db import db
from webapp.user.models import Users
from webapp.user.forms import EditProfileForm, LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from webapp.utils import get_redirect_target

blueprint = Blueprint('user', __name__, url_prefix='/user')

@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    title = 'Авторизация' 
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form = login_form)   

@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter(Users.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы успешно зашли на сайт')
            return redirect(get_redirect_target())

    flash('Неверное имя пользователя или пароль')
    return redirect(url_for('user.login'))

@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('news.index'))  

@blueprint.route('/registration')
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    title = 'Регистрация'
    registration_form = RegistrationForm()
    return render_template('user/registration.html', page_title=title, form=registration_form)

@blueprint.route('/process_reg', methods=['POST'] )
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = Users(username=form.username.data, email=form.email.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно прошли регистрацию')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash("Ошибка в поле {}: {}".format(getattr(form,field).label.text, error))

        return redirect(url_for('user.registration'))

@blueprint.route('/profile/<username>')
@login_required
def profile(username):
    user = Users.query.filter_by(username=username).first_or_404()
    title = 'Страница профиля'
    return render_template('user/profile.html', page_title=title, user=user)

@blueprint.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.email)
    title = 'Редактирование профиля'
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Ваши изменения сохранены')
        return redirect(url_for('user.profile', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('user/edit_profile.html', page_title=title, form=form)

@blueprint.route('/reset_password_request', methods=['GET','POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            mail_for_reset_password(user)
        flash('На адрес вашей электронной почты отправленна инструкция для смены пароля')
    title = 'Запрос на смену пароля'
    return render_template('user/reset_password_request.html', form=form, page_title=title)

@blueprint.route('/reset_passowrd/<token>', methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    user = Users.verifi_reset_passsword_token(token)
    if not user:
        flash('Некорретная или устаревшая ссылка. Попробуйте запросить новую ссылку')
        return redirect(url_for('user.reset_password_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Пароль успешно сохранен')
        return redirect(url_for('user.login'))
    title = 'Смена пароля'
    return render_template('user/reset_password.html', form=form, page_title=title)

