from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget, QPushButton, QSizePolicy, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QMouseEvent
from UI.HistoryControl import HistoryControl
import cv2
from PIL import Image, ImageQt
import ImageTools
'''
此控件包含一个主imagewindow和一个副imagewindow,当风格化时开启副窗
主窗初始设置

'''
class ImageWindow(QWidget):
    __width: int
    __height: int
    img_path: str = ""
    img_size_status = 0
    img_crop_status = False
    layout: QHBoxLayout

    img_original: QLabel
    img_style: QLabel
    pixmap_original: QPixmap
    pixmap_style: QPixmap
    crop_start: tuple
    crop_end: tuple

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.history_ctrl = HistoryControl()
        self.__width = self.parent().width()
        self.__height = self.parent().height() - 60
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        # self.layout.setContentsMargins(60, 20, 20, 20)
        self.setLayout(self.layout)
        self.img_original = QLabel(self)
        self.img_original.setAlignment(Qt.AlignCenter)
        # self.img_original.setAlignment(132)
        self.layout.addWidget(self.img_original)
        self.setGeometry(0, 60, self.__width, self.__height)



    def mousePressEvent(self, e: QMouseEvent):
        if self.img_crop_status:
            self.crop_start = e.pos()
    def mouseReleaseEvent(self, e: QMouseEvent):
        if self.img_crop_status:
            self.crop_end = e.pos()
            self.img_crop_status = False
            self.crop_exec(self.crop_start, self.crop_end)

    def draw_img_path(self, img_path):
        if img_path != "":
            self.pixmap_original = QPixmap(img_path)
            self.img_original.setPixmap(self.pixmap_original)

    def draw_img(self, img: Image, img_box: QLabel):
        self.pixmap_original = ImageQt.toqpixmap(img)
        img_box.setPixmap(self.pixmap_original)

    def on_image_open(self, open_image_url: str):
        # opencv 打开中文有问题,而pillow已经集成了qt转换器ImageQt,但是有些图片打开失败!!???
        # img = cv2.imread(open_image_url, cv2.IMREAD_UNCHANGED)
        # img = ImageTools.cv_imread(open_image_url)
        img = Image.open(open_image_url)
        self.img_size_status = 0
        print(open_image_url)
        self.img_path = open_image_url
        self.history_ctrl.clear()  # 新的图片要清空历史
        self.update_display(img, "打开 %s" % self.img_path[self.img_path.rfind('/') + 1:])

    def update_display(self, img: Image, descp: None):
        self.history_ctrl.push(img, descp)
        self.draw_img(img, self.img_original)
        self.parent().menubar.toggle_btn()

    def on_window_resize(self, w, h):
        self.setFixedSize(w - 300, h - 60)


    def save_image(self):
        question_result = QMessageBox.question(self, "当前编辑图像会覆盖原图", "是否覆盖？",
                                               QMessageBox.StandardButtons(QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel))
        if question_result == QMessageBox.Yes:
            img, descp = self.history_ctrl.current()
            img.save(self.img_path, quality=95)

    def save_other(self, des_path):
        img, descp = self.history_ctrl.current()
        img.save(des_path, quality=95)

    def zoom_in(self):
        if not self.img_path:
            return
        self.img_size_status += 1
        img = self.pixmap_original
        if self.img_size_status > 0:
            img = img.scaled(img.size() * 1.25**self.img_size_status, 1, 1)
        elif self.img_size_status < 0:
            img = img.scaled(img.size() * 0.8 ** (-self.img_size_status), 1, 1)
        self.img_original.setPixmap(img)

    def zoom_out(self):
        if not self.img_path:
            return
        self.img_size_status -= 1
        img = self.pixmap_original
        if self.img_size_status > 0:
            img = img.scaled(img.size() * 1.25 ** self.img_size_status, 1, 1)
        elif self.img_size_status < 0:
            img = img.scaled(img.size() * 0.8 ** (-self.img_size_status), 1, 1)
        self.img_original.setPixmap(img)

    def crop(self):
        self.img_crop_status = not self.img_crop_status
        pass
    def crop_exec(self, s: QPoint, e: QPoint):
        # 根据图片放缩率，算出控件坐标与图片坐标关系,完成坐标转换
        # 偷懒，只考虑左上裁剪到右下的情况
        if s.x()>=e.x() or s.y()>=e.y():
            print("请从左上裁剪到右下")
            return
        s=[s.x(), s.y()]
        e=[e.x(), e.y()]
        if self.img_size_status > 0:
            scalling = 1.25**self.img_size_status
        else:
            scalling = 0.8**(-self.img_size_status)
        pixmap_size = self.pixmap_original.size()*scalling
        offset = (self.size() - pixmap_size)*0.5
        offset=[offset.width(), offset.height()]
        crop_s = list(map(lambda x: int((x[0] - x[1])/scalling), zip(s, offset)))
        crop_e = list(map(lambda x: int((x[0] - x[1])/scalling), zip(e, offset)))
        print("widget", self.width(), self.height(), s, e)
        print("offset", offset)
        print("image", self.pixmap_original.size(), crop_s, crop_e)

        # 裁剪坐标范围从0到size,偷懒忽略了
        # crop_s = [0 if i<0 else i for i in crop_s]
        # crop_e = [0 if i<0 else i for i in crop_e]
        img, descp = self.history_ctrl.current()
        print("image in his", img.size,"crop",crop_s[0], crop_s[1], crop_e[0], crop_e[1])
        img = img.crop((crop_s[0], crop_s[1], crop_e[0], crop_e[1]))
        self.update_display(img, "crop")



    def undo(self):
        self.history_ctrl.undo()
        img, descp = self.history_ctrl.current()
        self.draw_img(img, self.img_original)
        pass
    def redo(self):
        self.history_ctrl.redo()
        img, descp = self.history_ctrl.current()
        self.draw_img(img, self.img_original)
        pass

