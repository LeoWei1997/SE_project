from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QSizePolicy, QHBoxLayout

# 巨坑!!!stylesheet设置无效
class MenuButton(QPushButton):
    # def init_menubutton(self):
    pass

class MenuBar(QWidget):
    __height = 60
    __min_width = 670

    # 打开,保存, 放大,缩小,裁剪,撤销,重做, 另存为,关闭
    # normal: 130,90,300,90,60 = 670
    # min: 540
    image_btn: MenuButton
    save_btn: MenuButton

    zoomin_btn: MenuButton
    zoomout_btn: MenuButton
    crop_btn: MenuButton
    undo_btn: MenuButton
    redo_btn: MenuButton

    edit_btn: MenuButton
    save_other_btn: MenuButton

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.draw()
        # self.setStyleSheet("background-color: rgb(0,120,215);")

    def draw(self):
        # self.setGeometry(0, 0, self.parent().width(), 60)  # 不需要,默认顶格父控件
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # hor: expnd ver: fixed
        self.setFixedSize(self.parent().width(), self.__height)
        layout = QHBoxLayout()
        l_layout = QHBoxLayout()
        m_layout = QHBoxLayout()
        r_layout = QHBoxLayout()

        self.draw_left_layout(l_layout)
        self.draw_middle_layout(m_layout)
        self.draw_right_layout(r_layout)

        layout.addLayout(l_layout)
        layout.addStretch(1)
        layout.addLayout(m_layout)
        layout.addStretch(1)
        layout.addLayout(r_layout)
        self.setLayout(layout)
        self.layout().setContentsMargins(0, 0, 0, 0)  # 默认layout中有边框

    def draw_left_layout(self, l_layout):
        l_layout.setSpacing(0)
        # 没用MenuButton
        self.image_btn = MenuButton(QIcon("resource/edit_icon.png"), "打开图片", self)
        self.image_btn.setObjectName("image_btn")
        l_layout.addWidget(self.image_btn)
        self.image_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.image_btn.setShortcut("Ctrl+O")
        # 点击->filedialog open->file selected->Main update info & Image update img
        self.image_btn.clicked.connect(self.parent().file_dialog.open_image)
        # # 设置stylesheet无效只好用切换方案的方法
        # self.image_btn.setProperty("color", "1")
        # self.image_btn.style().polish(self.image_btn)
        print(self.image_btn.styleSheet())
        #

        # self.image_btn.setEnabled(False)
        self.save_btn = MenuButton(QIcon("./resource/save_icon.png"), "保存", self)
        self.save_btn.setObjectName("save_btn")
        l_layout.addWidget(self.save_btn)
        self.save_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.save_btn.setShortcut("Ctrl+S")
        self.save_btn.clicked.connect(self.parent().image_window.save_image)

    def draw_middle_layout(self, m_layout):
        m_layout.setSpacing(0)

        self.zoomin_btn = MenuButton(QIcon("./resource/magnifier_plus_icon.png"), '', self)
        self.zoomin_btn.setObjectName("zoomin_btn")
        m_layout.addWidget(self.zoomin_btn)
        self.zoomin_btn.setIconSize(QSize(30, 30))
        self.zoomin_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.zoomin_btn.clicked.connect(self.parent().image_window.zoom_in)

        self.zoomout_btn = MenuButton(QIcon("./resource/magnifier_minus_icon.png"), '', self)
        self.zoomout_btn.setObjectName("zoomout_btn")
        m_layout.addWidget(self.zoomout_btn)
        self.zoomout_btn.setIconSize(QSize(30, 30))
        self.zoomout_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.zoomout_btn.clicked.connect(self.parent().image_window.zoom_out)

        self.crop_btn = MenuButton(QIcon("./resource/cut_icon.png"), '', self)
        self.crop_btn.setObjectName("crop_btn")
        m_layout.addWidget(self.crop_btn)
        self.crop_btn.clicked.connect(self.parent().image_window.crop)

        self.undo_btn = MenuButton(QIcon("./resource/undo_icon.png"), '', self)
        self.undo_btn.setEnabled(False)
        self.undo_btn.setObjectName("undo_btn")
        m_layout.addWidget(self.undo_btn)
        # 不可用则不显示悬浮变色,因为悬浮在主窗口qss中设置了
        # self.undo_btn.setStyleSheet("MenuButton:hover{background-color: #fff}")
        self.undo_btn.setShortcut("Ctrl+Z")
        self.undo_btn.clicked.connect(self.parent().image_window.undo)  # 更新窗口显示

        self.redo_btn = MenuButton(QIcon("./resource/redo_icon.png"), '', self)
        self.redo_btn.setEnabled(False)
        self.redo_btn.setObjectName("redo_btn")
        m_layout.addWidget(self.redo_btn)
        # 不可用则不显示悬浮变色,因为悬浮在主窗口qss中设置了
        # self.redo_btn.setStyleSheet("MenuButton:hover{background-color: #fff}")
        self.redo_btn.setShortcut("Ctrl+Y")
        self.redo_btn.clicked.connect(self.parent().image_window.redo)
        self.undo_btn.clicked.connect(self.toggle_btn)  # 更新按钮状态
        self.redo_btn.clicked.connect(self.toggle_btn)

    def draw_right_layout(self, r_layout):
        r_layout.setSpacing(0)

        # self.edit_btn = MenuButton(QIcon("./resource/edit_icon.png"), "编辑", self)
        # r_layout.addWidget(self.edit_btn)
        # self.edit_btn.setStyleSheet("MenuButton{ width: 90px\
        #                                         }")
        # self.edit_btn.clicked.connect(self.parent().right_window.toggle)
        # self.edit_btn.clicked.connect(self.parent().image_window.on_right_window_toggle)

        self.save_other_btn = MenuButton(QIcon("./resource/save_other_icon.png"), "另存为", self)
        self.save_other_btn.setObjectName("save_other_btn")
        r_layout.addWidget(self.save_other_btn)
        self.save_other_btn.clicked.connect(self.parent().image_window.save_other)

        self.close_btn = MenuButton(QIcon("./resource/close_icon.png"), '', self)
        self.close_btn.setObjectName("close_btn")
        r_layout.addWidget(self.close_btn)
        self.close_btn.clicked.connect(self.parent().image_window.on_image_close)

    def on_window_resize(self, w, h):
        self.setFixedWidth(w)
        # 0,1,7按钮文字隐藏
        if w < self.__min_width:
            for i in [0, 1, 7]:
                self.children()[i].setText("")
                self.children()[i].setStyleSheet("min-width: 60px;")
        else:
            self.children()[0].setText("打开图片")
            self.children()[0].setStyleSheet("max-width: 130px;")
            self.children()[1].setText("保存")
            self.children()[1].setStyleSheet("min-width: 90px")
            self.children()[7].setText("另存为")
            self.children()[7].setStyleSheet("min-width: 90px")

    # 切换撤销/重做按钮状态, 每次撤销/重做或者编辑时调用
    def toggle_btn(self):
        enable = self.parent().image_window.history_ctrl.undo_enable()
        self.undo_btn.setEnabled(enable)
        enable = self.parent().image_window.history_ctrl.redo_enable()
        self.redo_btn.setEnabled(enable)

