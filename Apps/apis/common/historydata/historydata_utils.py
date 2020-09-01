# -*- coding: utf-8 -*-
from flask import request
from flask_restful import reqparse

from config import DB_URI
from sqlalchemy import create_engine
import time

eng = create_engine(DB_URI)

#获取历史记录
parser = reqparse.RequestParser()
parser.add_argument("groupName",type=str)
parser.add_argument("devName",type=str)
parser.add_argument("dataPoints",type=list)
parser.add_argument("page",type=int)
parser.add_argument("limit",type=int)
parser.add_argument("startTime",type=int)
parser.add_argument("endTime",type=int)
#根据设备组名获取其设备列表
# parser.add_argument("groupName",type=str)


def timestamp_to_str(timestamp=None, format='%Y-%m-%d %H:%M:%S'):
    if timestamp:
        timestamp = timestamp/1000
        time_tuple = time.localtime(timestamp)  # 把时间戳转换成时间元祖
        result = time.strftime(format, time_tuple)  # 把时间元祖转换成格式化好的时间
        return result
    else:
        return time.strptime(format)

def dpList_conver(dp):
    dp1 = []
    dp2 = []
    for i in dp.split(','):
        dp1.append(i)
    for j in dp1:
        j = j.replace(' ', '')
        j = j.replace('[', '')
        j = j.replace(']', '')
        dp2.append(j)
    return dp2


class histotydataHandle():
    def __init__(self):
        self.conditions = []
        self.groupList1 = []
        self.groupList = []
        self.devList = []
        self.dataPointList = []
        self.code = ''
        self.dpName = []
        self.dp = [] #用来存传入的数据点

    # history-data.js
    def time_filter(self, **kwargs):
        args = parser.parse_args()
        groupName = args.get("groupName")
        devName = args.get("devName")
        dataPoints = request.json.get("dataPoints")
        page = args.get("page")
        limit = args.get("limit")
        startTime = args.get("startTime")
        endTime = args.get("endTime")
        print(groupName,devName,dataPoints,page,limit,startTime,endTime)
        try:
            if groupName==None and devName==None and dataPoints==None and page==None and limit==None and startTime==None and endTime==None:
                with eng.connect() as con:
                    res = con.execute("select*from historydatas")
                    for row in res:
                        data = {"id": row.id,
                                "devName": row.devName,
                                "alarm": row.alarm,
                                "dataPointName": row.dataPointName,
                                "type": row.type,
                                "date": row.createTime,
                                "groupName":row.groupName,
                                "value": row.value}
                        self.conditions.append(data)
                    data = {"code": "200", "data": {"historyDataList":self.conditions,'total':len(self.conditions)}}
                    return data
            else:
                page = page - 1
                self.dp = dataPoints
                startTime = timestamp_to_str(startTime)
                endTime = timestamp_to_str(endTime)
                with eng.connect() as con:
                    dev = con.execute("select*from devices where device_g = " + "'" + groupName + "'").fetchall()
                    if dev:
                        for d in dev:
                            if d.devName == devName:  # 如果传进来的设备名在数据库存在
                                dp = con.execute(
                                    "select*from datapoints where dp_dev = " + "'" + d.devName + "'" + " group by dpName").fetchall()
                                if dp:
                                    for DP in dp:
                                        self.dpName.append(DP.dpName)
                                    for D in self.dp:
                                        if D in self.dpName:  # 如果传进来的数据点中在数据库存在
                                            history = con.execute(
                                                "select*from historydatas where dataPointName = " + "'" + D + "'" +
                                                " and createTime between " + "'" + startTime + "'" + " and " + "'" + endTime + "'").fetchall()
                                            if history:
                                                for h in history:
                                                    data = {"id": h.id,
                                                            "devName": h.devName,
                                                            "alarm": h.alarm,
                                                            "dataPointName": h.dataPointName,
                                                            "type": h.type,
                                                            "date": h.createTime,
                                                            "groupName":h.groupName,
                                                            "value": h.value}
                                                    self.conditions.append(data)
                                            else:
                                                self.conditions = []
                                else:
                                    self.conditions = []
                    else:
                        self.conditions = []
                if len(self.conditions) <= limit:
                    data = {"code": 200, "data": {"historyDataList":self.conditions,'total':len(self.conditions)}}

                elif len(self.conditions) > limit and page == 0:
                    data = {"code": 200, "data": {"historyDataList":self.conditions[0:limit],'total':len(self.conditions[0:limit])}}
                else:
                    if limit * page <= len(self.conditions):
                        data = {"code": 200, "data": {"historyDataList":self.conditions[limit * (page - 1):limit * page],'total':len(self.conditions[limit * (page - 1):limit * page])}}
                    else:
                        if len(self.conditions) > limit * (page - 1) and len(self.conditions) < limit * page:
                            data = {"code": 200, "data": {"historyDataList":self.conditions[limit * (page - 1):],'total':len(self.conditions[limit * (page - 1):])}}
                        else:
                            data = {"code": 2001, "data": []}
                return data
        except Exception as e:
            print(e)
            return {"code": 500, "data": []}


    def get_reg_g_data(self):
        try:
            with eng.connect() as con:
                reg = con.execute("select*from regions").fetchall()
                for r in reg:
                    regionName = r.regName
                    gro = con.execute("select*from groups where g_reg = " + "'" + r.regName + "'").fetchall()
                    if gro:
                        for g in gro:
                            rg = g.gName
                            self.groupList1.append(rg)
                            data = {"regionName": regionName,
                                    "groupList": self.groupList1}
                        self.groupList.append(data)
                    else:
                        data = {"regionName": regionName,
                                "groupList": []}
                        self.groupList.append(data)
                data = {'code': 200, 'data': self.groupList}
                return data
        except Exception as e:
            return {"code": "500", "data": []}


    def get_devlist(self):
        args = parser.parse_args()
        groupName = args.get("groupName")
        try:
            if groupName!=None:
                with eng.connect() as con:
                    res = con.execute("select*from devices where device_g = "+"'"+groupName+"'").fetchall()
                    for row in res:
                        self.devList.append(row.devName)
                    data = {'code': 200, 'data': {"devList":self.devList}}
            else:
                data = {'code': 2002, 'data':[]}
            return data
        except Exception as e:
            return {"code": "500", "data": []}


    def get_dataPointList(self):
        args = parser.parse_args()
        devName = args.get("devName")
        try:
            if devName!=None:
                with eng.connect() as con:
                    dev = con.execute("select*from devices where devName= "+"'"+devName+"'").fetchone()
                    res = con.execute("select*from datapoints where dp_dev= "+"'"+dev.devName+"'"+" group by dpName").fetchall()
                    for row in res:
                        self.dataPointList.append(row.dpName)
                    data = {'code': 200, 'data': {'dataPointList':self.dataPointList}}
            else:
                data = {'code': 2002, 'data': {'dataPointList':[]}}
            return data
        except Exception as e:
            return {"code": "500", "data": {'dataPointList':[]}}
