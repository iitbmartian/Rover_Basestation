#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Float64MultiArray,Float32MultiArray,String
import numpy as np

def talker():
    pub = rospy.Publisher('arm_cont', Float64MultiArray, queue_size=10)
    rospy.init_node('arm_cont', anonymous=True)
    rate = rospy.Rate(1) # 10hz
    count=0
    pub_array=np.array([0,0])
    while not rospy.is_shutdown():
        if(count==0):
            pub_array[0]=0
            pub_array[1]=1
        elif(count==1):
            pub_array[0]=0
            pub_array[1]=-1
        elif(count==2):
            pub_array[0]=1
            pub_array[1]=0
        elif(count==3):
            pub_array[0]=-1
            pub_array[1]=0
        count=(count+1)%4
        pub_msg=Float64MultiArray(data=pub_array)
        pub.publish(pub_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass