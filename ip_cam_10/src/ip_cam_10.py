#!/usr/bin/env python

import cv2,platform
import urllib
import numpy as np
from sensor_msgs.msg import Image
import roslib
import sys
import rospy
import cv
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError

class ipcamera(object):
    def __init__(self, url):
        try:
            self.stream=cv2.VideoCapture(url)
        except:
            rospy.logerr('Unable to open camera stream: ' + str(url))
            sys.exit() #'Unable to open camera stream')
        if not self.stream.isOpened():
            print "Error opening resource: " + str(url)
            print "Maybe opencv VideoCapture can't open it"
            sys.exit()
        #
        print "Correctly opened resource, starting to show feed."
        self.bytes=''
        self.image_pub = rospy.Publisher("ipcam10_vid", Image,queue_size=1000)
        self.bridge = CvBridge()

if __name__ == '__main__':
    try:
        camUrl='udp://:8554'
        rospy.init_node('ipcam_10', anonymous=True)
        ip_camera = ipcamera(camUrl)

        while not rospy.is_shutdown():
            rval, frame = ip_camera.stream.read()
            if rval:
                #cv2.imshow("Stream: webcam", frame)
                (rval,frame) = ip_camera.stream.read()
                ip_camera.image_pub.publish(ip_camera.bridge.cv2_to_imgmsg(frame, "bgr8"))
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        ip_camera.stream.release()
        cv2.destroyAllWindows()
    except rospy.ROSInterruptException:
        pass
    '''
        ip_camera.bytes += ip_camera.stream.read(1024)
        a = ip_camera.bytes.find('\xff\xd8')
        b = ip_camera.bytes.find('\xff\xd9')
        if a!=-1 and b!=-1:
            jpg = ip_camera.bytes[a:b+2]
            ip_camera.bytes= ip_camera.bytes[b+2:]
            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
            image_message = cv.fromarray(i)
            ip_camera.image_pub.publish(ip_camera.bridge.cv_to_imgmsg(image_message, "bgr8"))

            if args.gui:
                cv2.imshow('IP Camera Publisher Cam',i)
            if cv2.waitKey(1) ==27: # wait until ESC key is pressed in the GUI window to stop it
                exit(0)
    #ip_camera.stream.release()

    '''
