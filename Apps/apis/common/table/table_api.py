from flask import g
from flask_restful import Resource, fields, marshal

from Apps.apis.common.user.user_utils import login_required
from config import DB_URI
from sqlalchemy import create_engine
eng = create_engine(DB_URI)


item_fields = {'id':fields.Integer,
               'title':fields.String,
               'status':fields.List(fields.String),
               'author':fields.String,
               'display_time':fields.DateTime(dt_format='iso8601'),
               'pageviews':fields.String}

items_fields = {'code':fields.Integer,'data':fields.List(fields.Nested(item_fields))}


class tableData(Resource):
    def __init__(self):
        self.status = []
        self.items = []
    @login_required
    def get(self):
        rank = g.user.rank
        if rank:
            with eng.connect() as con:
                res = con.execute("select*from table_t")
                for row in res:
                    self.status = []
                    for i in row.status.split(','):
                        self.status.append(i)
                    item = {'id':row.id,
                            'title':row.title,
                            'status':self.status,
                            'author':row.author,
                            'display_time':row.display_time,
                            'pageviews':row.pageviews}
                    self.items.append(item)
            tabledata = {"code":200,"data":self.items}
            data = marshal(tabledata,items_fields)
            return data