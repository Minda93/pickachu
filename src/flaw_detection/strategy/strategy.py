#!/usr/bin/env python3
# -*- coding: utf-8 -*-+

import roslib
roslib.load_manifest('flaw_detection')
import rospy

from lib.nodehandle import NodeHandle

def main():
    rospy.init_node('flaw_detection', anonymous=True)
    nh = NodeHandle()
    # 25 hz
    rate = rospy.Rate(25)

    while not rospy.is_shutdown():

        rate.sleep()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == "__main__":
    main()
