# -*- coding: utf-8 -*-
from flask import request
from flask_restful import Resource, fields, marshal
from Apps.apis.common.historydata.historydata_utils import histotydataHandle
from Apps.apis.common.user.user_utils import login_required, g
from Apps.models import HistoryData
from Apps.apis.common.historydata.historydata_utils import timestamp_to_str
from config import DB_URI
from sqlalchemy import create_engine

eng = create_engine(DB_URI)


historydata_fields = {
    "id": fields.Integer,
    "devName": fields.String,
    "alarm": fields.Integer,
    "dataPointName": fields.String,
    "type": fields.Integer,
    "date": fields.DateTime(dt_format='iso8601'),
    "groupName":fields.String,
    "value": fields.String
}

fie = {'regionName': fields.String,
       'groupList': fields.List(fields.String)}

regionGroupList_fields = {'code': fields.Integer, 'data': fields.List(fields.Nested(fie))}
devLi_fields = {"devList":fields.List(fields.String)}
devList_fields = {'code': fields.Integer, 'data': fields.Nested(devLi_fields)}

dpList_fields = {'dataPointList':fields.List(fields.String)}
dataPointList_fields = {'code': fields.Integer, 'data': fields.Nested(dpList_fields)}

historyDataList = {"historyDataList":fields.List(fields.Nested(historydata_fields)),'total':fields.Integer}

histotydataList_fields = {'code': fields.Integer, 'data': fields.Nested(historyDataList)}

#post成功
success_Flag = {'code':fields.Integer,'msg':fields.String}


class historyData(Resource, histotydataHandle):
    @login_required
    def post(self):
        """
        获取历史数据
        """
        rank = g.user.rank
        if rank:
            data = self.time_filter()
            data = marshal(data, histotydataList_fields)
            return data
        else:
            return marshal({'code':5000,'msg':'No access'})

    def get(self):
        data = marshal({'code': '308', 'data': []}, histotydataList_fields)
        return data


class regionGroupList(Resource, histotydataHandle):
    @login_required
    def get(self):
        """
        获取区和组数据
        """
        rank = g.user.rank
        if rank:
            data = marshal(self.get_reg_g_data(), regionGroupList_fields)
            return data

    def post(self):
        data = marshal({'code': '308', 'data': []}, regionGroupList_fields)
        return data


class devList(Resource, histotydataHandle):
    @login_required
    def get(self):
        # 获取设备列表
        rank = g.user.rank
        if rank:
            data = marshal(self.get_devlist(), devList_fields)
            return data

    def post(self):
        data = marshal({'code': '308', 'data': []}, devList_fields)
        return data


class dataPointList(Resource, histotydataHandle):
    @login_required
    def get(self):
        # 获取数据点列表
        rank = g.user.rank
        if rank:
            data = self.get_dataPointList()
            data = marshal(data, dataPointList_fields)
            return data

    def post(self):
        data = marshal({'code': '308', 'data': []}, dataPointList_fields)
        return data


class createNewhistoryData(Resource):
    @login_required
    def post(self):
        groupName = request.json.get("groupName")
        devName = request.json.get("devName")
        date = request.json.get("date")
        dataPointName = request.json.get("dataPointName")
        value = request.json.get("value")
        alarm = request.json.get("alarm")
        rank = g.user.rank
        if rank:
            try:
                date = timestamp_to_str(date)
                with eng.connect() as con:
                    res = con.execute(
                        "insert into historydatas (devName,dataPointName,createTime,value,groupName,alarm) values (" + "'"
                        + devName + "'" + "," + "'" + dataPointName + "'" + "," + "'" + date + "'" + "," + str(
                            value) + "," + "'" + groupName + "'" + "," + str(alarm) + ")")
                    if res:
                        return marshal({'code':'200','msg':'ok'},success_Flag)
                    else:
                        return marshal({'code': '2003', 'msg': 'insert error'}, success_Flag)
            except Exception as e:
                return {"code": "500", "msg": "error"}

    def get(self):
        data = marshal({'code': '308', 'msg': "error"}, success_Flag)
        return data


class deleteOneData(Resource):
    @login_required
    def post(self):
        id = request.json.get("id")
        groupName = request.json.get("groupName")
        devName = request.json.get("devName")
        date = request.json.get("date")
        dataPointName = request.json.get("dataPointName")
        value = request.json.get("value")
        alarm = request.json.get("alarm")
        rank = g.user.rank
        with eng.connect() as con:
            if rank:
                res = con.execute("select * from historydatas where id = " + str(id)).fetchall()
                if len(res):
                    con.execute("delete from historydatas where id = " + str(id))
                    return marshal({'code':200,'msg':'ok'},success_Flag)
                else:
                    return marshal({'code': 2007, 'msg': 'Record does not exist'}, success_Flag)


class changeAlarmStatus(Resource):
    @login_required
    def post(self):
        id = request.json.get("id")
        groupName = request.json.get("groupName")
        devName = request.json.get("devName")
        date = request.json.get("date")
        dataPointName = request.json.get("dataPointName")
        value = request.json.get("value")
        alarm = request.json.get("alarm")
        rank = g.user.rank
        if rank:
            with eng.connect() as con:
                res = con.execute("select * from historydatas where id = " + str(id)).fetchall()
                if len(res):
                    con.execute("update historydatas set alarm = " + str(not res[0].alarm) + " where id =" + str(id))
                    return marshal({'code':200,'msg':'ok'},success_Flag)
                else:
                    return marshal({'code': 2007, 'msg': 'Record does not exist'}, success_Flag)


class updateData(Resource):
    @login_required
    def post(self):
        id = request.json.get("id")
        groupName = request.json.get("groupName")
        devName = request.json.get("devName")
        date = request.json.get("date")
        dataPointName = request.json.get("dataPointName")
        value = request.json.get("value")
        alarm = request.json.get("alarm")
        rank = g.user.rank
        if rank:
            date = timestamp_to_str(date)
            with eng.connect() as con:
                res = con.execute("select * from historydatas where id = " + str(id)).fetchall()
                if len(res):
                    con.execute("update historydatas set devName="+"'"+devName+"'"+",dataPointName="
                                      +"'"+dataPointName+"'"+",createTime="+"'"+date+"'"+",value="+str(value)+",groupName="+"'"+groupName+"'"+",alarm="+str(alarm)+" where id="+str(id))
                    return marshal({'code':200,'msg':'ok'},success_Flag)
                else:
                    return marshal({'code': 2007, 'msg': 'Record does not exist'}, success_Flag)
