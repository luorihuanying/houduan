import time

from flask import g, request
from flask_restful import Resource, fields, marshal, reqparse
from Apps.apis.common.chartDisplay.sensorDataUtils import getData
from Apps.apis.common.chartDisplay.getCameraUtils import getCameraData
from Apps.apis.common.chartDisplay.getNodeUtils import getNode
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

newest = {'wendu': fields.String, 'qiya': fields.String, 'guangqiang': fields.String, 'shijian': fields.String}
cameraDataDay = {'date': fields.List(fields.String),
                 'humidity': fields.List(fields.Float),
                 'illumination': fields.List(fields.Float),
                 'pressure': fields.List(fields.Float),
                 'temperature': fields.List(fields.Float),
                 'newest': fields.Nested(newest),
                 'avgMaxMin': fields.List(fields.List(fields.String))}
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

pic = {'createTime': fields.List(fields.String),
       'image': fields.List(fields.String),
       'latestPic': fields.String}
pic_fields = {'code': fields.Integer, 'data': fields.Nested(pic)}


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
                       'newest': data[5],
                       'avgMaxMin': data[6]}
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
            value = int(args.get("value") / 1000)
            timeDifference = currentTime - value
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
            return marshal({'code': 200, 'data': data}, pic_fields)
        else:
            return marshal({'code': 5000, 'msg': '无权限'}, flag_fields)


new = {'createTime': fields.String,
       'dataPointName': fields.String,
       'value': fields.String}
newtest_fields = {'code': fields.Integer, 'data': fields.List(fields.List(fields.Nested(new)))}


# 物联网节点
class getNewtestData(Resource, getNode):
    def get(self):
        rank = 1
        if rank:
            data = getNode.newtestHis(self)
            return marshal({'code': 200, 'data': data}, newtest_fields)
        else:
            return marshal({'code': 5000, 'msg': '无权限'}, flag_fields)


info = {'state': fields.String, 'latestTime': fields.String, 'devId': fields.String}
info_fields = {'code': fields.Integer, 'data': fields.Nested(info)}


class get4GInfo(Resource, getNode):
    def get(self):
        rank = 1
        if rank:
            data = getNode.getInfo(self)
            return marshal({'code': 200, 'data': data}, info_fields)
        else:
            return marshal({'code': 5000, 'msg': '无权限'}, flag_fields)


# 自定义时间格式
def _custom_format(dt, fmt):
    if isinstance(dt, str):
        return dt
    return dt.strftime(fmt)


class CustomDate(fields.DateTime):
    '''
    自定义CustomDate,原有的fileds.DateTime序列化后
    只支持 rfc822,ios8601 格式，新增 strftime 格式
    strftime格式下支持 format 参数，默认为 '%Y-%m-%d %H:%M:%S'
    '''
    def __init__(self, dt_format='rfc822', format=None, **kwargs):
        super(fields.DateTime, self).__init__(**kwargs)
        self.dt_format = dt_format
        self.fmt = format if format else '%Y-%m-%d %H:%M:%S'

    def format(self, value):
        if self.dt_format in ('rfc822', 'iso8601'):
            return super(fields.DateTime.format(value))
        elif self.dt_format == 'strftime':
            return _custom_format(value, self.fmt)
        else:
            raise Exception('Unsupported date format %s' % self.dt_format)
# 使用方法很简单和上面使用 fields.Raw 自定义的fields 一样：
#
# fields = {
#     'name': CustomDate(dt_format='strftime')
# }


# timeValue = {'createTime': fields.List(CustomDate(dt_format='strftime')), 'value': fields.List(fields.Float)}
timeValue = {'createTime': fields.List(fields.String), 'value': fields.List(fields.Float)}
dayData = {'h10': fields.Nested(timeValue),
           'h20': fields.Nested(timeValue),
           'h30': fields.Nested(timeValue),
           'v20': fields.Nested(timeValue)}
dayData_fields = {'code': fields.Integer, 'data': fields.Nested(dayData)}


class getIotDay(Resource, getNode):
    def get(self):
        rank = 1
        if rank:
            data = getNode.getIotDayData(self)
            return marshal({'code': 200, 'data': data}, dayData_fields)
        else:
            return marshal({'code': 5000, 'msg': '无权限'}, flag_fields)

week = {'avg':fields.List(fields.Float),
        'max':fields.List(fields.Float),
        'min':fields.List(fields.Float),
        'date':fields.List(fields.String),
        'mi':fields.Float,
        'ma':fields.Float}
weekdata = {'h10':fields.Nested(week),
            'h20':fields.Nested(week),
            'h30':fields.Nested(week),
            'v20':fields.Nested(week)}
week_fields = {'code':fields.Integer,'data':fields.Nested(weekdata)}
class getIotWeek(Resource,getNode):
    def get(self):
        rank = 1
        if rank:
            data = getNode.getIotWeekData(self)
            return marshal({'code': 200, 'data': data}, week_fields)
        else:
            return marshal({'code': 5000, 'msg': '无权限'}, flag_fields)

month = {'date':fields.List(fields.String),
         'avg':fields.List(fields.Float),
         'max':fields.List(fields.Float),
         'min':fields.List(fields.Float),
         'av':fields.Float,
         'ma':fields.Float,
         'mi':fields.Float}
monthData = {'h10':fields.Nested(month),
         'h20':fields.Nested(month),
         'h30':fields.Nested(month),
         'v20':fields.Nested(month)}
month_fields = {'code':fields.Integer,'data':fields.Nested(monthData)}
class getIotMonth(Resource,getNode):
    def get(self):
        rank = 1
        if rank:
            data = getNode.getIotMonthData(self)
            return marshal({'code': 200, 'data': data}, month_fields)
        else:
            return marshal({'code': 5000, 'msg': '无权限'}, flag_fields)