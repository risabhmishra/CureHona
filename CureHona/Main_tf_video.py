import numpy as np
import cv2 as cv
import concurrent.futures
import imutils
from imutils.video import VideoStream

import configparser
import multiprocessing

from PPE_ObjectDetector import PPE_ObjectDetector
from PPE_ObjectTracker_dlib import PPE_ObjectTracker


if __name__=='__main__':

    # Config Parser for Getting Values from Main_Config file

    configParser = configparser.RawConfigParser()
    configParser.readfp(open(r'Config/Main_Config.ini'))




    tf_graph_filepath = configParser.get('OBJECT_DETECTION', 'TF_GRAPH_FILE_PATH')
    input_video_path = configParser.get('OBJECT_DETECTION', 'INPUT_VIDEO_PATH')

    track_length = int(configParser.get('OBJECT_TRACKING', 'TRACK_LENGTH'))


    # q = multiprocessing.Queue()
    #
    # process_object_detection = multiprocessing.Process(target=object_detect,args=(tf_graph_filepath,input_video_path,q))
    # process_object_tracking = multiprocessing.Process(target=object_track,args=(q,))
    #
    # process_object_detection.start()
    # process_object_tracking.start()
    #
    # process_object_detection.join()
    # process_object_tracking.join()



    object_detector = PPE_ObjectDetector()
    object_detector.read_graph(tf_graph_filepath)

    object_tracker = PPE_ObjectTracker(track_length)

    cap = cv.VideoCapture(input_video_path)
    out = cv.VideoWriter('output10.avi', cv.VideoWriter_fourcc('D', 'I', 'V', 'X'), 15, (600, 600), 1)


    label_count = {}
    max_id = -1

    # img = cv.imread('./data/08jpg')
    #
    # face_cascade = cv.CascadeClassifier('./Model/haarcascade_frontalface_default.xml')
    #
    # gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    #
    # faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    while cap.isOpened():

        ret, frame = cap.read()

        if ret == False:
            break

        img = cv.resize(frame,(600,600))
        object_detector.preprocess_image(img)

        object_detector.object_detect()

        rects = object_detector.postprocess_image()

        print(rects)

        # for face in faces:
        #     rects.append((face[0],face[1],face[2],face[3],'Without Mask'))

        objects = object_tracker.update(img, rects)

        print("Objects for Tracking", objects)

        if objects:

            for (id, object) in objects.items():
                # draw both the ID of the object and the centroid of the
                # object on the output frame
                print(id, object[0], object[1])

                if not object[0] in label_count:
                    print("New Class Count")
                    label_count[object[0]] = 1
                    max_id = id
                elif object[0] in label_count and id > max_id:
                    print("Update Class Count")
                    label_count[object[0]] += 1
                    max_id = id

                pos = object[1].get_position()
                # unpack the position object
                startX = int(pos.left())
                startY = int(pos.top())
                endX = int(pos.right())
                endY = int(pos.bottom())

                cv.rectangle(img, (startX, startY), (endX, endY), (0, 255, 0), thickness=2)
                cv.putText(img, "People With {0}".format(object[0], id), (round(startX + 10), round(endY - 10)), cv.FONT_ITALIC,
                           0.7, (255, 0, 0), 1)

        # show the output frame
        print(label_count)
        print(max_id)
        # cv.putText(img, str(label_count), (10, 550), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        out.write(img)
        cv.imshow("Frame", img)


        key = cv.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # do a bit of cleanup
    cv.destroyAllWindows()
    cap.release()
    out.release()






