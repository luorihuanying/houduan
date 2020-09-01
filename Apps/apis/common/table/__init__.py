from flask_restful import Api

from Apps.apis.common.table.table_api import tableData

table_api = Api(prefix="/cms")
table_api.add_resource(tableData, "/tableDataApi/")    #未用到
