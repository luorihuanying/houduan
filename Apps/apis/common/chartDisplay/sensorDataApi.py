import time

from flask import g, request
from flask_restful import Resource, fields, marshal, reqparse
from Apps.apis.common.chartDisplay.sensorDataUtils import getData
from Apps.apis.common.chartDisplay.getCameraUtils import getCameraData
from Apps.apis.common.user.user_utils import login_required

flag_fields = {'code': fields.Integer, "msg": fields.String}
parser = reqparse.RequestParser()
parser.add_argument("value", type=int)

t3 = {'temperature': fields.Float,
      'moisture': fields.Float}
t2 = {'temperature': fields.Float}
t1 = {'地表': fields.Nested(t2),
      '10cm': fields.Nested(t3),
      '20cm': fields.Nested(t3),
      '30cm': fields.Nested(t3),
      '40cm': fields.Nested(t3),
      '50cm': fields.Nested(t3),
      '60cm': fields.Nested(t3)}

chartDataFields = {'timestamp': fields.String,
                   'datetime': fields.String,
                   'values': fields.Nested(t1)}

chart_fields = {'code': fields.Integer, 'data': fields.Nested(chartDataFields)}

tq = {'averageWindSpeed': fields.Float,
      'rainfall': fields.Float,
      'solarRadiationIntensity': fields.Float,
      'airTemperature': fields.Float,
      'relativeHumidity': fields.Float,
      'windDirection': fields.Float}

t = {'地表': fields.Nested(tq)}

tianQin = {'timestamp': fields.Integer,
           'datetime': fields.String,
           'values': fields.Nested(t)}
tianQin_fields = {'code': fields.Integer, 'data': fields.List(fields.Nested(tianQin))}
# 摄像头
camera = {'设备名称': fields.String,
          '在线状态': fields.String,
          '设备编号': fields.String,
          '设备型号': fields.String,
          '拍摄间隔': fields.Integer,
          '充电状态': fields.String,
          '最后活跃时间': fields.String,
          '位置信息': fields.String,
          '海拔高度': fields.Integer,
          '经度': fields.Float,
          '纬度': fields.Float}

camera_fields = {'code': fields.Integer, 'data': fields.Nested(camera)}

newest = {'wendu':fields.String,'qiya':fields.String,'guangqiang':fields.String,'shijian':fields.String}
cameraDataDay = {'date': fields.List(fields.String),
                 'humidity': fields.List(fields.Float),
                 'illumination': fields.List(fields.Float),
                 'pressure': fields.List(fields.Float),
                 'temperature': fields.List(fields.Float),
                 'newest':fields.Nested(newest),
                 'avgMaxMin':fields.List(fields.List(fields.String))}
cameraDataDay_fields = {'code': fields.Integer, 'data': fields.Nested(cameraDataDay)}

CDM = {'average': fields.List(fields.Float),
       'max': fields.List(fields.Float),
       'min': fields.List(fields.Float)}
cameraDataMonth = {'humidity': fields.Nested(CDM),
                   'illumination': fields.Nested(CDM),
                   'pressure': fields.Nested(CDM),
                   'temperature': fields.Nested(CDM),
                   'date': fields.List(fields.String),
                   'sunshine': fields.List(fields.Integer)}
cameraDataMonth_fields = {'code': fields.Integer, 'data': fields.Nested(cameraDataMonth)}

pic = {'createTime':fields.List(fields.String),
       'image':fields.List(fields.String),
       'latestPic':fields.String}
pic_fields = {'code':fields.Integer,'data':fields.Nested(pic)}

class getZhiShang1(Resource, getData):
    # @login_required
    def get(self):
        # rank = g.user.rank
        rank = 1
        if rank:
            oneDay, twoData, devId = getData.getLatestData(self, '18092100088571')
            data = getData.acquireDataCollectedByEquipment(self, oneDay, twoData, devId)
            return marshal({'code': 200, 'data': data}, chart_fields)

        else:
            return marshal({'code': 5000, 'msg': '无权限'}, flag_fields)


class getTianQi(Resource, getData):
    # @login_required
    def get(self):
        # rank = g.user.rank
        rank = 1
        if rank:
            oneDay, twoData, devId = getData.getLatestData(self, '19101600107986')
            data = getData.acquireTianQiData(self, oneDay, twoData, devId)
            return marshal({'code': 200, 'data': data}, tianQin_fields)

        else:
            return marshal({'code': 5000, 'msg': '无权限'}, flag_fields)


# 摄像头
class getCamera(Resource, getCameraData):
    # @login_required
    def get(self):
        # rank = g.user.rank
        rank = 1
        if rank:
            data = getCameraData.getFacilityInfo(self)
            return marshal({'code': 200, 'data': data}, camera_fields)

        else:
            return marshal({'code': 5000, 'msg': '无权限'}, flag_fields)


class getDataDay(Resource, getCameraData):
    def get(self):
        rank = 1
        if rank:
            start, end = getCameraData.fetchTimeInterval(self, 'day')
            data = getCameraData.queryEquipmentStaDay(self, start, end)
            dayData = {'date': data[0],
                       'humidity': data[1],
                       'illumination': data[2],
                       'pressure': data[3],
                       'temperature': data[4],
                       'newest':data[5],
                       'avgMaxMin':data[6]}
            return marshal({'code': 200, 'data': dayData}, cameraDataDay_fields)
        else:
            return marshal({'code': 5000, 'msg': '无权限'}, flag_fields)


class getDataMonth(Resource, getCameraData):
    def get(self):
        rank = 1
        if rank:
            start, end = getCameraData.fetchTimeInterval(self, 'month')
            data = getCameraData.queryEquipmentStaMonth(self, start, end)
            return marshal({'code': 200, 'data': data}, cameraDataMonth_fields)
        else:
            return marshal({'code': 5000, 'msg': '无权限'}, flag_fields)


class getDataYear(Resource, getCameraData):
    def get(self):
        rank = 1
        if rank:
            year = getCameraData.fetchTimeInterval(self, 'year')
            data = getCameraData.queryEquipmentStaYear(self, year)
            return marshal({'code': 200, 'data': data}, cameraDataMonth_fields)
        else:
            return marshal({'code': 5000, 'msg': '无权限'}, flag_fields)


class downloadData(Resource, getCameraData):
    def post(self):
        rank = 1
        if rank:
            currentTime = int(time.time())
            args = parser.parse_args()
            value = int(args.get("value")/1000)
            timeDifference = currentTime - value
            print(value,currentTime)
            if timeDifference < 2592000:
                data = getCameraData.queryEquipmentStaMonth(self, value, currentTime)
                return marshal({'code': 200, 'data': data}, cameraDataMonth_fields)
            else:
                return marshal({'code': 400, 'msg': '只能导出距今一个月内的数据'}, flag_fields)

class livePic(Resource, getCameraData):
    def get(self):
        rank = 1
        if rank:
            data = getCameraData.getlivePic(self)
            return marshal({'code':200,'data':data},pic_fields)
        else:
            return marshal({'code': 5000, 'msg': '无权限'}, flag_fields)

