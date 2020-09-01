# -*- coding: utf-8 -*-
from flask_restful import Api

from Apps.apis.common.devGroups.devGroupApi import reg,createRegInfo,updateRegInfo,delRegInfo,updataGroupInfo,delGroupInfo,createGroupInfo

devGroupApi = Api(prefix="/cms")

devGroupApi.add_resource(reg, "/getGroupInfo/")
#post
devGroupApi.add_resource(createRegInfo, "/createRegInfo/")
devGroupApi.add_resource(updateRegInfo, "/updateRegInfo/")
devGroupApi.add_resource(delRegInfo, "/delRegInfo/")
devGroupApi.add_resource(createGroupInfo, "/createGroupInfo/")
devGroupApi.add_resource(updataGroupInfo, "/updateGroupInfo/")
devGroupApi.add_resource(delGroupInfo, "/delGroupInfo/")