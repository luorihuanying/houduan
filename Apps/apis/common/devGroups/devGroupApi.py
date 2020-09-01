from flask import g, request
from flask_restful import Resource, fields, marshal
from Apps.apis.common.devGroups.devGroups_utils import devGroupHandle
from Apps.apis.common.historydata.historydata_utils import timestamp_to_str
from Apps.apis.common.user.user_utils import login_required
from config import DB_URI
from sqlalchemy import create_engine

eng = create_engine(DB_URI)

flag_fields = {'code': fields.Integer, "msg": fields.String}

gro1_fields = {'gName': fields.String,
               'date': fields.DateTime(dt_format='iso8601'),
               'devsTotal': fields.Integer,
               'desc': fields.String,
               'position': fields.List(fields.Float)}

re_fields = {'regName': fields.String,
             'date': fields.DateTime(dt_format='iso8601'),
             'groupInfo': fields.List(fields.Nested(gro1_fields)),
             'layerUrl': fields.String,
             'desc': fields.String,
             'localtion': fields.String,
             'regRange': fields.Integer,
             'position': fields.List(fields.Float),
             'polotsTotal': fields.Integer}

reg_fields = {'code': fields.Integer, 'data': fields.List(fields.Nested(re_fields))}


class reg(Resource, devGroupHandle):
    @login_required
    def get(self):
        rank = g.user.rank
        if rank:
            data = marshal(self.getreg(), reg_fields)
            return data


# post
class createRegInfo(Resource):
    @login_required
    def post(self):
        regName = request.json.get("regName")
        position = request.json.get("position")
        desc = request.json.get("desc")
        localtion = request.json.get("localtion")
        layerUrl = request.json.get("layerUrl")
        date = request.json.get("date")
        rank = g.user.rank
        if rank:
            date = timestamp_to_str(date)
            with eng.connect() as con:
                res = con.execute(
                    "insert into regions (regName,regPosition,regLocation,regDesc,createTime,layerUrl) values ("
                    + "'" + regName + "'" + "," + "'" + str(
                        position) + "'" + "," + "'" + localtion + "'" + "," + "'" + desc + "'" + "," + "'" + date + "'" + ",'" + layerUrl + "'" + ")")
                if res.rowcount:
                    return marshal({'code': 200, 'msg': 'ok'}, flag_fields)
                else:
                    return marshal({'code': 2003, 'msg': 'Insert failed'}, flag_fields)


class updateRegInfo(Resource):
    @login_required
    def post(self):
        position = request.json.get("position")
        regName = request.json.get("regName")
        desc = request.json.get("desc")
        localtion = request.json.get("localtion")
        layerUrl = request.json.get("layerUrl")
        date = request.json.get("date")
        rank = g.user.rank
        if rank:
            date = timestamp_to_str(date)
            with eng.connect() as con:
                res = con.execute("update regions set regPosition=" + "'" + str(position) + "'" + ",regLocation="
                                  + "'" + localtion + "'" + ",regDesc=" + "'" + desc + "'" + ",createTime=" + "'" + date + "'" + ",layerUrl=" + "'" + layerUrl + "'" + " where regName=" + "'" + regName + "'")
                if res.rowcount:
                    return marshal({'code': 200, 'msg': 'ok'}, flag_fields)
                else:
                    return marshal({'code': 2004, 'msg': 'Update failed'}, flag_fields)


class delRegInfo(Resource):
    @login_required
    def post(self):
        regName = request.json.get("regName")
        rank = g.user.rank
        if rank:
            with eng.connect() as con:
                res = con.execute("delete from regions where regName = " + "'" + regName + "'")
                if res.rowcount:
                    return marshal({'code': 200, 'msg': 'ok'}, flag_fields)
                else:
                    return marshal({'code': 2005, 'msg': 'Delete failed'}, flag_fields)


class createGroupInfo(Resource):
    @login_required
    def post(self):
        regName = request.json.get("regName")
        gName = request.json.get("gName")
        date = request.json.get("date")
        position = request.json.get("position")
        desc = request.json.get("desc")
        rank = g.user.rank
        if rank:
            date = timestamp_to_str(int(date))
            with eng.connect() as con:
                reg = con.execute("select * from regions where regName = " + "'" + regName + "'").fetchone()
                if reg:
                    gro = con.execute("insert into groups (g_reg,gName,createTime,gPosition,gDesc) values ("
                                      + "'" + regName + "'" + "," + "'" + gName + "'" + "," + "'" + date + "'" + "," + "'" + str(
                        position) + "'" + "," + "'" + desc + "'" + ")")
                    if gro.rowcount:
                        return marshal({"code": 200, "msg": "ok"}, flag_fields)
                    else:
                        return marshal({"code": 2003, "msg": "Insert failed"}, flag_fields)
                else:
                    return marshal({"code": 1000, "msg": "Region does not exist"}, flag_fields)


class updataGroupInfo(Resource):
    @login_required
    def post(self):
        gName = request.json.get("gName")
        regName = request.json.get("regName")
        desc = request.json.get("desc")
        date = request.json.get("date")
        position = request.json.get("position")
        rank = g.user.rank
        if rank:
            date = timestamp_to_str(date)
            with eng.connect() as con:
                res = con.execute("update groups set gDesc=" + "'" + desc + "'" + ",gPosition="
                                  + "'" + str(
                    position) + "'" + ",createTime=" + "'" + date + "'" + " where gName=" + "'" + gName + "' and g_reg=" + "'" + regName + "'")
                if res.rowcount:
                    return marshal({'code': 200, 'msg': 'ok'}, flag_fields)
                else:
                    return marshal({'code': 2004, 'msg': 'Update failed'}, flag_fields)


class delGroupInfo(Resource):
    @login_required
    def post(self):
        regName = request.json.get("regName")
        gName = request.json.get("gName")
        rank = g.user.rank
        if rank:
            with eng.connect() as con:
                res = con.execute(
                    "delete from groups where gName = " + "'" + gName + "' and g_reg=" + "'" + regName + "'")
                if res.rowcount:
                    return marshal({'code': 200, 'msg': 'ok'}, flag_fields)
                else:
                    return marshal({'code': 2005, 'msg': 'Delete failed'}, flag_fields)
