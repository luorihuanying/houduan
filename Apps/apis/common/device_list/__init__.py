# -*- coding: utf-8 -*-
from flask_restful import Api

from Apps.apis.common.device_list.devlistApi import region, updateDevsInfo, deleteDev, devList1

devlistApi = Api(prefix="/cms")

devlistApi.add_resource(devList1, "/getDevsList/")
devlistApi.add_resource(region, "/getDevsCount/")
#post
devlistApi.add_resource(updateDevsInfo, "/updateDevsInfo/")
devlistApi.add_resource(deleteDev, "/deleteDev/")
