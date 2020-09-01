from flask import g
from flask_restful import reqparse, Resource, fields, marshal
from Apps.apis.common.user.user_utils import login_required
from config import DB_URI
from sqlalchemy import create_engine
eng = create_engine(DB_URI)
from wand.image import Image
import os

parser = reqparse.RequestParser()
parser.add_argument("username", type=str)

tifPath = "D:/tifPath/"
imgPath = "D:/imgPath/"

def get_imlist(path):
    """返回目录中所有tif图像的文件名列表"""
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith(".tif")]

class imgDisplay(Resource):
    # @login_required
    def get(self):
        rank = 1#g.user.rank
        if rank:
            listdir = get_imlist(tifPath)
            for dir in listdir:
                print(dir)
                with Image(filename=dir) as img:
                    # img.resize(4096, 4096)  # width, height
                    # 存的目录为"G:/Test/6-28/HBsAg_png/",用了一步replace，换了个目录
                    imgdir = dir[0:3]+"img"+dir[6:]
                    print(imgdir)
                    img.save(filename=(imgdir[:-3] + 'jpg'))
        # from osgeo import gdal
        # file_path = tifPath+"test.tif"
        # ds = gdal.Open(file_path)
        # driver = gdal.GetDriverByName('png')
        # dst_ds = driver.CreateCopy(tifPath+'example.png', ds)
        # print(dst_ds)
        # dst_ds = None
        # src_ds = None
