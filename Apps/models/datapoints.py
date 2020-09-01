# -*- coding: utf-8 -*-

from Apps.ext import db
from Apps.models.cms_models import BaseModel2
from datetime import datetime





class DataPoint(BaseModel2):
    __tablename__ = 'datapoints'
    dpName = db.Column(db.String(100), nullable=False)
    dpPosition = db.Column(db.String(30))
    type = db.Column(db.Boolean)
    dpValue = db.Column(db.Float)
    dpDesc = db.Column(db.Text)
    createTime = db.Column(db.DateTime,default=datetime.now)
    devId = db.Column(db.Integer, db.ForeignKey('devices.id'))