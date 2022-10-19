
from datetime import datetime
from flask import Flask
from flask_login import LoginManager, current_user 
from flask_migrate import Migrate
from flask_mail import Mail
from webapp.db import db
from webapp.admin.views import blueprint as admin_blueprint
from webapp.error.wiews import blueprint as error_blueprint
from webapp.news.views import blueprint as news_blueprint
from webapp.user.views import blueprint as user_blueprint

from webapp.user.models import Users



def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    mail = Mail(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.login"
    app.register_blueprint(news_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(error_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(user_id)
    
    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()


    return app


