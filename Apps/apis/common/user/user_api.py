import uuid

from flask import g, request
from flask_restful import reqparse, Resource, fields, marshal
from method_decorator import method_decorator

from Apps.apis.common.user.user_utils import login_required
from Apps.ext import cache
from config import DB_URI
from sqlalchemy import create_engine

eng = create_engine(DB_URI)

parser = reqparse.RequestParser()
parser.add_argument("username", type=str)
parser.add_argument("password", type=str)

usrI_fields = {'roles': fields.List(fields.String),
               'introduction': fields.String,
               'avatar': fields.String,
               'name': fields.String}
usrInfo_fields = {'code': fields.Integer,
                  'data': fields.Nested(usrI_fields)}

usrl_fields = {"token": fields.String}
usrLogin_field = {"code": fields.Integer,
                  "data": fields.Nested(usrl_fields)}

usrIsE_fields = {'exsit': fields.Integer}
userIsExist_fields = {'code': fields.Integer, 'data': fields.Nested(usrIsE_fields)}
socket_fields = {'code':fields.Integer,'data':fields.String}


class tokens(Resource):
    @login_required
    def get(self):
        rank = g.user.rank
        if rank:
            with eng.connect() as con:
                res = con.execute("select * from cms_user")
                users = {}
                d = {}
                token = {'token': fields.String}
                for row in res:
                    d[row.rank] = fields.Nested(token)
                    users[row.rank] = {"token": row.rank + "-token"}
            print(users)
            print(d)
            return marshal(users, d)


class userInfo(Resource):
    method_decorators = [login_required]

    def __init__(self):
        self.roles = []

    def get(self):
        rank = g.user.rank
        id = g.user.id
        if rank and id:
            with eng.connect() as con:
                res = con.execute("select * from cms_user where rank=" + "'" + rank + "' and id=" + str(id)).fetchone()
                if ',' in res.role:
                    for i in res.role.split(','):
                        self.roles.append(i)
                else:
                    self.roles.append(res.role)
                data = {'code': 200,
                        'data': {'roles': self.roles,
                                 'introduction': res.introduction,
                                 'avatar': res.avatar,
                                 'name': res.username}}
            data = marshal(data, usrInfo_fields)
            return data


class userIsExist(Resource):

    def get(self):
        args = parser.parse_args()
        username = args.get("username")

        if username:
            with eng.connect() as con:
                res = con.execute("select*from cms_user where username=" + "'" + username + "'").fetchone()
                if res.rowcount:
                    return marshal({'code': 200, 'data': {'exsit': 0}}, userIsExist_fields)
                else:
                    return marshal({'code': 200, 'data': {'exsit': 1}}, userIsExist_fields)


class userLogin(Resource):

    def post(self):
        args = parser.parse_args()
        username = args.get("username")
        password = args.get("password")
        with eng.connect() as con:
            user = con.execute("select * from cms_user where username = " + "'" + username + "'").fetchone()
            if user and password == user.password:
                uid = str(uuid.uuid4()).replace("-", "")
                cache.set(uid, (user.rank, user.id), timeout=24*60*60*30)
                con.execute(
                    "update cms_user set token = " + "'" + uid + "'" + " where username = " + "'" + user.username + "'")
                data = {'code': 200,
                        'data': {'token': uid}}
                return marshal(data, usrLogin_field)


class getSocketUrl(Resource):
    @login_required
    def get(self):
        rank = g.user.rank
        if rank:
            data = {'code':200,'data':'http://127.0.0.1:5000/socketio'}
            return marshal(data,socket_fields)

class logout(Resource):
    @login_required
    def get(self):
        rank = g.user.id
        if rank:
            with eng.connect() as con:
                res = con.execute("update cms_user set token = " + "'"+''+"'" + " where id = " + str(rank))
                if res.rowcount:

                    return 'ok'
