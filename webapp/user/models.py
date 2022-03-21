from datetime import datetime
from flask_login import UserMixin
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from webapp.db import db

class Users(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)
    email = db.Column(db.String(50)) 
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)  

    def avatar(self, size):
        mail = self.email
        digest = md5(mail.lower().encode('utf-8')).hexdigest()
        return 'https//www.qravatar.com/avatar/{}?d=mp&s={}'.format(digest,size)

    @property
    def is_admin(self):
        return self.role == "admin"   

    def __repr__(self) -> str:
        return "<User {}>".format(self.username)