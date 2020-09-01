# -*- coding: utf-8 -*-
from datetime import datetime

from Apps.ext import db
from Apps.models.cms_models import BaseModel2


class Plot(BaseModel2):
    __tablename__ = 'plots'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bounds = db.Column(db.String(60), nullable=False)
    # exterior = db.Column(db.String(30))
    plotsName = db.Column(db.String(100))
    lotRange = db.Column(db.Integer)
    layerUrl = db.Column(db.String(100))
    plotsDesc = db.Column(db.Text)
    regId = db.Column(db.Integer, db.ForeignKey('regions.id'))
