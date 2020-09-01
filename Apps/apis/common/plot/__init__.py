# -*- coding: utf-8 -*-
from flask_restful import Api

from Apps.apis.common.plot.plot_api import plotList,createPlotInfo,updatePlotInfo,deletePlotInfo

plot_api = Api(prefix="/cms")

plot_api.add_resource(plotList, "/getPlots/")
#post
plot_api.add_resource(createPlotInfo, "/createPlotInfo/")
plot_api.add_resource(updatePlotInfo, "/updatePlotInfo/")
plot_api.add_resource(deletePlotInfo, "/deletePlotInfo/")
