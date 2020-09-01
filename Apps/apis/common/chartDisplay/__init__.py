# -*- coding: utf-8 -*-
from flask_restful import Api

from Apps.apis.common.chartDisplay.sensorDataApi import getZhiShang1,getTianQi,getCamera,getDataDay,getDataMonth,getDataYear,downloadData,livePic

getChartDataApi = Api(prefix="/cms")

getChartDataApi.add_resource(getZhiShang1, "/getZhiShang1Api/")
getChartDataApi.add_resource(getTianQi, "/getTianQiApi/")
getChartDataApi.add_resource(getCamera, "/getCameraApi/")
getChartDataApi.add_resource(getDataDay, "/getDataDayApi/")
getChartDataApi.add_resource(getDataMonth, "/getDataMonthApi/")
getChartDataApi.add_resource(getDataYear, "/getDataYearApi/")
getChartDataApi.add_resource(livePic, "/getlivePicApi/")
# post
getChartDataApi.add_resource(downloadData, "/downloadDataApi/",strict_slashes = False)