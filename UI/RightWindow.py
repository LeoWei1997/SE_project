from PyQt5.QtWidgets import QWidget, QPushButton, QSizePolicy, QVBoxLayout, \
    QHBoxLayout, QGridLayout, QLabel, QButtonGroup, QScrollArea
from PyQt5.QtGui import QIcon, QPixmap


class RightWindow(QWidget):
    status = False
    __width = 300
    layout = QVBoxLayout()

    close_btn: QPushButton
    style_transfer_btn: QPushButton
    face_swap_btn: QPushButton
    object_recog_btn: QPushButton

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.__height = self.parent().height() - 60
        print(self.__height)
        self.setGeometry(self.parent().width() - self.__width, 60, self.__width, self.__height)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # self.setVisible(False)
        self.draw_right_window()
        print(self.width(),self.height())

    def draw_right_window(self):
        self.layout.setSpacing(1)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # self.setStyleSheet("*{background-color: #f2f2f2;} QLabel{  \
        #                                         padding-top: 10px;    \
        #                                         padding-left: 22px;  \
        #                                         padding-bottom: 10px;\
        #                                         font-size: 16px;     \
        #                                         color: #6c6c6c;      \
        #                                     }")
        self.setLayout(self.layout)
        self.draw_title(self.layout)
        self.draw_content(self.layout)


    def draw_title(self, layout):
        title_label = QLabel("编辑", self)
        title_label.setObjectName("edit_label")
        # title_label.setStyleSheet("QLabel{font-size: 24px;width: 300px;height: 50px}")
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(title_label)

    def draw_content(self, layout):
        style_box = QWidget(self)
        style_box.setMinimumSize(self.__width, 120)
        grid = QGridLayout(style_box)
        style_trans = QLabel("风格转换", self)
        style_trans.setObjectName("style_label")
        grid.addWidget(style_trans, 0, 0, 1, 3)
        styles = ['星空', '向日葵', '浪花', '壁画', 'xx', 'wtf', 'damn', '自定义']
        for i, style in enumerate(styles):
            style_btn = QPushButton(QIcon('./resource/QQ.png'), '', style_box)
            style_btn.setFixedSize(70, 70)
            style_btn.clicked.connect(self.make_calluser(style))  # 自定义的回调函数工厂
            row, col = divmod(i, 3)  # 三个一行
            grid.addWidget(style_btn, row + 1, col)
        style_box.setLayout(grid)

        # 加入滚动条
        # scroll = QScrollArea()
        # scroll.setWidget(style_box)
        # layout.addWidget(scroll)

        layout.addWidget(style_box)



        face_swap = QLabel("人脸识别", self)
        face_swap.setObjectName("face_label")
        layout.addWidget(face_swap)

        object_detc = QLabel("物体识别", self)
        object_detc.setObjectName("object_label")
        object_detc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(object_detc)

    def make_calluser(self, style):
        def calluser():
            print(style)
            # set style here......
        return calluser

    def on_window_resize(self, w, h):
        # if self.status:
        #     self.setGeometry(w - self.__width, 60, self.__width, self.__height)
        self.setGeometry(w - self.__width, 60, self.__width, self.__height)

