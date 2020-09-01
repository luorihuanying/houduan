import datetime

from flask_restful import reqparse
from config import DB_URI
from sqlalchemy import create_engine
eng = create_engine(DB_URI)
from Apps.apis.common.plot.plot_utils import coordinate_to_list

parser = reqparse.RequestParser()
parser.add_argument('regName',type=str)
parser.add_argument('groupName',type=str)
parser.add_argument('status',type=int)
parser.add_argument('page',type=int)
parser.add_argument('limit',type=int)



class devListHandle():
    def __init__(self):
        self.group = []
        self.gname = []
        self.regLists = []
        self.groups = []
        self.sumdev = 0
        self.online = 0
        self.packs = []
        self.devs = []
        self.regdata = []

    def getdevList1(self):
        args = parser.parse_args()
        regName = args.get('regName')
        groupName = args.get('groupName')
        status = args.get('status')
        page = args.get('page')
        limit = args.get('limit')
        if regName!=None and groupName!=None and status!=None and page!=None and limit!=None:
            with eng.connect() as con:
                gro = con.execute("select*from groups where g_reg="+"'"+regName+"'").fetchall()
                if gro:
                    for g in gro:
                        if g.gName==groupName:
                            dev = con.execute("select*from devices where device_g="+"'"+groupName+"'"+" and status="+str(status)).fetchall()
                            if dev:
                                for d in dev:
                                    dev_p = coordinate_to_list(d.devPosition)
                                    dev = {'id': d.id,
                                           'devName': d.devName,
                                           'regName': regName,
                                           'status': d.status,
                                           'gName': g.gName,
                                           'date': d.createTime,
                                           'position': dev_p}
                                    self.devs.append(dev)
                                #返回的记录小于传入的limit则全部显示
                                if len(self.devs) <= limit:
                                    devdata = {"code": 200, "data": [{'regName': regName,'groups': [groupName],'devs': self.devs}]}
                                #只要求显示第0页，但是返回记录大于limit，则只显示limit
                                elif len(self.devs) > limit and page == 0:
                                    devdata = {"code": 200,
                                               "data": [{'regName': regName, 'groups': [groupName], 'devs': self.devs[0:limit]}]}
                                else:
                                    #显示第page页，page从0开始
                                    if limit * page <= len(self.devs):
                                        devdata = {"code": 200, "data": [{'regName': regName, 'groups': [groupName], 'devs': self.devs[limit * (page - 1):limit * page]}]}
                                    else:
                                        #如果4页数据有40条记录，5页有50条，但是返回的记录只有45条，要求显示第五页则只显示第40~45条数据
                                        if len(self.devs) > limit * (page - 1) and len(
                                                self.devs) < limit * page:
                                            devdata = {"code": 200, "data": [
                                                {'regName': regName, 'groups': [groupName], 'devs': self.devs[limit * (page - 1):]}]}
                                        else:
                                            #如果返回数据只能够显示到第4页，而传入page=5则返回空数据和私有状态码
                                            devdata = {"code": 2001, "data": [
                                                {'regName': regName, 'groups': [groupName], 'devs': []}]}
                                return devdata
                            else:
                                data = {'regName': regName,
                                        'groups': [groupName],
                                        'devs': []}
                                return {'code': 200, 'data': [data]}
                else:
                    data = {'regName':regName,
                            'groups':[],
                            'devs':[]}
                    return {'code':200,'data':[data]}
        else:
            with eng.connect() as con:
                reg = con.execute("select*from regions").fetchall()
                for r in reg:
                    self.group = []
                    self.devs = []
                    gro = con.execute("select*from groups where g_reg="+"'"+r.regName+"'").fetchall()
                    if gro:
                        for g in gro:
                            self.group.append(g.gName)
                            dev = con.execute("select*from devices where device_g="+"'"+g.gName+"'").fetchall()
                            if dev:
                                for d in dev:
                                    dev_P = coordinate_to_list(d.devPosition)
                                    dev = {'id':d.id,
                                           'devName':d.devName,
                                           'regName':r.regName,
                                           'status':d.status,
                                           'gName':g.gName,
                                           'date':d.createTime,
                                           'position':dev_P}
                                    self.devs.append(dev)
                        data = {'regName': r.regName,
                                'groups': self.group,
                                'devs': self.devs}
                        self.regdata.append(data)
                    else:
                        data = {'regName':r.regName,
                                'groups':[],
                                'devs':[]}
                        self.regdata.append(data)
            return {'code':200,'data':self.regdata}

    def getreg(self):
        with eng.connect() as con:
            reg = con.execute("select*from regions").fetchall()
            for r in reg:
                self.groups = []
                self.sumdev = 0
                self.online = 0
                gro = con.execute("select * from groups where g_reg = "+"'"+r.regName+"'").fetchall()
                if gro:
                    for g in gro:
                        dev = con.execute("select*from devices where device_g = "+"'"+g.gName+"'").fetchall()
                        online = con.execute("select*from devices where device_g = " + "'" + g.gName + "'"+" and status="+str(1)).fetchall()
                        if dev:
                            self.sumdev = self.sumdev+len(dev)
                            self.online = self.online+len(online)
                            group = {'name':g.gName,
                                     'devsCount':len(dev)}
                            self.groups.append(group)
                        else:
                            self.sumdev = self.sumdev
                            group = {'name': g.gName,
                                     'devsCount': 0}
                            self.groups.append(group)
                    pack = {'regName':r.regName,
                            'groups':self.groups,
                            'devsCount':{'total':self.sumdev,
                                         'offline':0,
                                         'online':self.online}}
                    self.packs.append(pack)
                else:
                    pack = {'regName':r.regName,
                            'groups':[],
                            'devsCount':{'total':0,
                                         'offline':0,
                                         'online':0}}
                    self.packs.append(pack)
        data = {'code':200,'data':self.packs}
        return data
