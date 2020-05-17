import os
from PyQt5.QtWidgets import QFileDialog

class FileDialog(QFileDialog):
    title = "选择图片"

    def __init__(self, parent):
        super(QFileDialog, self).__init__(parent)
        self.fileSelected.connect(self.parent().update_open_image)  # 该事件自动传参文件path
        self.fileSelected.connect(self.parent().image_window.on_image_open)

    def open_image(self):
        img_path, img_type = QFileDialog.getOpenFileName(self.parent(), self.title, os.getcwd(),
                                                         "Image Files(*.jpg *.jpeg *.png")
        if img_path != '':
            self.fileSelected.emit(img_path)