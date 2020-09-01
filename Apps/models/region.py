# -*- coding: utf-8 -*-
from datetime import datetime

from Apps.ext import db
from Apps.models.cms_models import BaseModel2


class Region(BaseModel2):
    __tablename__ = 'regions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    regName = db.Column(db.String(20), nullable=False)
    regPosition = db.Column(db.String(30))
    regLocation = db.Column(db.Text)
    regRange = db.Column(db.Integer)
    regDesc = db.Column(db.Text)