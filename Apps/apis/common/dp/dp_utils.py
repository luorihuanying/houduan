from flask import request
from flask_restful import reqparse

from config import DB_URI
from sqlalchemy import create_engine
eng = create_engine(DB_URI)
from Apps.apis.common.plot.plot_utils import coordinate_to_list


#传入区域名
parser = reqparse.RequestParser()
parser.add_argument("regName",type=str)

class dataPointsListHandle():

    def __init__(self):
        self.dataPointsLists1 = []
        self.dataPointsLists = []
        self.d1s = []
        self.reg = []
        self.dp = []
        self.dev = []
        self.pack = []

    def getreg(self):
        args = parser.parse_args()
        regName = args.get("regName")
        if regName:
            with eng.connect() as con:
                reg = con.execute("select*from regions where regName="+"'"+regName+"'").fetchone()
                gro = con.execute("select * from groups where g_reg = " + "'" + reg.regName + "'").fetchall()
                if gro:
                    for g in gro:
                        dev = con.execute("select*from devices where device_g = " + "'" + g.gName + "'").fetchall()
                        if dev:
                            for d in dev:
                                DEV_p = coordinate_to_list(d.devPosition)
                                dp = con.execute("select*from datapoints where dp_dev = " + "'" + d.devName + "'"+" group by dpName").fetchall()
                                if dp:
                                    for D in dp:
                                        DP_p = coordinate_to_list(D.dpPosition)
                                        his = con.execute("select*from historydatas where dataPointName = " + "'" + D.dpName + "'"+" and devId="+"'"+d.deviceId+"'").fetchall()
                                        dpdata = {
                                            'dpName': D.dpName,
                                            'desc': D.dpDesc,
                                            'position': DP_p,
                                            'dataTotal': len(his),
                                            'type': D.type}
                                        self.dp.append(dpdata)
                                else:
                                    self.dp = []
                                dptotal = con.execute("select*from datapoints where dp_dev = " + "'" + d.devName + "'"+" group by dpName").fetchall()
                                print(d)
                                dataTotal = con.execute("select*from historydatas where devId = " + "'" + d.deviceId + "'").fetchall()
                                devdata = {'devName':d.devName,
                                           'desc':d.devDesc,
                                           'position':DEV_p,
                                           'dataPoints':self.dp,
                                           'dpTotal':len(dptotal),
                                           'dataTotal':len(dataTotal)}
                                self.dev.append(devdata)
                    reg = {'regName':regName,
                           'devs':self.dev}
                    self.pack.append(reg)
                else:
                    reg = {'regName': reg.regName,
                           'devs': []}
                    self.pack.append(reg)
            return {'code':200,'data':self.pack}
        else:
            with eng.connect() as con:
                reg = con.execute("select*from regions").fetchall()
                for r in reg:
                    gro = con.execute("select * from groups where g_reg = " + "'" + r.regName + "'").fetchall()
                    if gro:
                        for g in gro:
                            self.dev = []
                            dev = con.execute("select*from devices where device_g = " + "'" + g.gName + "'").fetchall()
                            if dev:
                                for d in dev:
                                    self.dp = []
                                    DEV_p = coordinate_to_list(d.devPosition)
                                    dp = con.execute(
                                        "select*from datapoints where dp_dev = " + "'" + d.devName + "'" + " group by dpName").fetchall()
                                    if dp:
                                        for D in dp:
                                            DP_p = coordinate_to_list(D.dpPosition)
                                            his = con.execute(
                                                "select*from historydatas where dataPointName = " + "'" + D.dpName + "'" + " and devId=" + "'" + d.deviceId + "'").fetchall()
                                            dpdata = {
                                                'dpName': D.dpName,
                                                'desc': D.dpDesc,
                                                'position': DP_p,
                                                'dataTotal': len(his),
                                                'type': D.type}
                                            self.dp.append(dpdata)
                                    dptotal = con.execute(
                                        "select*from datapoints where dp_dev = " + "'" + d.devName + "'" + " group by dpName").fetchall()
                                    dataTotal = con.execute(
                                        "select*from historydatas where devId = " + "'" + d.deviceId + "'").fetchall()
                                    devdata = {'devName': d.devName,
                                               'desc': d.devDesc,
                                               'position': DEV_p,
                                               'dataPoints': self.dp,
                                               'dpTotal': len(dptotal),
                                               'dataTotal': len(dataTotal)}
                                    self.dev.append(devdata)
                                reg = {'regName': r.regName,
                                       'devs': self.dev}
                                self.pack.append(reg)
                    else:
                        reg = {'regName': r.regName,
                               'devs': []}
                        self.pack.append(reg)
        data = {'code':200,'data':self.pack}
        print(data)
        return data