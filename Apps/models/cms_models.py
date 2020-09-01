# -*- coding: utf-8 -*-
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from Apps.ext import db

PERMISSION_NONE = 0
PERMISSION_COMMON = 1
SUPER_USER = 2


class BaseModel(db.Model):
    __abstract__ = True

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False


class BaseModel2(BaseModel):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class CMSUser(BaseModel2):
    __tablename__ = 'cms_user'

    username = db.Column(db.String(50), nullable=False, unique=True)
    _password = db.Column(db.String(100), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    is_super = db.Column(db.Boolean, default=False)
    permission = db.Column(db.Integer, default=PERMISSION_COMMON)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username):
        self.username = username

    @property
    def password(self):
        # return self._password
        raise Exception("cannot access")

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self._password, raw_password)
        return result

    def check_permission(self, permission):
        return self.is_super or permission & self.permission == permission
