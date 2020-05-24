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
                                                         "Image Files(*.bmp;*.jpg;*.jpeg;*.png")
        if img_path != '':
            self.fileSelected.emit(img_path)
        print(img_path, img_type)

    def save_other(self):
        img_path, img_type = QFileDialog.getSaveFileName(self.parent(), "Save as", os.getcwd(),
                                                           "Images (*.png *.bmp *.jpg  *.gif *.jpeg)",
                                                           options=QFileDialog.ShowDirsOnly
                                                           | QFileDialog.DontResolveSymlinks
                                                           )
        return img_path

    def get_img_paths(self):
        img_path = QFileDialog.getExistingDirectory(self.parent(), "Choose directory", os.getcwd())
        if img_path != "":
            print(img_path)
            img_paths = [x.path for x in os.scandir(img_path) if
                         (x.name.endswith(".jpg") or x.name.endswith(".png") or x.name.endswith(".jpeg"))]
            self.parent().image_window.cloud(img_paths)

    def open_face(self):
        img_path, img_type = QFileDialog.getOpenFileName(self.parent(), "请选择目标人像", os.getcwd(),
                                                         "Image Files(*.bmp;*.jpg;*.jpeg;*.png")
        return img_path
