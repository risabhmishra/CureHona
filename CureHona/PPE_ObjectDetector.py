import numpy as np
import tensorflow as tf
import cv2 as cv
import threading


class PPE_ObjectDetector:

    label_map = {1: "person",2: "Mask"}

    # Read the graph.
    def read_graph(self,filepath):
        with tf.io.gfile.GFile(filepath, 'rb') as f:
            self.graph_def = tf.compat.v1.GraphDef()
            self.graph_def.ParseFromString(f.read())

    # Read and preprocess an image.
    def preprocess_image(self,image_path):

        # self.img = cv.imread(image_path)
        self.img = image_path
        self.inp = cv.resize(self.img, (300, 300))
        self.inp = self.inp[:, :, [2, 1, 0]]  # BGR2RGB

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


    # Visualize detected bounding boxes.
    def postprocess_image(self):

        rows = self.img.shape[0]
        cols = self.img.shape[1]
        num_detections = int(self.out[0][0])

        rects = []

        for i in range(num_detections):
            classId = int(self.out[3][0][i])
            score = float(self.out[1][0][i])
            bbox = [float(v) for v in self.out[2][0][i]]
            if score > 0.5:
                x = bbox[1] * cols
                y = bbox[0] * rows
                right = bbox[3] * cols
                bottom = bbox[2] * rows
                # cv.rectangle(self.img, (int(x), int(y)), (int(right), int(bottom)), (125, 255, 51), thickness=2)
                # cv.putText(self.img, self.label_map[classId], (round(x), round(y - 10)), cv.FONT_ITALIC, 0.7, (0, 0, 255),2)

                box = (int(x),int(y),int(right),int(bottom),self.label_map[classId])

                rects.append(box)

        return rects
        # cv.imshow('TensorFlow Personnel Protective Equipment Compliance', self.img)
        # cv.waitKey()

