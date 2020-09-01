from flask_restful import Api

from Apps.apis.common.largeSizeImageDisplay.imageDisplayApi import imgDisplay

imageDisplayApi = Api(prefix="/cms")
#get
imageDisplayApi.add_resource(imgDisplay, "/imgDisplayApi/")