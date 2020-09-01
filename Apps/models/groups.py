# -*- coding: utf-8 -*-
from Apps.ext import db
from Apps.models.cms_models import BaseModel2


class Group(BaseModel2):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    devsTotal = db.Column(db.Integer)
    gName = db.Column(db.String(100),nullable=False)
    gPosition = db.Column(db.String(30),nullable=False)
    groupId = db.Column(db.String(30))
    gDesc = db.Column(db.Text)
    plotsId = db.Column(db.Integer, db.ForeignKey('plots.id'))
