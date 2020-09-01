from flask_restful import Api

from Apps.apis.common.user.user_api import userLogin,tokens,userInfo,userIsExist,getSocketUrl,logout

user_api = Api(prefix="/cms")
user_api.add_resource(tokens, "/tokensApi/")   #未用到
user_api.add_resource(userInfo, "/userInfoApi/")
user_api.add_resource(userIsExist, "/userIsExist/")
user_api.add_resource(getSocketUrl, "/getSocketUrl/")
#post
user_api.add_resource(userLogin, "/userLoginApi/")
user_api.add_resource(logout, "/logout/")