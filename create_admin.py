from getpass import getpass
import sys

from webapp import create_app
from webapp.db import db
from webapp.user.models import Users

app = create_app()

with app.app_context():
    username = input('Введите имя')

    if Users.query.filter(Users.username == username).count():
        print('Пользователь с таким имен уже существует')
        sys.exit(0)
    
    password = getpass('Введите пароль')
    password2 = getpass('Повторите пароль')
    
    if not password == password2:
        print('Пароли неодинаковые')
        sys.exit(0)

    new_user = Users(username=username, role="admin")
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    print('Создан пользователь с id={}'.format(new_user.id))
