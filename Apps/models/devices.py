# -*- coding: utf-8 -*-
from datetime import datetime
from Apps.ext import db
from Apps.models.cms_models import BaseModel2


class Device(BaseModel2):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    devName = db.Column(db.String(100),nullable=False)
    dpTotal = db.Column(db.Integer)
    dataTotal = db.Column(db.Integer)
    devPosition = db.Column(db.String(30))
    deviceId = db.Column(db.String(30),nullable=False)
    devDesc = db.Column(db.Text)
    gId = db.Column(db.Integer, db.ForeignKey('groups.id'))
    # gId = db.Column(db.Integer, db.ForeignKey('groups.id'))

