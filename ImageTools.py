import cv2
import numpy as np
from PyQt5.QtGui import QImage

def cv_imread(img_path):
    # opencv读不了中文路径
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
    return img

# opencv 读取的图片是np矩阵
def cv2QImage(img: np.ndarray):
    height, width, channel = img.shape[0], img.shape[1], img.shape[2]
    print(channel)
    if channel == 0:
        print(img)
        img = QImage(img, width, height, width, QImage.Format_Grayscale8)
    elif channel == 3:
        img = QImage(img.data, width, height, width * 3, QImage.Format_RGB888).rgbSwapped()
    elif channel == 4:
        img = QImage(img.data, width, height, width * 4, QImage.Format_RGBA8888).rgbSwapped()
    else:
        print("Invalid image type")
        img = QImage(img.data, width, height, width, QImage.Format_Invalid)
    return img