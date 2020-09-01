# -*- coding: utf-8 -*-
from flask_restful import Api
cms_api = Api(prefix="/cms")

from Apps.apis.common.amap_about import amapAbout_api
from Apps.apis.common.devGroups import devGroupApi
from Apps.apis.common.device_list import devlistApi
from Apps.apis.common.dp import dp_api
from Apps.apis.common.plot import plot_api
from Apps.apis.common.historydata import historydata_api
from Apps.apis.common.user import user_api
from Apps.apis.common.table import table_api
from Apps.apis.common.pictureUpload import picUploadApi
from Apps.apis.common.chartDisplay import getChartDataApi
# from Apps.apis.common.largeSizeImageDisplay import imageDisplayApi


def api_init(app):
    amapAbout_api.init_app(app)
    devGroupApi.init_app(app)
    devlistApi.init_app(app)
    dp_api.init_app(app)
    plot_api.init_app(app)
    historydata_api.init_app(app)
    user_api.init_app(app)
    table_api.init_app(app)
    picUploadApi.init_app(app)
    getChartDataApi.init_app(app)
    # imageDisplayApi.init_app(app)
