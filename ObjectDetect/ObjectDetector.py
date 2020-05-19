from imageai.Detection import ObjectDetection
import os
import numpy as np
from PIL import Image


class Object_Detector(object):
    execution_path = os.getcwd()
    detector = ObjectDetection()
    detector.setModelTypeAsTinyYOLOv3()
    detector.setModelPath(os.path.join(execution_path, "ObjectDetect/yolo-tiny.h5"))
    detector.loadModel()

    def object_detc(self, input_image: Image)->Image:
        input_image = np.array(input_image)
        image, object_list = self.detector.detectObjectsFromImage(input_image, input_type='array', output_type='array',
                                                       minimum_percentage_probability=16,
                                                       display_percentage_probability=True,
                                                       display_object_name=True)
        image = Image.fromarray(image)
        print(object_list)
        return image, object_list

if __name__ == "__main__":
    detector = Object_Detector()
    while True:
        file = input("输入图片名")
        img = Image.open("%s.jpg"%file)
        img_res, obj_list = detector.object_detc(img)
        img_res.show()
