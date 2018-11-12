#!/usr/bin/env python3
# -*- coding: utf-8 -*-+

import roslib
roslib.load_manifest('flaw_detection')
import rospy

from lib.flaw_detection import Strategy



def main():
    rospy.init_node('flaw_detection', anonymous=True)
    robot = Strategy()
    # 25 hz
    rate = rospy.Rate(25)

    while not rospy.is_shutdown():
        robot.Run()
        rate.sleep()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == "__main__":
    main()
