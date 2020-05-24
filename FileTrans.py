# 客户端收发
import requests
import json
import base64
from io import BytesIO
from PIL import Image

class FileTrans(object):
    # PIL图像转base64, 内存中编解码都要通过BytesIO对象来操作, 磁盘中图片直接调用tobytes方法
    def img2byte(self, img: Image):
        buffer = BytesIO()
        if img.mode != 'RGB':
            print("非RGB图像")
            img = img.convert('RGB')
        img.save(buffer, format='JPEG')
        img_byte = buffer.getvalue()
        img_base64 = base64.b64encode(img_byte)
        img_str = bytes.decode(img_base64)  # 还要转换成str
        return img_str

    # base64转PIL图像
    def byte2img(self, img_str):
        img_base64 = str.encode(img_str)
        img_byte = base64.b64decode(img_base64)
        img = BytesIO(img_byte)
        img = Image.open(img)
        return img

    def send_st(self, address, tag: int, img: Image):
        # address = ip:port, tag表示风格号
        img_base64 = self.img2byte(img)
        data = {'tag': tag, 'img': img_base64}
        json_data = json.dumps(data)
        url = 'http://' + address + '/style_transfer/'
        try:
            res = requests.post(url=url, data=json_data)
            print(res.text)
        except:
            print("Failed to send")

    def send_fs(self, address: str, face1: Image, face2: Image):
        # return None
        face1, face2 = self.img2byte(face1), self.img2byte(face2)
        data = {'face1': face1, 'face2': face2}
        json_data = json.dumps(data)
        url = 'http://' + address + '/face_swap/'
        try:
            res = requests.post(url=url, data=json_data)
            print(res.text)
        except:
            print("Failed to send")
        return None

    def wait_receive(self):
        # 接受服务器返回的数据, 用socket监听??
        pass
