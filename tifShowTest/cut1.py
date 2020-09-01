import cv2
import gdal
import numpy as np
import pandas as pd
import csv


class UseCv:
    def __init__(self):
        self.path = r'E:\tifPath\1.tif'

    def cut(self):
        img = cv2.imread(self.path, flags=cv2.IMREAD_COLOR)
        h = int(img.shape[0])
        w = int(img.shape[1])
        img = cv2.resize(img,(h,w))
        cv2.imshow("1",img)

        cv2.namedWindow('roi', 0)
        bbox = cv2.selectROI(windowName='roi', img=img, showCrosshair=False, fromCenter=False)
        cut1 = img[bbox[1]:bbox[1] + bbox[3], bbox[0]:bbox[0] + bbox[2]]
        cv2.imwrite('cut1.tif', cut1)

    def readTif(self, fileName):
        dataset = gdal.Open(fileName)

        if dataset == None:
            print(fileName + "文件无法打开")
            return
        im_width = dataset.RasterXSize  # 栅格矩阵的列数
        im_height = dataset.RasterYSize  # 栅格矩阵的行数
        im_bands = dataset.RasterCount  # 波段数
        band1 = dataset.GetRasterBand(1)
        print(band1)
        print('Band Type=', gdal.GetDataTypeName(band1.DataType))
        im_data = dataset.ReadAsArray(0, 0, im_width, im_height)  # 获取数据
        im_geotrans = dataset.GetGeoTransform()  # 获取仿射矩阵信息
        im_proj = dataset.GetProjection()  # 获取投影信息
        im_blueBand = im_data[0, 0:im_height, 0:im_width]  # 获取蓝波段
        im_greenBand = im_data[1, 0:im_height, 0:im_width]  # 获取绿波段
        im_redBand = im_data[2, 0:im_height, 0:im_width]  # 获取红波段
        im_nirBand = im_data[3, 0:im_height, 0:im_width]  # 获取近红外波段

        return (im_width, im_height, im_bands, im_data, im_geotrans
                , im_proj, im_blueBand, im_greenBand, im_redBand, im_nirBand)


if __name__ == '__main__':
    u = UseCv()
    # u.readTif(r'E:\tifPath\1.tif')
    u.cut()
