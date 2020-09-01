from flask_restful import reqparse

from config import DB_URI
from sqlalchemy import create_engine
eng = create_engine(DB_URI)

parser = reqparse.RequestParser()
parser.add_argument("regName", type=str)

def exterior_to_list(exterior):
    list1 = []
    list2 = []
    list3 = []
    for i in exterior.split(','):
        list1.append(i)
    for j in list1:
        j = j.replace(' ', '')
        j = j.replace('[', '')
        j = j.replace(']', '')
        j = float(j)
        list2.append(j)
    for k in range(len(list2)):
        if k + 2 < len(list2):
            list3.append([list2[k], list2[k + 2]])
    return list3

def coordinate_to_list(coordinate):
    bound1 = []
    bound2 = []
    for i in coordinate.split(','):
        bound1.append(i)
    for j in bound1:
        j = j.replace(' ', '')
        j = j.replace('[', '')
        j = j.replace(']', '')
        bound2.append(float(j))
    return bound2

class dataplotHandle():

    def __init__(self):
        self.bounds = []
        self.plotLists = []
        self.regs = []

    def getplotList(self):
        args = parser.parse_args()
        regName = args.get('regName')
        if regName!=None:
            with eng.connect() as con:
                reg = con.execute("select*from regions where regName="+"'"+regName+"'").fetchone()
                if reg:
                    plot = con.execute("select*from plots where plot_regid = " + str(reg.id)).fetchall()
                    if plot:
                        for p in plot:
                            self.bounds = []
                            self.bounds = coordinate_to_list(p.bounds)
                            plotList = {'plotName': p.plotsName,
                                        'desc': p.plotsDesc,
                                        'bounds': self.bounds,
                                        'layerUrl': p.layerUrl,
                                        'exterior': exterior_to_list(p.exterior),
                                        'lotRange': p.plotsRange}
                            self.plotLists.append(plotList)
                        reg = {'regName': reg.regName,
                               'plots': self.plotLists}
                        self.regs.append(reg)
                    else:
                        reg = {'regName': reg.regName,
                               'plots': []}
                        self.regs.append(reg)
                else:
                    return {'code':1000,'data':[{'regName': regName,
                               'plots': []}]}
                data = {'code': 200, 'data': self.regs}
                return data
        else:
            with eng.connect() as con:
                reg = con.execute("select*from regions").fetchall()
                for r in reg:
                    self.plotLists = []
                    plot = con.execute("select*from plots where plot_regid = "+str(r.id)).fetchall()
                    if plot:
                        for p in plot:
                            self.bounds = []
                            self.bounds = coordinate_to_list(p.bounds)
                            plotList = {'plotName':p.plotsName,
                                        'desc':p.plotsDesc,
                                        'bounds':self.bounds,
                                        'layerUrl':p.layerUrl,
                                        'exterior':exterior_to_list(p.exterior),
                                        'lotRange':p.plotsRange}
                            self.plotLists.append(plotList)
                        reg = {'regName':r.regName,
                               'plots':self.plotLists}
                        self.regs.append(reg)
                    else:
                        reg = {'regName': r.regName,
                               'plots': []}
                        self.regs.append(reg)
            data = {'code':200,'data':self.regs}
            return data

