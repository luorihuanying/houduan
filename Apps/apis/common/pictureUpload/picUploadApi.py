import os
from flask import request
from flask_restful import Resource, fields, marshal

successFlag_fields = {'code': fields.Integer,
                      'name': fields.String,
                      'url': fields.String}

imgPath = './Apps/static/image/'


class picUpload(Resource):
    def __init__(self):
        self.name = []
        if len(os.listdir(imgPath)):
            for filename in os.listdir(imgPath):
                self.name.append(int(os.path.join(filename[:-4])))
        else:
            self.name.append(0)

    def post(self):
        file = request.files.get("file")
        if file:
            self.name.sort()
            imgName = self.name[-1] + 1
            file.save(os.path.join(imgPath, str(imgName) + ".jpg"))
            return marshal(
                {'code':200,'name': str(imgName) + '.jpg', 'url': 'http://127.0.0.1:5000/static/image/' + str(imgName) + '.jpg'},
                successFlag_fields)
