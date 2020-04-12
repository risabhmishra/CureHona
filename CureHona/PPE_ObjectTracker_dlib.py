import numpy as np
import tensorflow as tf
import cv2 as cv
import threading
import dlib

from scipy.spatial import distance as dist
from collections import OrderedDict

class PPE_ObjectTracker:

    def __init__(self, maxDisappeared):

        # Initializing the object id
        self.nextObjectId = 0

        # Ordered dict of new objects detected
        self.objects = OrderedDict()

        # Ordered dict of labels
        self.labels = OrderedDict()

        # Ordered dict of objects with the count of disappeared frames
        self.disappeared = OrderedDict()

        # Max no of frames the objects to be tracked before declaring it disappeared
        self.maxDisappeared = maxDisappeared


    def register(self,tracker,label):

        # create new object with id and assign the centroid value to it
        self.objects[self.nextObjectId] = tracker

        # create new label for the corresponding tracker
        self.labels[self.nextObjectId] = label

        # Initialize the frames disappeared count of object to 0
        self.disappeared[self.nextObjectId] = 0

        # Increment the nextObjectId by 1
        self.nextObjectId += 1


    def deregister(self,ObjectId):

        # Delete the object from Objects Ordered Dictionary
        del self.objects[ObjectId]

        # Delete the corresponding label from Labels Ordered Dictionary
        del self.labels[ObjectId]

        # Delete the object from disappeared Ordered Dictionary
        del self.disappeared[ObjectId]

    def update(self,frame,rects):

        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        # If there are no detections
        if len(rects) == 0:

            # Iterate over the objects present in the disappeared ordered dictionary
            for objectId in self.disappeared.keys():

                # Increment the count by 1
                self.disappeared[objectId] += 1

                # Check if the disappeared count of any object has crossed the maxDisappeared Threshold
                if self.disappeared[objectId] > self.maxDisappeared:

                    # Deregister such objects
                    self.deregister(objectId)

            print("Tracker - No Faces Detected",self.objects)

            # return self.objects,self.labels

        # Else if there are valid detections present
        else:

            print("Tracker - Faces",rects)

            for rect in rects:

                x = int(rect[0])
                y = int(rect[1])
                w = int(rect[2]-rect[0])
                h = int(rect[3]-rect[1])

                # calculate the centerpoint
                x_bar = x + 0.5 * w
                y_bar = y + 0.5 * h

                # Variable holding information which personid we
                # matched with
                matchedPid = None

                # Now loop over all the trackers and check if the
                # centerpoint of the person is within the box of a
                # tracker
                for pid in self.objects.keys():

                    tracked_position = self.objects[pid].get_position()

                    t_x = int(tracked_position.left())
                    t_y = int(tracked_position.top())
                    t_w = int(tracked_position.width())
                    t_h = int(tracked_position.height())

                    # calculate the centerpoint
                    t_x_bar = t_x + 0.5 * t_w
                    t_y_bar = t_y + 0.5 * t_h

                    # check if the centerpoint of the person is within the
                    # rectangle of a tracker region. Also, the centerpoint
                    # of the tracker region must be within the region
                    # detected as a person. If both of these conditions hold
                    # we have a match
                    if ((t_x <= x_bar <= (t_x + t_w)) and (t_y <= y_bar <= (t_y + t_h)) and
                            (x <= t_x_bar <= (x + w)) and
                            (y <= t_y_bar <= (y + h))):
                        matchedPid = pid

                        # self.labels[pid] = person.label

                    # self.disappeared[pid] = 0

                print(matchedPid)

                # If no matched pid, then we have to create a new tracker
                if matchedPid is None:
                    print("Creating new tracker ")
                    # Create and store the tracker
                    tracker = dlib.correlation_tracker()
                    tracker.start_track(rgb,dlib.rectangle(x - 10,y - 20,x + w + 10,y + h + 20))

                    self.register(tracker,rect[4])

            # Update all the trackers and remove the ones for which the update
            # indicated the quality was not good enough

            for pid in self.objects.keys():

                trackingQuality = self.objects[pid].update(rgb)

                # If the tracking quality is good enough, we must delete
                # this tracker
                print("Tracking Quality",trackingQuality)
                if trackingQuality < 7:
                    self.disappeared[pid] += 1

                    # Check if the disappeared count of any object has crossed the maxDisappeared Threshold
                    if self.disappeared[pid] > self.maxDisappeared:
                        # Deregister such objects
                        self.deregister(pid)

            objects_labels = {}

            for pid,tracker in self.objects.items():
                if self.disappeared[pid] == 0:
                    objects_labels[pid] = [self.labels[pid],tracker]


            return objects_labels


