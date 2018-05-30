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
        
if __name__ == '__main__':
    try:
        camUrl='udp://10.5.5.9:8554'
        rospy.init_node('foss_node', anonymous=True)
        stream=urllib.urlopen(camUrl)
        print "Correctly opened resource, starting to show feed."
        image_pub = rospy.Publisher("fosscam_vid", Image,queue_size=1000)
        bridge = CvBridge()
        bytes=''
        while not rospy.is_shutdown():
            bytes+=stream.read(1024)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            if a!=-1 and b!=-1:
                jpg = bytes[a:b+2]
                bytes= bytes[b+2:]
                i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
                image_pub.publish(bridge.cv2_to_imgmsg(i, "bgr8"))
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
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
