#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Float64MultiArray
from sensor_msg.msg import Joy

def callback(inp):
    print(inp.data)
    
rospy.init_node('joy', anonymous=True)
rospy.Subscriber("Joy", Joy, callback)
# spin() simply keeps python from exiting until this node is stopped
rospy.spin()
