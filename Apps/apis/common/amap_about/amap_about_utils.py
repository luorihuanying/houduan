# -*- coding: utf-8 -*-
from config import DB_URI
from sqlalchemy import create_engine

end = create_engine(DB_URI)
from Apps.apis.common.plot.plot_utils import coordinate_to_list,exterior_to_list


class amapAboutHandle():

    def __init__(self):
        self.all = []
        self.groups = []
        self.devs = []
        self.dataPoints = []
        self.plots = []
        self.bounds = []

    # amap_about.js
    def getdata(self):
        with end.connect() as con:
            # 区域
            reg = con.execute("select*from regions").fetchall()
            for r in reg:
                self.plots = []
                self.groups = []
                # 存坐标
                reg_p = coordinate_to_list(r.regPosition)
                gro = con.execute("select*from groups where g_reg = " + "'" + r.regName + "'").fetchall()
                if gro:
                    for g in gro:
                        self.devs = []
                        dev = con.execute("select*from devices where device_g = " + "'" + g.gName + "'").fetchall()
                        devsTotal = len(dev)
                        g_p = coordinate_to_list(g.gPosition)
                        if dev:
                            for d in dev:
                                self.dataPoints = []
                                dp = con.execute(
                                    "select * from datapoints where dp_dev = " + "'"+d.devName+"'" + " group by dpName").fetchall()
                                dpTotal = len(dp)
                                dp1 = con.execute("select*from datapoints where dp_dev = " + "'"+d.devName+"'").fetchall()
                                dataTotal = len(dp1)
                                dev_p = coordinate_to_list(d.devPosition)
                                if dp:
                                    for DP in dp:
                                        dp_p = coordinate_to_list(DP.dpPosition)
                                        res = con.execute(
                                            "select*from datapoints where dp_dev = " + "'"+d.devName+"'" + " and dpName = " + "'" + DP.dpName + "'").fetchall()
                                        if res:
                                            dataPoint = {'dataTotal': len(res),
                                                         'desc': DP.dpDesc,
                                                         'dpName': DP.dpName,
                                                         'position': dp_p,
                                                         'type': DP.type}
                                            self.dataPoints.append(dataPoint)
                                        else:
                                            dataPoint = {'dataTotal': 0,
                                                         'desc': '',
                                                         'dpName': '',
                                                         'position': [],
                                                         'type': 0}
                                            self.dataPoints.append(dataPoint)
                                else:
                                    self.dataPoints = []
                                dev = {'dataPoints': self.dataPoints,
                                       'dataTotal': dataTotal,
                                       'desc': d.devDesc,
                                       'devName': d.devName,
                                       'dpTotal': dpTotal,
                                       'position': dev_p}
                                self.devs.append(dev)

                        else:
                            self.devs = []
                        group = {'desc': g.gDesc,
                                 'devs': self.devs,
                                 'devsTotal': devsTotal,
                                 'gName': g.gName,
                                 'position': g_p,
                                 }
                        self.groups.append(group)
                else:
                    self.groups = []
                # 地块信息
                pl = con.execute("select * from plots where plot_regid = " + str(r.id)).fetchall()
                if pl:
                    for p in pl:
                        self.bounds = []
                        self.bounds = coordinate_to_list(p.bounds)
                        plot = {'bounds': self.bounds,
                                'desc': p.plotsDesc,
                                'exterior': exterior_to_list(p.exterior),
                                'layerUrl': p.layerUrl,
                                'plotsRange': p.plotsRange,
                                'plotName': p.plotsName}
                        self.plots.append(plot)
                else:
                    self.plots = []

                al = {'desc': r.regDesc,
                      'groups': self.groups,
                      'location': r.regLocation,
                      'plots': self.plots,
                      'position': reg_p,
                      'regName': r.regName,
                      'regRange': r.regRange}
                self.all.append(al)
        data = {'code':200,'data':self.all}
        return data
