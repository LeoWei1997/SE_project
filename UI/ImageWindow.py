from PyQt5.QtWidgets import QWidget, QPushButton, QSizePolicy, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QImage
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
    # right_wnd_open = False
    layout: QHBoxLayout

    img_original: QLabel
    img_style: QLabel
    pixmap_original: QPixmap
    pixmap_style: QPixmap

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
        self.layout.addWidget(self.img_original)
        self.setGeometry(0, 60, self.__width, self.__height)

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
        print(open_image_url)
        self.img_path = open_image_url
        self.history_ctrl.clear()  # 新的图片要清空历史
        self.history_ctrl.push(img, "打开 %s" % self.img_path[self.img_path.rfind('/') + 1:])
        # self.draw_img(ImageTools.cv2QImage(img))
        self.draw_img(img, self.img_original)
        self.parent().menubar.toggle_btn()

    def on_window_resize(self, w, h):
        self.setFixedSize(w - 300, h - 60)


    def save_image(self):
        pass
    def save_other(self):
        pass
    def zoom_in(self):
        # img, descp = self.history_ctrl.current()
        pass
    def zoom_out(self):
        pass
    def crop(self):
        pass
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

