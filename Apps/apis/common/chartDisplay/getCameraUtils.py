import datetime
import hashlib
import base64
from Crypto.Cipher import AES
import time
import hmac
from hashlib import sha1
import random
import string
import numpy as np
import os, base64
import requests as req
from PIL import Image
from io import BytesIO
import requests


class getCameraData:

    def __init__(self):
        self.account = 'wx-MEFBQkloZw'
        self.number = 'W867012033415867'
        self.base_url = 'https://api.iot.xa.com/v5/'
        self.clientId = 'IIjMZPHdWoE'
        self.secret = '602d166208914f04'
        self.client_id = bytes(self.clientId, encoding='utf-8')
        secret = bytes(self.secret, encoding='utf-8')
        password_ori = 'qw?zx123'
        self.password = self.AES_Encrypt(password_ori, self.client_id, secret)
        self.session = self.get_session(self.password)
        data = self.getSignature(secret)
        self.parameter = '&client_id=' + self.clientId + '&nonce=' + data[0] + '&timestamp=' + data[1] + '&signature=' + \
                         data[2]

    # 时间戳转格式
    def timestampConverse(self, timestamp):
        dateArray = datetime.datetime.fromtimestamp(timestamp)
        otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
        return otherStyleTime

    # 在线状态
    def onlineStat(self, stat):
        dict = {'0': '未激活',
                '1': '在线',
                '2': '离线'}
        return dict[str(stat)]

    # 是否在充电
    def chargingStat(self, stat):
        dict = {'False': '未在充电',
                'True': '充电中'}
        return dict[str(stat)]

    @staticmethod
    def error_code(code):
        if code is None:
            return False

        if code == 0:
            return True
        return False

    @property
    def headers(self):
        data = self.getSignature(bytes(self.secret, encoding='utf-8'))
        headers = {
            'Content-Type': 'application/json;charset=utf-8',
            # 'client_id': self.account,
            # 'signature': data[2],
            'session': self.session
        }
        return headers

    def AES_Encrypt(self, data, client_id, secret):
        md5_iv = hashlib.md5(client_id).digest()
        md5_key = hashlib.md5(secret).digest()
        pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        data = pad(data)
        cipher = AES.new(md5_key, AES.MODE_CBC, md5_iv)
        encryptedbytes = cipher.encrypt(data.encode('utf8'))
        encodestrs = base64.b64encode(encryptedbytes)
        enctext = encodestrs.decode('utf8')
        return enctext

    def getSignature(self, secret):
        nonce = ''.join(random.sample(string.ascii_letters + string.digits, 6))
        timestamp = str(int(time.time()))
        signature = hmac.new(secret, bytes(timestamp + nonce, encoding='utf-8'), digestmod="sha1").hexdigest()
        return [nonce, timestamp, signature]

    # 获取token,
    # 调用样例/v3/token?appid=test&secret=test
    def get_session(self, password):
        data = self.getSignature(bytes(self.secret, encoding='utf-8'))
        # url = self.base_url + 'login?account='+account+'&password='+password+'&client_id='+self.account+'&nonce='+data[0]+'&timestamp='+data[1]+'&signature='+data[2]
        # print(url)
        # r = requests.post(url)
        # print(r)
        url = self.base_url + 'login?client_id=' + self.clientId + '&nonce=' + data[0] + '&timestamp=' + data[
            1] + '&signature=' + data[2]
        r = requests.post(url, json={'account': self.account, 'password': password})
        session = r.json().get('session', None)
        return session
        # 查询设备

    def getFacilityInfo(self):
        url = self.base_url + 'clients/' + self.account + '/devices/' + self.number + '?config_encoding=obj' + self.parameter
        r = requests.get(url, headers=self.headers)
        # 设备名称
        name = r.json().get('name', None)
        # 设备在线状态
        status = self.onlineStat(r.json().get('status', None))
        # 设备编号
        id = r.json().get('id', None)
        # 型号
        model_name = r.json().get('model_name', None)
        # 图像时间采样间隔
        config = int(int(r.json().get('config', None)['custom']['sleep']) / 60)
        # 是否在充电
        charging = self.chargingStat(r.json().get('charging', None))
        # 设备最后活跃时间
        activity = self.timestampConverse(r.json().get('activity', None))
        # 位置信息
        locationInfo = '广西崇左市扶绥县渠黎镇'
        # 经纬度、海拔
        altitude = r.json().get('location', None)['altitude']
        longitude = r.json().get('location', None)['longitude']
        # 纬度
        latitude = r.json().get('location', None)['latitude']
        data = {'设备名称': name,
                '在线状态': status,
                '设备编号': id,
                '设备型号': model_name,
                '拍摄间隔': config,
                '充电状态': charging,
                '最后活跃时间': activity,
                '位置信息': locationInfo,
                '海拔高度': altitude,
                '经度': longitude,
                '纬度': latitude}
        return data

    # 获取时间间隔
    def fetchTimeInterval(self, option):
        end = int(time.time())
        if option == 'day':
            timeArray = time.localtime(end)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)[:10] + ' 00:00:00'
            timeArray = time.strptime(otherStyleTime, "%Y-%m-%d %H:%M:%S")
            begin = int(time.mktime(timeArray))
        if option == 'month':
            begin = end - 2592000 + 86400
        if option == 'year':
            year = []
            for i in range(12):
                begin = end - 2592000
                year.append([begin, end])
                end = begin - 86400
            year = year[::-1]
            return year
        return begin, end

    def getHour(self):
        hour = []
        for i in range(24):
            if i < 10:
                hour.append('0' + str(i) + ':00')
            else:
                hour.append(str(i) + ':00')
        return hour

    def getDay(self):
        day = []
        now = int(time.time())
        before = now - 2592000 + 86400
        for i in range(30):
            timeArray = time.localtime(before)
            otherStyleTime = time.strftime("%Y-%m-%d", timeArray)[5:11]
            day.append(otherStyleTime)
            before = before + 86400
        return day

    def getYear(self):
        year = []
        now = int(time.time())
        before = now - 31536000 + 86400
        for i in range(365):
            timeArray = time.localtime(before)
            otherStyleTime = time.strftime("%Y-%m-%d", timeArray)[2:11]
            year.append(otherStyleTime)
            before = before + 86400
        return year

    # 查询设备期间数据  日
    def queryEquipmentStaDay(self, begin, end):
        begin = str(begin)
        end = str(end)
        url = self.base_url + 'clients/' + self.account + '/devices/' + self.number + '/datapoints/time?begin=' + begin + '&end=' + end + '&encoding=json&order=asc' + self.parameter
        r = requests.get(url, headers=self.headers)
        datapoints = r.json().get('datapoints', None)
        newest = {'wendu': '', 'qiya': '', 'guangqiang': '', 'shijian': ''}
        dd = datapoints[::-1]
        for i in dd:
            if 'battery' in i['data']:
                timeArray = time.localtime(i['created_at'])
                otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                newest['wendu'] = i['data']['temperature']
                newest['qiya'] = i['data']['pressure']
                newest['guangqiang'] = int(i['data']['illumination'])
                newest['shijian'] = otherStyleTime
                break
        t = []
        hum = []
        ill = []
        pre = []
        tem = []
        humidity = []
        illumination = []
        pressure = []
        temperature = []
        for i in range(24):
            humidity.append(None)
            illumination.append(None)
            pressure.append(None)
            temperature.append(None)
        for i in datapoints:
            if 'battery' in i['data']:
                timeArray = time.localtime(i['created_at'])
                otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                t.append(otherStyleTime)
                hum.append(i['data']['humidity'])
                ill.append(i['data']['illumination'])
                pre.append(i['data']['pressure'])
                tem.append(i['data']['temperature'])
        avgMaxMin = [[np.max(hum), np.min(hum), round(np.average(hum), 4)],
                     [np.max(ill), np.min(ill), round(np.average(ill), 4)],
                     [np.max(pre), np.min(pre), round(np.average(pre), 4)],
                     [np.max(tem), np.min(tem), round(np.average(tem), 4)]]
        ti = self.getHour()
        for i in range(len(ti)):
            for j in range(len(t)):
                if t[j][11:13] == ti[i][:2]:
                    humidity[i] = hum[j]
                    illumination[i] = ill[j]
                    pressure[i] = pre[j]
                    temperature[i] = tem[j]
        return [ti, humidity, illumination, pressure, temperature, newest, avgMaxMin]

    # 查询设备期间数据  月
    def queryEquipmentStaMonth(self, begin, end):
        url = self.base_url + 'clients/' + self.account + '/devices/' + self.number + '/public?begin=' + str(
            begin) + '&end=' + str(int(end)) + '&order=asc' + self.parameter
        r = requests.get(url, headers=self.headers)
        datapoints = r.json().get('datapoints', None)
        ha, hm, hmi, ia, im, imi, pa, pm, pmi, ta, tm, tmi, sun = [], [], [], [], [], [], [], [], [], [], [], [], []
        for i in range(30):
            ha.append(None)
            hm.append(None)
            hmi.append(None)
            ia.append(None)
            im.append(None)
            imi.append(None)
            pa.append(None)
            pm.append(None)
            pmi.append(None)
            ta.append(None)
            tm.append(None)
            tmi.append(None)
            sun.append(None)
        ti = self.getDay()
        data = {'humidity': {'average': ha, 'max': hm, 'min': hmi},
                'illumination': {'average': ia, 'max': im, 'min': imi},
                'pressure': {'average': pa, 'max': pm, 'min': pmi},
                'temperature': {'average': ta, 'max': tm, 'min': tmi},
                'date': ti,
                'sunshine': sun}
        for i in range(len(tmi)):
            for j in range(len(datapoints)):
                timeArray = time.localtime(datapoints[j]['created_at'])
                t = time.strftime("%Y-%m-%d", timeArray)[5:11]
                if ti[i] == t:
                    data['humidity']['average'][i] = datapoints[j]['data']['humidity']['average']
                    data['humidity']['max'][i] = datapoints[j]['data']['humidity']['max']
                    data['humidity']['min'][i] = datapoints[j]['data']['humidity']['min']
                    data['illumination']['average'][i] = datapoints[j]['data']['illumination']['average']
                    data['illumination']['max'][i] = datapoints[j]['data']['illumination']['max']
                    data['illumination']['min'][i] = datapoints[j]['data']['illumination']['min']
                    data['pressure']['average'][i] = datapoints[j]['data']['pressure']['average']
                    data['pressure']['max'][i] = datapoints[j]['data']['pressure']['max']
                    data['pressure']['min'][i] = datapoints[j]['data']['pressure']['min']
                    data['temperature']['average'][i] = datapoints[j]['data']['temperature']['average']
                    data['temperature']['max'][i] = datapoints[j]['data']['temperature']['max']
                    data['temperature']['min'][i] = datapoints[j]['data']['temperature']['min']
                    data['sunshine'][i] = int(datapoints[j]['data']['sunshine'] / 3600)
        return data

    # 查询设备期间数据  年
    def queryEquipmentStaYear(self, year):
        ha, hm, hmi, ia, im, imi, pa, pm, pmi, ta, tm, tmi = [], [], [], [], [], [], [], [], [], [], [], []
        t, humidityAve, humidityMax, humidityMin, illuminationAve, illuminationMax, illuminationMin, pressureAve, pressureMax, pressureMin, temperatureAve, temperatureMax, temperatureMin = [], [], [], [], [], [], [], [], [], [], [], [], []
        for i in range(365):
            ha.append(None)
            hm.append(None)
            hmi.append(None)
            ia.append(None)
            im.append(None)
            imi.append(None)
            pa.append(None)
            pm.append(None)
            pmi.append(None)
            ta.append(None)
            tm.append(None)
            tmi.append(None)
        date = self.getYear()
        for y in year:
            url = self.base_url + 'clients/' + self.account + '/devices/' + self.number + '/public?begin=' + str(
                y[0]) + '&end=' + str(y[1]) + '&order=asc' + self.parameter
            r = requests.get(url, headers=self.headers)
            datapoints = r.json().get('datapoints', None)
            for j in range(len(datapoints)):
                timeArray = time.localtime(datapoints[j]['created_at'])
                revTime = time.strftime("%Y-%m-%d", timeArray)[2:11]
                t.append(revTime)
                humidityAve.append(datapoints[j]['data']['humidity']['average'])
                humidityMax.append(datapoints[j]['data']['humidity']['max'])
                humidityMin.append(datapoints[j]['data']['humidity']['min'])
                illuminationAve.append(datapoints[j]['data']['illumination']['average'])
                illuminationMax.append(datapoints[j]['data']['illumination']['max'])
                illuminationMin.append(datapoints[j]['data']['illumination']['min'])
                pressureAve.append(datapoints[j]['data']['pressure']['average'])
                pressureMax.append(datapoints[j]['data']['pressure']['max'])
                pressureMin.append(datapoints[j]['data']['pressure']['min'])
                temperatureAve.append(datapoints[j]['data']['temperature']['average'])
                temperatureMax.append(datapoints[j]['data']['temperature']['max'])
                temperatureMin.append(datapoints[j]['data']['temperature']['min'])
        for i in range(len(date)):
            for j in range(len(t)):
                if t[j] == date[i]:
                    ha[i] = humidityAve[j]
                    hm[i] = humidityMax[j]
                    hmi[i] = humidityMin[j]
                    ia[i] = illuminationAve[j]
                    im[i] = illuminationMax[j]
                    imi[i] = illuminationMin[j]
                    pa[i] = pressureAve[j]
                    pm[i] = pressureMax[j]
                    pmi[i] = pressureMin[j]
                    ta[i] = temperatureAve[j]
                    tm[i] = temperatureMax[j]
                    tmi[i] = temperatureMin[j]
        data = {'humidity': {'average': ha, 'max': hm, 'min': hmi},
                'illumination': {'average': ia, 'max': im, 'min': imi},
                'pressure': {'average': pa, 'max': pm, 'min': pmi},
                'temperature': {'average': ta, 'max': tm, 'min': tmi},
                'date': date}
        return data

    def getlivePic(self):
        end = int(time.time())
        begin = end - 604800 - 1
        url = self.base_url + 'clients/' + self.account + '/devices/' + self.number + '/datapoints/time?begin=' + str(
            begin) + '&end=' + str(end) + '&encoding=json' + self.parameter
        r = requests.get(url, headers=self.headers)
        data = {'createTime': [], 'image': [], 'latestPic': ''}
        datapoints = r.json().get('datapoints', None)
        for d in range(len(datapoints)):
            if 'image' in datapoints[d]['data'].keys():
                timeArray = time.localtime(datapoints[d]['created_at'])
                revTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                data['latestPic'] = revTime
                break
        for d in range(len(datapoints)):
            if 'image' in datapoints[d]['data'].keys():
                timeArray = time.localtime(datapoints[d]['created_at'])
                revTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                data['createTime'].append(revTime)
                data['image'].append(datapoints[d]['data']['image'])
                if len(data['createTime']) == 12:
                    break
        return data

    def downloadImg(self):
        path = 'C:\\Users\\A07\Desktop\\商用传感器数据\\扶绥FM1摄像头\\图像'
        # end = int(time.time())
        # begin = end - 604800 - 1
        begin = 1600001224
        end = begin + 604800-1
        for i in range(1):
            url = self.base_url + 'clients/' + self.account + '/devices/' + self.number + '/datapoints/time?begin=' + str(
                begin) + '&end=' + str(end) + '&encoding=json' + self.parameter
            r = requests.get(url, headers=self.headers)
            datapoints = r.json().get('datapoints', None)
            if datapoints != None:
                for d in range(len(datapoints)):
                    if 'image' in datapoints[d]['data'].keys():
                        timeArray = time.localtime(datapoints[d]['created_at'])
                        revTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                        revTime = revTime[0:4] + revTime[5:7] + revTime[8:10] + revTime[11:13] + revTime[
                                                                                                 14:16] + revTime[17:19]
                        imgUrl = datapoints[d]['data']['image']
                        response = req.get(imgUrl)  # 将这个图片保存在内存
                        # 得到这个图片的base64编码
                        ls_f = base64.b64encode(BytesIO(response.content).read()).decode('utf-8')
                        # 打印出这个base64编码
                        # print(ls_f)
                        print(revTime)
                        #########################
                        # 下面是将base64编码进行解码
                        imgdata = base64.b64decode(ls_f)
                        # 将它用写入一个图片文件即可保存
                        file = open(path + "\\" + revTime + '.jpg', 'wb')
                        file.write(imgdata)
                        # 关闭这个文件
                        file.close()
            begin = end+1
            end = begin + 604800-1
            print('***************************************************************************************')
            print(begin,end)


if __name__ == '__main__':
    test = getCameraData()
    # test.downloadImg()
