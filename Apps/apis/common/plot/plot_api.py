from flask import g, request
from flask_restful import Resource, fields, marshal
from Apps.apis.common.plot.plot_utils import dataplotHandle
from Apps.apis.common.user.user_utils import login_required
from config import DB_URI
from sqlalchemy import create_engine
from Apps.apis.common.plot.plot_utils import exterior_to_list
eng = create_engine(DB_URI)


plot_fields = {'plotName': fields.String,
               'desc': fields.String,
               'bounds': fields.List(fields.Float),
               'layerUrl': fields.String,
               'exterior': fields.List(fields.List(fields.Float)),
               'lotRange': fields.Integer}
p_fields = {'regName':fields.String,
            'plots':fields.List(fields.Nested(plot_fields))}
plotList_fields = {'code':fields.Integer,'data': fields.List(fields.Nested(p_fields))}

flag_fields = {'code':fields.Integer,'msg':fields.String}


class plotList(Resource, dataplotHandle):
    @login_required
    def get(self):
        rank = g.user.rank
        if rank:
            data = marshal(self.getplotList(), plotList_fields)
            return data



# post
class updatePlotInfo(Resource):
    @login_required
    def post(self):
        plotName = request.json.get('plotName')
        desc = request.json.get('desc')
        bounds = request.json.get('bounds')
        plotRange = request.json.get('lotRange')
        regName = request.json.get('regName')
        exterior = request.json.get('exterior')
        layerUrl = request.json.get('layerUrl')
        rank = g.user.rank
        if rank:
            with eng.connect() as con:
                reg = con.execute("select*from regions where regName="+"'"+regName+"'").fetchone()
                if reg:
                    if exterior:
                        res = con.execute("update plots set bounds=" + "'" + str(bounds) + "'" + ",plot_regid=" + str(reg.id) + ",plotsRange=" + "'" + str(plotRange) +
                                          "'" + ",plotsDesc=" + "'" + desc + "'" + ",layerUrl="+"'"+layerUrl+"'"+",exterior="+"'"+str(exterior)+"'"+" where plotsName=" + "'"+plotName+"'")
                    else:
                        res = con.execute("update plots set bounds=" + "'" + str(bounds) + "'" + ",plot_regid=" + str(
                            reg.id) + ",plotsRange=" + "'" + str(plotRange) +
                                          "'" + ",plotsDesc=" + "'" + desc + "'" + ",layerUrl=" + "'" + layerUrl + "'"+ " where plotsName=" + "'" + plotName + "'")
                    if res:
                        return {'code':200,'msg':'ok'}
                else:
                    return {'code':1000,'msg':'Region not existent'}


class createPlotInfo(Resource):
    @login_required
    def post(self):
        plotName = request.json.get('plotName')
        desc = request.json.get('desc')
        bounds = request.json.get('bounds')
        plotRange = request.json.get('plotRange')
        regName = request.json.get('regName')
        exterior = request.json.get('exterior')
        layerUrl = request.json.get('layerUrl')
        rank = g.user.rank
        if rank:
            with eng.connect() as con:
                reg = con.execute("select*from regions where regName="+"'"+regName+"'").fetchone()
                if reg:
                    if exterior:
                        res = con.execute("insert into plots (bounds,plotsName,plotsRange,plotsDesc,plot_regid,layerUrl,exterior) values ("
                                          "" + "'" + str(bounds) + "'" + "," + "'" + plotName + "'" + "," + "'" + str(plotRange) + "'" + "," + "'" +
                                          desc + "'" + "," + str(reg.id) + ","+"'"+layerUrl+"'"+","+"'"+str(exterior)+"'"+")")
                    else:
                        res = con.execute(
                            "insert into plots (bounds,plotsName,plotsRange,plotsDesc,plot_regid,layerUrl,exterior) values ("
                            "" + "'" + str(bounds) + "'" + "," + "'" + plotName + "'" + "," + "'" + str(plotRange) + "'" + "," + "'" +
                            desc + "'" + "," + str(
                                reg.id) + "," + "'" + layerUrl + "'" + ")")
                    if res.rowcount:
                        return {'code':200,'msg':'ok'}
                    else:
                        return {'code': 2003, 'msg': 'Insert failed'}
                else:
                    return {'code': 1000, 'msg': 'Region not existent'}

class deletePlotInfo(Resource):
    def __init__(self):
        self.pname = []
    @login_required
    def post(self):
        plotName = request.json.get('plotName')
        regName = request.json.get('regName')
        rank = g.user.rank
        if rank:
            with eng.connect() as con:
                reg = con.execute("select*from regions where regName="+"'"+regName+"'").fetchone()
                if reg:
                    plot = con.execute("select*from plots where plot_regid="+str(reg.id)).fetchall()
                    if plot:
                        for p in plot:
                            self.pname.append(p.plotsName)
                        if plotName in self.pname:
                            res = con.execute("delete from plots where plotsName = "+"'"+plotName+"'")
                            if res.rowcount:
                                return {'code': 200, 'msg': 'ok'}
                            else:
                                return {'code': 2005, 'msg': 'Delete failed'}
                        else:
                            return {'code': 1002, 'msg': 'Plot not existent'}
                else:
                    return {'code': 1000, 'msg': 'Region not existent'}
