# -*- coding: utf-8 -*-
from flask import g
from flask_restful import reqparse, Resource, fields,marshal
from Apps.apis.common.amap_about.amap_about_utils import amapAboutHandle
from Apps.apis.common.user.user_utils import login_required

parser = reqparse.RequestParser()

dp_fields = {'dataTotal':fields.Integer,
             'desc':fields.String,
             'dpName':fields.String,
             'position':fields.List(fields.Float),
             'type':fields.Integer}
dev_fields = {'dataPoints':fields.List(fields.Nested(dp_fields)),
              'dataTotal':fields.Integer,
              'desc':fields.String,
              'devName':fields.String,
              'dpTotal':fields.Integer,
              'position':fields.List(fields.Float),
              }
gro_fields = {'desc':fields.String,
              'devs':fields.List(fields.Nested(dev_fields)),
              'devsTotal':fields.Integer,
              'gName':fields.String,
              'position':fields.List(fields.Float)}
plot_fields = {'bounds':fields.List(fields.Float),
               'desc':fields.String,
               'exterior':fields.List(fields.List(fields.Float)),
               'layerUrl':fields.String,
               'plotsRange':fields.Integer,
               'plotName':fields.String}

reg_fields = {'desc':fields.String,
              'groups':fields.List(fields.Nested(gro_fields)),
              'location':fields.String,
              'plots':fields.List(fields.Nested(plot_fields)),
              'position':fields.List(fields.Float),
              'regName':fields.String,
              'regRange':fields.Integer}

data_fields = {'code':fields.Integer,'data':fields.List(fields.Nested(reg_fields))}



class amapAboutData(Resource,amapAboutHandle):
    @login_required
    def get(self):
        rank = g.user.rank
        if rank:
            data = marshal(self.getdata(),data_fields)
            return data

    def post(self):
        return "请求方法错误"


