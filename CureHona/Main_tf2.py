import numpy as np
import tensorflow as tf
import cv2 as cv
import configparser
import os

label_map = {1:"person",2:"Mask"}

# Config Parser for Getting Values from Main_Config file

configParser = configparser.RawConfigParser()
configParser.readfp(open(r'Config/Main_Config.ini'))

tf_graph_filepath = configParser.get('OBJECT_DETECTION', 'TF_GRAPH_FILE_PATH')

files = os.listdir('./data')

# Read the graph.
with tf.gfile.FastGFile(tf_graph_filepath, 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())

with tf.Session() as sess:
    # Restore session
    sess.graph.as_default()
    tf.import_graph_def(graph_def, name='')

    for file in files:
        # Read and preprocess an image.
        print('./data/{0}'.format(file))
        img = cv.imread('./data/{0}'.format(file))
        rows = img.shape[0]
        cols = img.shape[1]
        inp = cv.resize(img, (300, 300))
        inp = inp[:, :, [2, 1, 0]]  # BGR2RGB

        # Run the model
        out = sess.run([sess.graph.get_tensor_by_name('num_detections:0'),
                        sess.graph.get_tensor_by_name('detection_scores:0'),
                        sess.graph.get_tensor_by_name('detection_boxes:0'),
                        sess.graph.get_tensor_by_name('detection_classes:0')],
                       feed_dict={'image_tensor:0': inp.reshape(1, inp.shape[0], inp.shape[1], 3)})

        # Visualize detected bounding boxes.
        num_detections = int(out[0][0])
        for i in range(num_detections):
            classId = int(out[3][0][i])
            score = float(out[1][0][i])
            bbox = [float(v) for v in out[2][0][i]]
            if score > 0.3:
                x = bbox[1] * cols
                y = bbox[0] * rows
                right = bbox[3] * cols
                bottom = bbox[2] * rows
                cv.rectangle(img, (int(x), int(y)), (int(right), int(bottom)), (125, 255, 51), thickness=2)
                cv.putText(img, label_map[classId], (round(x), round(y - 10)), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                           (0, 0, 255))
        cv.imshow('TensorFlow Personnel Protective Equipment Compliance', img)
        cv.waitKey()


