import os
import cv2 as cv
import warnings

warnings.filterwarnings('ignore')

dir = r'E:/tifPath/'
files = os.listdir(r'E:/tifPath/')
# 定义转换格式后的保存路径
ResultPath2 = "E:\\cutTif\\"
# ResultPath2 = "./RS_Cut_Result/"  # 定义裁剪后的保存路径
for file in files:  # 这里可以去掉for循环
    a, b = os.path.splitext(file)  # 拆分影像图的文件名称
    this_dir = os.path.join(dir + file)  # 构建保存 路径+文件名
    print(this_dir)
    img = cv.imread(r'E:/tifPath/1.tif', 1)  # 读取tif影像
    print(img)

    # 下面开始裁剪-不需要裁剪tiff格式的可以直接注释掉
    hight = img.shape[0]  # opencv写法，获取宽和高
    width = img.shape[1]
    # 定义裁剪尺寸
    w = 480  # 宽度
    h = 360  # 高度
    _id = 1  # 裁剪结果保存文件名：0 - N 升序方式
    i = 0
    while (i + h <= hight):  # 控制高度,图像多余固定尺寸总和部分不要了
        j = 0
        while (j + w <= width):  # 控制宽度，图像多余固定尺寸总和部分不要了
            cropped = img[i:i + h, j:j + w]  # 裁剪坐标为[y0:y1, x0:x1]
            cv.imwrite(ResultPath2 + a + "_" + str(_id) + b, cropped)
            _id += 1
            j += w
        i = i + h
