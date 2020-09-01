import time

import requests


class getData:

    def __init__(self):
        self.base_url = 'http://openapi.ecois.info/v3/'
        self.token = self.get_token()

    @staticmethod
    def error_code(code):
        if code is None:
            return False

        if code == 0:
            return True
        return False

    @property
    def headers(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': self.get_token()
        }
        return headers

    # 获取token,
    # 调用样例/v3/token?appid=test&secret=test
    def get_token(self):
        url = self.base_url + 'token?appid=dKXWuDrgdWbiGT7Z&secret=ILncoN60J4FS0EvrzropdWZ4LCpIStNw'
        r = requests.get(url)
        if r.status_code == 200:
            token = r.json().get('token', None)
            expirationTime = r.json().get('expires', None)
            return token
        else:
            raise ValueError('连接无效!')

    # 获取设备列表
    # 调用样例/v3/devices?page=2&limit=100
    def getDeviceList(self):
        url = self.base_url + 'devices?page=1&limit=100'
        r = requests.get(url, headers=self.headers)
        # "message": "ok",
        # "count": 1,
        # "list"
        print(r.json().get('list', None))

    # 获取设备详情
    # 调用样例
    # / v3 / device / 00000000000000
    def getDeviceDetails(self):
        url = self.base_url + 'device/19101600107986'
        r = requests.get(url, headers=self.headers)
        alias = r.json().get('alias', None)
        status = r.json().get('status', None)
        print(alias, status)

    # 获取设备采集数据
    # 调用样例/v3/device/00000000000000/data?range=20180102,20181112&includeParameters=moisture,temperature&includeNodes=0,1,2,3,4
    def acquireDataCollectedByEquipment(self, oneDay, twoDay, devId):
        url = self.base_url + 'device/' + devId + '/data?range=' + oneDay + ',' + twoDay + '&includeParameters=moisture,temperature'
        r = requests.get(url, headers=self.headers)
        list = r.json().get('list', None)
        return list

    def acquireTianQiData(self, oneDay, twoDay, devId):
        url = self.base_url + 'device/' + devId + '/data?range=' + oneDay + ',' + twoDay + '&includeParameters=rainfall,solarRadiationIntensity,airTemperature,relativeHumidity,averageWindSpeed,windDirection'
        r = requests.get(url, headers=self.headers)
        list = r.json().get('list', None)
        return list

    # 获取设备采集参数的描述
    # 调用样例/v3/device/00000000000000/description
    def deviceParametersDescription(self):
        url = self.base_url + 'device/18121700094174/description'
        r = requests.get(url, headers=self.headers)
        nodes = r.json().get('nodes', None)
        print(nodes)

    # 增量获取设备采集数据
    # 调用样例/v3/device/00000000000000/data/incremental
    def addAcquireDataCollectedByEquipment(self):
        url = self.base_url + 'device/18121700094174/data/incremental'
        r = requests.get(url, headers=self.headers)
        increments = r.json().get('increments', None)
        print(increments[0]['values'])

    # 获取设备最新一包采集数据
    # 调用样例/v3/device/00000000000000/latest
    def getLatestData(self, devId):
        url = self.base_url + 'device/' + devId + '/latest'
        r = requests.get(url, headers=self.headers)
        timeStamp = r.json().get('timestamp', None)
        t = int(timeStamp) - 86400
        t1 = time.localtime(t)
        oneDay = time.strftime("%Y-%m-%d %H:%M:%S", t1)
        timeArray = time.localtime(timeStamp)
        twoDay = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        oneDay = oneDay[:4] + oneDay[5:7] + oneDay[8:10]
        twoDay = twoDay[:4] + twoDay[5:7] + twoDay[8:10]
        return oneDay, twoDay, devId


if __name__ == '__main__':
    test = getData()
    f = test.getLatestData()
    print(f)
