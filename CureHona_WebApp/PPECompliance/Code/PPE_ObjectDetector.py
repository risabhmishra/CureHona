import tensorflow as tf
import cv2 as cv
import os

# from CureHona_WebApp.PPECompliance.model import *

from CureHona_WebApp import settings



class PPE_ObjectDetector:

    label_map = {1: "person", 2: "Mask"}

    # Read the graph.
    def read_graph(self,filepath):
        with tf.io.gfile.GFile(filepath, 'rb') as f:
            self.graph_def = tf.compat.v1.GraphDef()
            self.graph_def.ParseFromString(f.read())



    # Visualize detected bounding boxes.
    def postprocess_image(self):


        rows = self.img.shape[0]
        cols = self.img.shape[1]
        num_detections = int(self.out[0][0])


        for i in range(num_detections):
            classId = int(self.out[3][0][i])
            score = float(self.out[1][0][i])
            bbox = [float(v) for v in self.out[2][0][i]]
            if score > 0.5:
                x = bbox[1] * cols
                y = bbox[0] * rows
                right = bbox[3] * cols
                bottom = bbox[2] * rows
                cv.rectangle(self.img, (int(x), int(y)), (int(right), int(bottom)), (125, 255, 51), thickness=2)
                cv.putText(self.img, self.label_map[classId], (round(x), round(y - 10)), cv.FONT_ITALIC, 0.7, (0, 0, 255),2)


        result_filename = str(self.original_image_path).replace('/Images/','/PPE/')

        cv.imwrite(os.path.join(settings.MEDIA_ROOT,result_filename),self.img)

        self.result_filename = str(self.original_image_path).replace('/Images/','/PPE/')


        # self.PPECompliance_object.result_image = result_filename
        # self.PPECompliance_object.save()



    # Run the model
    def object_detect(self):
        with tf.compat.v1.Session() as sess:
            # Restore session
            sess.graph.as_default()
            tf.import_graph_def(self.graph_def, name='')

            self.out = sess.run([sess.graph.get_tensor_by_name('num_detections:0'),
                            sess.graph.get_tensor_by_name('detection_scores:0'),
                            sess.graph.get_tensor_by_name('detection_boxes:0'),
                            sess.graph.get_tensor_by_name('detection_classes:0')],
                           feed_dict={'image_tensor:0': self.inp.reshape(1, self.inp.shape[0], self.inp.shape[1], 3)})

        self.postprocess_image()




    # Read and preprocess an image.
    def preprocess_image(self,path):

        self.original_image_path = path
        self.img = cv.imread(os.path.join(settings.MEDIA_ROOT,self.original_image_path))
        self.inp = cv.resize(self.img, (600, 600))
        self.inp = self.inp[:, :, [2, 1, 0]]  # BGR2RGB

        self.object_detect()

        return self.result_filename


