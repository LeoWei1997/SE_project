from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QWidget, \
    QMessageBox, QDesktopWidget, QFileDialog

from UI.ImageWindow import ImageWindow
from UI.MenuBar import MenuBar
from UI.RightWindow import RightWindow
from UI.dialog.FileDialog import FileDialog
from UI.qss.QSSReader import QSSReader


class MainWindow(QMainWindow):
    __width = 1300
    __height = 900
    __min_width = 480
    __min_height = 600
    __window_title = "图骗"
    __icon = "resource/dingdangmao.png"
    __cur_image = ''

    file_dialog: QFileDialog  # 图片打开和储存
    menubar: QWidget  # 顶部菜单栏
    image_window: QWidget  # 图片窗口
    right_window: QWidget  # 侧边窗口

    __resize_sig = QtCore.pyqtSignal(int, int)  # get reshape ev's width and height
    saved = True

    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_window()

    def init_window(self):
        self.resize(self.__width, self.__height)
        self.setWindowIcon(QIcon(self.__icon))
        self.set_window_title()
        self.set_window_center()
        self.setStyleSheet(QSSReader.read_qss("./UI/qss/mainwindow.qss"))
        self.setMinimumWidth(self.__min_width)
        self.setMinimumHeight(self.__min_height)
        self.setFont(QFont("Microsoft YaHei UI"))

        self.image_window = ImageWindow(self)
        self.right_window = RightWindow(self)
        self.file_dialog = FileDialog(self)
        self.menubar = MenuBar(self)
        self.image_window.setObjectName("image_window")
        self.right_window.setObjectName("right_window")
        self.menubar.setObjectName("menubar")

        self.__resize_sig.connect(self.menubar.on_window_resize)
        self.__resize_sig.connect(self.image_window.on_window_resize)
        self.__resize_sig.connect(self.right_window.on_window_resize)

    def set_window_center(self):
        screen = QDesktopWidget().screenGeometry()
        self.move((screen.width() - self.__width) >> 1,
                  (screen.height() - self.__height) >> 1)

    def set_window_title(self):
        if self.__cur_image == '':
            self.setWindowTitle(self.__window_title)
        else:
            self.setWindowTitle("%s - %s" % (self.__window_title,
                                self.__cur_image[self.__cur_image.rfind('/') + 1:]))

    # 主窗口获取resize事件的宽, 高
    def resizeEvent(self, ev: QtGui.QResizeEvent) -> None:
        self.__resize_sig.emit(ev.size().width(), ev.size().height())

    # 打开图片后更新主窗口显示
    def update_open_image(self, open_image_url: str):
        self.__cur_image = open_image_url
        self.set_window_title()
        self.saved = True

    # 关闭程序先检查是否已保存
    def closeEvent(self, ev: QtGui.QCloseEvent) -> None:
        if not self.saved:
            confirm = QMessageBox.question(self, "是否退出", "当前所做的修改将会丢失", QMessageBox.Yes | QMessageBox.Cancel)
            if confirm == QMessageBox.Yes:
                ev.accept()
            else:
                print(confirm)
                ev.ignore()

    def imageEditEvent(self):
        self.saved = False

    def imageSaveEvent(self, img_path):
        self.saved = True
        if type(img_path) == type("str"):
            self.update_open_image(img_path)



