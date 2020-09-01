from datetime import datetime

from flask import g, request
from flask_restful import Resource, fields, marshal
from Apps.apis.common.dp.dp_utils import dataPointsListHandle
from Apps.apis.common.user.user_utils import login_required
from config import DB_URI
from sqlalchemy import create_engine
eng = create_engine(DB_URI)

flag_fields = {'code':fields.Integer,
               'msg':fields.String}

dp1_fields = {'dpName':fields.String,
              'desc':fields.String,
              'position':fields.List(fields.Float),
              'dataTotal':fields.Integer,
              'type':fields.Integer}

D1_fields = {'devName':fields.String,
             'desc':fields.String,
             'position':fields.List(fields.Float),
             'dataPoints':fields.List(fields.Nested(dp1_fields)),
             'dpTotal':fields.Integer,
             'dataTotal':fields.Integer}

re_fields = {'regName':fields.String,
             'devs':fields.List(fields.Nested(D1_fields))}
reg_fields = {'code':fields.Integer,'data':fields.List(fields.Nested(re_fields))}



class regions(Resource,dataPointsListHandle):
    @login_required
    def get(self):
        rank = g.user.rank
        if rank:
            data = marshal(self.getreg(),reg_fields)
            return data
#post
class delDev(Resource):
    @login_required
    def post(self):
        from flask import g
        regName = request.json.get('regName')
        devName = request.json.get('devName')
        rank = g.user.rank
        if rank:
            with eng.connect() as con:
                gro = con.execute("select * from groups where g_reg=" + "'" + regName + "'").fetchall()
                if gro:
                    for g in gro:
                        res = con.execute("delete from devices where devName = "+"'"+devName+"'"+" and device_g="+"'"+g.gName+"'")
                        if res:
                            return marshal({'code':200,'msg':'ok'},flag_fields)


class updateDev(Resource):
    @login_required
    def post(self):
        regName = request.json.get('regName')
        dev = request.json.get('dev')
        from flask import g
        rank = g.user.rank
        if rank:
            with eng.connect() as con:
                gro = con.execute("select * from groups where g_reg=" + "'" + regName + "'").fetchall()
                if gro:
                    for g in gro:
                        res = con.execute("update devices set devPosition=" + "'" + str(dev['position'][0])+","+str(dev['position'][1])+ "'" + ",devDesc=" + "'" +
                                              dev['desc'] + "'" + " where devName=" + "'"+dev['devName']+"' and device_g="+"'"+g.gName+"'")
                        if res:
                            return marshal({'code':200,'msg':'ok'},flag_fields)

class createDev(Resource):
    @login_required
    def post(self):
        regName = request.json.get('regName')
        dev = request.json.get('dev')
        rank = g.user.rank
        if rank:
            with eng.connect() as con:
                gro = con.execute("select * from groups where g_reg=" + "'" + regName + "'").fetchone()
                if gro:
                    res = con.execute(
                        "insert into devices (devName,devPosition,devDesc,device_g,createTime) values (" +
                        "'" + dev['devName'] + "'" + "," + "'" + str(dev['position']) + "'" + "," + "'" + dev['desc'] + "'" + "," + "'" + gro.gName + "'"+","+"'"+str(datetime.now())+"'"+")")
                    if res:
                        return marshal({'code':200,'msg':'ok'},flag_fields)

class delDp(Resource):
    @login_required
    def post(self):
        regName = request.json.get('regName')
        devName = request.json.get('devName')
        dpName = request.json.get('dpName')
        from flask import g
        rank = g.user.rank
        if rank:
            with eng.connect() as con:
                gro = con.execute("select * from groups where g_reg=" + "'" + regName + "'").fetchall()
                if gro:
                    for g in gro:
                        dev = con.execute("select * from devices where device_g=" + "'" + g.gName + "'").fetchall()
                        if dev:
                            for d in dev:
                                if devName==d.devName:
                                    res = con.execute("delete from datapoints where dpName=" + "'" + dpName + "'" + " and dp_dev=" + "'" + devName + "'")
                                    if res:
                                        return marshal({'code':200,'msg':'ok'},flag_fields)

class createDp(Resource):
    @login_required
    def post(self):
        dpName = request.json.get('dpName')
        position = request.json.get('position')
        type = request.json.get('type')
        desc = request.json.get('desc')
        regName = request.json.get("regName")
        devName = request.json.get("devName")
        # from flask import g
        rank = g.user.rank
        if rank:
            with eng.connect() as con:
                res = con.execute(
                    "insert into datapoints (dpName,dpPosition,type,dpDesc,dp_dev) values (" +
                    "'" + dpName + "'" + "," + "'" + str(position) +"'"+ "," + str(type)+ "," + "'" + desc + "'" + "," + "'" + devName + "'" + ")")
                if res:
                    return marshal({'code': 200, 'msg': 'ok'}, flag_fields)

class updateDp(Resource):
    @login_required
    def post(self):
        dpName = request.json.get('dpName')
        position = request.json.get('position')
        type = request.json.get('type')
        desc = request.json.get('desc')
        regName = request.json.get("regName")
        devName = request.json.get("devName")
        from flask import g
        rank = g.user.rank
        if rank:
            with eng.connect() as con:
                gro = con.execute("select * from groups where g_reg=" + "'" + regName + "'").fetchall()
                if gro:
                    for g in gro:
                        dev = con.execute("select * from devices where device_g=" + "'" + g.gName + "'").fetchall()
                        if dev:
                            for d in dev:
                                if devName == d.devName:
                                    res = con.execute("update datapoints set dpPosition=" + "'" + str(position) + "'" + ",type=" + "'" +
                                                      str(type) + "'" + ",dpDesc=" + "'" + desc + "'" + " where dpName=" + "'"+dpName+"' and dp_dev="+"'"+devName+"'")
                                    if res:
                                        return marshal({'code':200,'msg':'ok'},flag_fields)



