from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QPushButton, QSizePolicy, QVBoxLayout, \
    QHBoxLayout, QGridLayout, QLabel, QButtonGroup, QScrollArea
from PyQt5.QtGui import QIcon, QPixmap



class RightWindow(QWidget):
    status = False
    __width = 300
    layout = QVBoxLayout()
    qss = "QPushButton{background-color:rgba(100,225,100,30);\
                                                        border-style:outset;\
                                                        border-width:4px;\
                                                        border-radius:10px;\
                                                        border-color:rgba(255,255,255,30);\
                                                        font:bold 10px;\
                                                        color:rgba(0,0,0,100);\
                                                        padding:6px;\
                                                        text-align: bottom;\
                                                        }\
                                                        QPushButton:pressed{background-color:rgba(100,255,100,200);\
                                                        border-color:rgba(255,255,255,30);\
                                                        border-style:inset;\
                                                        color:rgba(0,0,0,100);\
                                                        }\
                                                        QPushButton:hover{background-color:rgba(100,255,100,100);\
                                                        border-color:rgba(255,255,255,200);\
                                                        color:rgba(0,0,0,200);\
                                                        }"

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.__height = self.parent().height() - 60
        print(self.__height)
        self.setGeometry(self.parent().width() - self.__width, 60, self.__width, self.__height)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        # self.setVisible(False)
        self.draw_right_window()
        print(self.width(),self.height())

    def draw_right_window(self):
        self.layout.setSpacing(1)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.draw_title(self.layout)
        self.draw_style_trans(self.layout)
        self.draw_face_swap(self.layout)
        self.draw_object_detect(self.layout)


    def draw_title(self, layout):
        title_label = QLabel("智能处理", self)
        title_label.setObjectName("edit_label")
        # title_label.setStyleSheet("QLabel{font-size: 24px;width: 300px;height: 50px}")
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(title_label)

    def draw_style_trans(self, layout):
        style_trans = QLabel("风格转换", self)
        style_trans.setObjectName("style_label")
        style_trans.setFixedSize(self.width(), 50)
        layout.addWidget(style_trans)
        style_box = QWidget(self)
        style_box.setMinimumWidth(self.__width)
        style_box.setMaximumHeight(270)
        grid = QGridLayout(style_box)
        # grid.addWidget(style_trans, 0, 0, 1, 3)
        styles = ['cubist', 'starry_night', 'feathers', 'mosaic', 'scream', 'udnie', 'wave', '自定义']
        for i, style in enumerate(styles):
            style_btn = QPushButton(QIcon('./resource/styles/style%d.jpg' % (i+1)), '', style_box)
            style_btn.setObjectName("%d"%i)
            style_btn.setIconSize(QSize(58, 58))
            style_btn.setStyleSheet(self.qss)
            style_btn.setFixedSize(70, 70)
            # style_btn.clicked.connect(self.make_calluser(i))  # 自定义的回调函数工厂
            # print("wtf i is %d" % i)  从0一直到7,最后停留在7,没法做到多对一映射
            # 所以不要用传参法,用self.sender(),利用sender.text()或sender.objectName()识别信号源
            # style_btn.clicked.connect(lambda: self.parent().image_window.style_trans(i))  # 不用工厂, 用lambda修饰就好了
            style_btn.clicked.connect(self.parent().image_window.style_trans)
            row, col = divmod(i, 3)  # 三个一行
            grid.addWidget(style_btn, row, col)
        style_box.setLayout(grid)

        # 如果内置风格太多,可以加入滚动条
        # scroll = QScrollArea()
        # scroll.setWidget(style_box)
        # layout.addWidget(scroll)
        layout.addWidget(style_box)

    def draw_face_swap(self, layout):
        face_swap = QLabel("人像换脸", self)
        face_swap.setObjectName("face_label")
        face_swap.setFixedSize(self.width(), 50)
        layout.addWidget(face_swap)
        face_box = QWidget(self)
        face_box.setMinimumWidth(self.__width)
        face_box.setMaximumHeight(90)
        grid = QGridLayout()
        swap_btn = QPushButton("AI换脸", face_box)
        swap_btn.setStyleSheet(self.qss)
        swap_btn.setFixedSize(120, 40)
        swap_btn.clicked.connect(self.parent().image_window.face_swap)
        grid.addWidget(swap_btn, 0, 1)
        face_box.setLayout(grid)
        layout.addWidget(face_box)

    def draw_object_detect(self, layout):
        object_detec = QLabel("物体识别", self)
        object_detec.setObjectName("object_label")
        object_detec.setFixedSize(self.width(), 50)
        layout.addWidget(object_detec)
        object_box = QWidget(self)
        object_box.setMinimumWidth(self.__width)
        object_box.setMaximumHeight(90)
        grid = QGridLayout(object_box)
        detec_btn = QPushButton("一键识别", object_box)
        detec_btn.setStyleSheet(self.qss)
        detec_btn.setFixedSize(120, 40)
        detec_btn.clicked.connect(self.parent().image_window.object_detect)
        grid.addWidget(detec_btn, 1, 1)

        cloud_btn = QPushButton("批量读图", object_box)
        cloud_btn.setStyleSheet(self.qss)
        cloud_btn.setFixedSize(120, 40)
        # cloud_btn.clicked.connect(self.parent().file_dialog.get_img_paths)
        cloud_btn.clicked.connect(lambda: self.wtf())
        grid.addWidget(cloud_btn, 1, 2)
        object_box.setLayout(grid)
        layout.addWidget(object_box)

        blank = QWidget(self)  # 填充空白的
        layout.addWidget(blank)

    def wtf(self):
        # 卧槽, 什么鬼, 上方直接写报错MainWindow没有file_dialog???!!!!
        self.parent().file_dialog.get_img_paths()

    def make_calluser(self, style: int):
        # 必须嵌套一个函数并返回这个函数, 否则直接加参数是不行的
        def calluser():
            print(style)
            self.parent().image_window.style_trans(style)
            pass
        return calluser

    def on_window_resize(self, w, h):
        self.setGeometry(w - self.__width, 60, self.__width, self.parent().height())



