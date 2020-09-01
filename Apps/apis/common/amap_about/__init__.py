# -*- coding: utf-8 -*-
from flask_restful import Api

from Apps.apis.common.amap_about.amapAbout_api import amapAboutData

amapAbout_api = Api(prefix="/cms")

amapAbout_api.add_resource(amapAboutData, "/amap_aboutApi/")

