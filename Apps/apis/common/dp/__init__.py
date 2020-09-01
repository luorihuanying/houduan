# -*- coding: utf-8 -*-
from flask_restful import Api

from Apps.apis.common.dp.dp_api import regions,createDev,updateDev,delDev,createDp,updateDp,delDp

dp_api = Api(prefix="/cms")
#get
dp_api.add_resource(regions, "/getDevsInfoList/")
#post
dp_api.add_resource(createDev, "/createDev/")
dp_api.add_resource(updateDev, "/updateDev/")
dp_api.add_resource(delDev, "/delDev/")
dp_api.add_resource(createDp, "/createDp/")
dp_api.add_resource(updateDp, "/updateDp/")
dp_api.add_resource(delDp, "/delDp/")