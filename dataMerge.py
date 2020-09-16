# import pandas as pd
# import os
# import warnings
# warnings.filterwarnings('ignore')
# from config import DB_URI
# from sqlalchemy import create_engine
# eng = create_engine(DB_URI)
#
#
# dir = './nodeData/'
# mergeData = pd.DataFrame(columns=('time','RSSI','Id'))
# for i in os.listdir(dir):
#     data = pd.read_excel(dir+i).iloc[:, :3]
#     data['nodeFlag'] = i[:3]
#     mergeData = pd.concat([mergeData,data],axis=0)
# mergeData.sort_values(by='time', inplace=True)
# mergeData.drop('Id',axis=1,inplace=True)
# mergeData['id'] = range(1,len(mergeData.index)+1)
# mergeData.set_index('id',inplace=True)
# count = 0
# with eng.connect() as con:
#     con.execute('truncate table historydatas')
#     for i in mergeData.index:
#         res = con.execute("insert into historydatas (devName,devId,dataPointName,createTime,value,groupName,alarm,type)"
#                           "values (%s,%s,%s,%s,%s,%s,%s,%s)",('4G模块','00016720001234567892',str(mergeData['nodeFlag'][i]),str(mergeData['time'][i]),str(mergeData['RSSI'][i]),'设备组1','1','0'))
#         if res.rowcount:
#             count = count+1
# print(count)
#
import random
n = random.randint(0,100)
m = random.randint(0,100)
def ff (n,m):
    if n%m == 0:
        return 1
    else:
        if n != 0:
            return 1
