# -*- coding: utf-8 -*-
from datetime import datetime

from Apps.ext import db
from Apps.models.cms_models import BaseModel2


class HistoryData(BaseModel2):
    __tablename__ = 'historydatas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    devName = db.Column(db.String(100), nullable=False)
    devId = db.Column(db.String(30), nullable=False)
    dataPointName = db.Column(db.String(30), nullable=False)
    createTime = db.Column(db.DateTime,default=datetime.now)
    value = db.Column(db.Float)
    regGroup = db.Column(db.String(30), nullable=False)