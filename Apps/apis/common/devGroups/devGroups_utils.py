from config import DB_URI
from sqlalchemy import create_engine
eng = create_engine(DB_URI)
from Apps.apis.common.plot.plot_utils import coordinate_to_list

class devGroupHandle():
    def __init__(self):
        self.reg_p = []
        self.regs = []
        self.groupInfo = []

    def getreg(self):
        with eng.connect() as con:
            reg = con.execute("select * from regions ").fetchall()
            for r in reg:
                self.groupInfo = []
                reg_p = coordinate_to_list(r.regPosition)
                gro = con.execute("select * from groups where g_reg="+"'"+r.regName+"'").fetchall()
                if gro:
                    for g in gro:
                        g_p = coordinate_to_list(g.gPosition)
                        dev = con.execute("select * from devices where device_g="+"'"+g.gName+"'").fetchall()
                        ginfo = {'gName':g.gName,
                                 'date':g.createTime,
                                 'devsTotal':len(dev),
                                 'desc':g.gDesc,
                                 'position':g_p}
                        self.groupInfo.append(ginfo)
                else:
                    self.groupInfo = []
                plot = con.execute("select * from plots where plot_regid="+str(r.id)).fetchall()
                reg = {'regName': r.regName,
                       'date': r.createTime,
                       'groupInfo':self.groupInfo,
                       'layerUrl': r.layerUrl,
                       'desc': r.regDesc,
                       'localtion': r.regLocation,
                       'regRange': r.regRange,
                       'polotsTotal':len(plot),
                       'position': reg_p}
                self.regs.append(reg)
        data = {'code':200,'data':self.regs}
        return data
