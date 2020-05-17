import numpy as np

class HistoryControl:
    stack_len = 0  # stack_len-1才是当前编辑图片
    position = 0  # 位置指针

    def __init__(self):
        self.history_src = []
        self.history_descp = []

    def push(self, img, descp):
        if self.position == self.stack_len:
            self.history_src.append(img)
            self.history_descp.append(descp)
        else:
            # 后面的全丢掉
            self.history_src[self.position] = img
            self.history_descp[self.position] = descp
            self.history_src = self.history_src[:self.position+1]
            self.history_descp = self.history_descp[:self.position+1]
        self.position += 1
        self.stack_len =self.position

    def current(self) -> np.ndarray:
        if self.position > 0:
            return self.history_src[self.position - 1], self.history_descp[self.position - 1]
        else:
            print("no image to extract")
            return False, False

    def undo_enable(self):
        return self.position > 1

    def redo_enable(self):
        return self.position < self.stack_len

    def undo(self):
        self.position -= 1

    def redo(self):
        self.position += 1

    def clear(self):
        self.history_src = []
        self.history_descp = []
        self.position = self.stack_len = 0