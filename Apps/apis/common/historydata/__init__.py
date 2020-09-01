# -*- coding: utf-8 -*-
from flask_restful import Api

from Apps.apis.common.historydata.historydata_api import historyData,regionGroupList,devList,dataPointList,createNewhistoryData,deleteOneData,changeAlarmStatus,updateData

historydata_api = Api(prefix="/cms")

historydata_api.add_resource(historyData, "/historydataApi/")
historydata_api.add_resource(regionGroupList, "/regGroApi/")
historydata_api.add_resource(devList, "/getDevsApi/")
historydata_api.add_resource(dataPointList, "/dpApi/")
#post
historydata_api.add_resource(createNewhistoryData, "/createNewhistoryDataApi/")
historydata_api.add_resource(deleteOneData, "/deleteOneDataApi/")
historydata_api.add_resource(changeAlarmStatus, "/changeAlarmStatusApi/")
historydata_api.add_resource(updateData, "/updateData/")

