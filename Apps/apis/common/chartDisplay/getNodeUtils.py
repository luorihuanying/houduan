import datetime
import hashlib
import json
import numpy as np
import random

import requests

from config import DB_URI
from sqlalchemy import create_engine

eng = create_engine(DB_URI)


class getNode():
    base_url = 'https://cloudapi.usr.cn/usrCloud'
    account = 'gxu621'
    row_md5 = hashlib.md5('qwertyuiop'.encode('utf-8')).hexdigest()

    def __init__(self):
        self.token = self.get_token()

    @staticmethod
    def error_code(code):
        if code is None:
            return False

        if code == 0:
            return True
        return False

    @staticmethod
    def get_user_agent():
        user_agent = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
            "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
        ]
        return random.choice(user_agent)

    @property
    def headers(self):
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': self.get_user_agent()
        }
        return headers

    def get_token(self):
        url = '/user/login'
        url = self.base_url + url
        r = requests.post(url, json={'account': self.account, 'password': self.row_md5}, headers=self.headers)
        if r.status_code != 200:
            raise ValueError('连接无效!')
        elif self.error_code(r.json().get('status', None)):
            data = r.json().get('data', None)
            if data:
                return data.get('token')
        else:
            raise ValueError('无法获取token')

    def getInfo(self):
        devId = '00016720001234567893'
        url = self.base_url+'/dev/getOnlineDevicesByUid'
        r = requests.post(url, json={'devIds': [devId], 'token': self.token}, headers=self.headers)
        if r.status_code == 200:
            state = r.json().get('data', None)[0]['state']
            if state == 0:
                state = '离线'
            else:
                state = '在线'
        with eng.connect() as con:
            res = con.execute('select createTime from historydatas order by id desc limit 1')
            for row in res:
                latestTime = row.createTime
        return {'state':state,'latestTime':latestTime,'devId':devId}

    def newtestHis(self):
        container = []
        label = ['h10', 'h20', 'h30', 'v20']
        with eng.connect() as con:
            for i in label:
                temp = []
                res = con.execute('select * from historydatas where dataPointName = %s order by id desc limit 8', (i))
                if res.rowcount:
                    for row in res:
                        temp.append(
                            {'createTime': row.createTime, 'dataPointName': row.dataPointName, 'value': row.value})
                container.append(temp)
        return container

    def getIotDayData(self):
        label = ['h10','h20','h30','v20']
        endTime = []
        startTime = []

        dict = {'h10':{},'h20':{},'h30':{},'v20':{}}
        with eng.connect() as con:
            for i in label:
                res = con.execute('select createTime from historydatas where dataPointName=%s order by id desc limit 1',(i))
                for row in res:
                    endTime.append(row.createTime)
            for i in endTime:
                t=(i+datetime.timedelta(days=-1)).strftime("%Y-%m-%d %H:%M:%S")
                startTime.append(t)
            for i in range(len(label)):
                t = []
                r = []
                res = con.execute('select createTime,value from historydatas where dataPointName=%s and createTime between %s and %s ',(label[i],str(startTime[i]),str(endTime[i]))).fetchall()
                for row in res:
                    value = row.value
                    if value == 'nan':
                        value = None
                    t.append(str(row.createTime)[11:16])
                    r.append(value)
                dict[label[i]]={'createTime':t,'value':r}
            return dict

    def getIotWeekData(self):
        label = ['h10', 'h20', 'h30', 'v20']
        endTime = []
        dict = {'h10':{},'h20':{},'h30':{},'v20':{}}
        with eng.connect() as con:
            for i in label:
                res = con.execute('select createTime from historydatas where dataPointName=%s order by id desc limit 1',(i))
                for row in res:
                    endTime.append(row.createTime)
            for i in range(len(label)):
                x = []
                avg,max,min = [],[],[]
                end = endTime[i]
                start = str(end)[:10]+' 00:00:00'
                start = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
                for j in range(7):
                    x.append(str(start)[6:11])
                    day = []
                    res = con.execute('select createTime,value from historydatas where dataPointName=%s and createTime between %s and %s ',(label[i],str(start),str(end))).fetchall()
                    end = start - datetime.timedelta(seconds=1)
                    start = start - datetime.timedelta(days=1)
                    for row in res:
                        if row.value != 'nan':
                            day.append(float(row.value))
                    if len(day):
                       avg.append(np.average(day))
                       max.append(np.max(day))
                       min.append(np.min(day))
                    else:
                       avg.append(None)
                       max.append(None)
                       min.append(None)
                ma,mi = [],[]
                for l in range(len(max)):
                    if max[l] != None:
                        ma.append(max[l])
                    if min[l] != None:
                        mi.append(min[l])
                dict[label[i]] = {'avg':avg[::-1],'max':max[::-1],'min':min[::-1],'date':x[::-1],'mi':np.min(mi),'ma':np.max(ma)}
        return dict
    def getIotMonthData(self):
        dict = {}
        label = ['h10', 'h20', 'h30', 'v20']
        with eng.connect() as con:
            for i in label:
                t = []
                v = []
                d = []
                avg = []
                max = []
                min = []
                res = con.execute('select createTime,value from historydatas where dataPointName = %s',(i))
                for row in res:
                    t.append(row.createTime)
                    v.append(row.value)
                for j in t:
                    if str(j)[5:10] not in d:
                        d.append(str(j)[5:10])
                for k in range(len(d)):
                    temp = []
                    for l in range(len(t)):
                        if d[k] == str(t[l])[5:10] and v[l] != 'nan':
                            temp.append(float(v[l]))
                    if len(temp):
                        avg.append(np.average(temp))
                        max.append(np.max(temp))
                        min.append(np.min(temp))
                    else:
                        avg.append(None)
                        max.append(None)
                        min.append(None)
                av,ma,mi = [],[],[]
                for m in range(len(min)):
                    if max[m] != None:
                        av.append(avg[m])
                        ma.append(max[m])
                        mi.append(min[m])
                dict[i] = {'date':d,'avg':avg,'max':max,'min':min,'av':np.mean(av),'ma':np.max(ma),'mi':np.min(mi)}
            return dict









if __name__ == '__main__':
    test = getNode()
    test.getIotMonthData()
