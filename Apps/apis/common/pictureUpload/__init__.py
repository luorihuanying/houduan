# -*- coding: utf-8 -*-
from flask_restful import Api

from Apps.apis.common.pictureUpload.picUploadApi import picUpload

picUploadApi = Api(prefix="/cms")
#post
picUploadApi.add_resource(picUpload, "/image/")
