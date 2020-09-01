from flask import request
from flask_restful import abort
from flask import g

from config import DB_URI
from sqlalchemy import create_engine
eng = create_engine(DB_URI)

from Apps.ext import cache

"""
request.form.get("key", type=str, default=None) 获取表单数据，
request.json.get("key", type=str, default=None) 获取body数据，
request.args.get("key") 获取get请求参数，
request.values.get("key") 获取所有参数。推荐使用request.values.get().
"""

def check_user():
    #未登录
    token = request.headers.get('token')
    if not token:
        data = {'code':5001,
                'msg':'Not logged in'}
        abort(data)
    user_id = cache.get(token)
    #token过期
    if not user_id:
        data = {'code': 5002,
                'msg':'Token Invalid'}
        abort(data)
    #此用户已被管理员删除
    with eng.connect() as con:
        user = con.execute("select * from cms_user where token = "+"'"+str(token)+"'").fetchone()
        if not user:
            data = {'code': 5003,
                    'msg':'User does not exist'}
            abort(data)
        g.user = user

def login_required(func):
    def wrapper(*args,**kwargs):
        check_user()
        return func(*args,**kwargs)

    return wrapper



