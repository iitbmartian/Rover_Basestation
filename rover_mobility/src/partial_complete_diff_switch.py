#!/usr/bin/env python

import rospy
import time
from std_msgs.msg import Bool
import math
from curtsies import Input
import signal
import sys

#-----------------------------------------------------------------
#SIGINT handler
def sigint_handler(signal, frame):
    sys.exit(0)

def main():
    pub = rospy.Publisher('Differential_switch', Bool,queue_size=10)
    rospy.init_node('Diff_Switch', anonymous=True)

    with Input(keynames='curses') as input_generator:
        for e in input_generator:
            print(str(repr(e)))
            if(str(repr(e))==str('u\'f\'')):
                print('Full Differential Mode')
                pub.publish(True)
            elif(str(repr(e))==str('u\'h\'')):
                print('Partial Differential Mode')
                pub.publish(False)
            elif(str(repr(e))==str('u\'q\'')):
                print("Invalid Option")

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    main()




#import keyboard #Using module keyboard

'''
pub = rospy.Publisher('autonomous_switch', Bool,queue_size=10)
rospy.init_node('talker', anonymous=True)
while True:#making a loop
    print("Here")
    try: #used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('s'):#if key 'q' is pressed 
            print('Steer Mode')
            pub.publish(True)
        elif keyboard.is_pressed('d'):
            print('Drive Mode')
            pub.publish(False)
        elif keyboard.is_pressed('q'):
            print("Quiting")
            break#finishing the loop
        else:
            pass
    except:
    #    break #if user pressed other than the given key the loop will break
        print("Exception")
'''

