from flask import g, request
from flask_restful import Resource, fields, marshal
from Apps.apis.common.device_list.device_list_utils import devListHandle
from Apps.apis.common.user.user_utils import login_required
from config import DB_URI
from sqlalchemy import create_engine

eng = create_engine(DB_URI)
from Apps.apis.common.historydata.historydata_utils import timestamp_to_str

flag_fields = {'code': fields.Integer, 'msg': fields.String}

dl1_fields = {'id': fields.Integer,
              'devName': fields.String,
              'regName': fields.String,
              'status': fields.Integer,
              'gName': fields.String,
              'date': fields.DateTime(dt_format='iso8601'),
              'position': fields.List(fields.Float)}

DL1_fields = {'regName': fields.String,
              'groups': fields.List(fields.String),
              'devs': fields.List(fields.Nested(dl1_fields))}

devList1_fields = {'code': fields.Integer, 'data': fields.List(fields.Nested(DL1_fields))}

reg_fields = {'regName': fields.String,
              'groups': fields.List(fields.String),
              'devs': fields.List(fields.Nested(dl1_fields))}

groups_fields = {'name': fields.String,
                 'devsCount': fields.Integer}
devsCount_fields = {'total': fields.Integer,
                    'offline': fields.Integer,
                    'online': fields.Integer}
regi_fields = {'regName': fields.String,
               'groups': fields.List(fields.Nested(groups_fields)),
               'devsCount': fields.Nested(devsCount_fields)}
region_fields = {'code': fields.Integer, 'data': fields.List(fields.Nested(regi_fields))}


# 获取分区下的设备信息列表，当不传查询参数时默认返回所有分区的设备数据。
class devList1(Resource, devListHandle):
    @login_required
    def get(self):
        rank = g.user.rank
        if rank:
            data = marshal(self.getdevList1(), devList1_fields)
            return data


class region(Resource, devListHandle):
    @login_required
    def get(self):
        rank = g.user.rank
        if rank:
            data = marshal(self.getreg(), region_fields)
            return data


# post
class updateDevsInfo(Resource):
    def __init__(self):
        self.gname = []

    @login_required
    def post(self):
        regName = request.json.get("regName")
        gName = request.json.get("gName")
        devName = request.json.get("devName")
        date = request.json.get("date")
        position = request.json.get("position")
        id = request.json.get("id")
        from flask import g
        rank = g.user.rank
        if rank:
            date = timestamp_to_str(date)
            with eng.connect() as con:
                reg = con.execute("select*from regions where regName=" + "'" + regName + "'").fetchone()
                if reg:  # 判断是否存在这个区
                    gro = con.execute("select*from groups where g_reg=" + "'" + regName + "'").fetchall()
                    if gro:
                        for g in gro:
                            self.gname.append(g.gName)
                    if gName in self.gname:  # 判断输入的组是否存在于输入的区下
                        res = con.execute("update devices set devName=" + "'" + devName + "'" + ",devPosition=" + "'" +
                                          str(position) + "'" + ",device_g=" + "'" + gName + "'" + ",createTime=" + "'" + date + "'" + " where id=" + str(
                            id))
                        if res.rowcount:
                            return marshal({'code': 200, 'msg': 'ok'}, flag_fields)
                        else:
                            return marshal({'code': 2004, 'msg': 'Update failed'}, flag_fields)
                    else:
                        return marshal({'code': 1001, 'msg': 'Group not existent'}, flag_fields)
                else:
                    return marshal({'code': 1000, 'msg': 'Region not existent'}, flag_fields)


class deleteDev(Resource):
    @login_required
    def post(self):
        id = request.json.get("id")
        rank = g.user.rank
        if rank:
            with eng.connect() as con:
                res = con.execute("delete from devices where id = " + str(id))
                if res.rowcount:
                    return marshal({'code': 200, 'msg': 'ok'}, flag_fields)
                else:
                    return marshal({'code': 2005, 'msg': 'Delete failed'}, flag_fields)
