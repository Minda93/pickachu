#!/usr/bin/env python3
# -*- coding: utf-8 -*-+

import roslib
roslib.load_manifest('arm_control')
import rospy

from lib.arm_cmd import ArmCmd


def main():
    rospy.init_node('arm_control', anonymous=True)
    arm = ArmCmd()
    # 25 hz
    rate = rospy.Rate(25)

    while not rospy.is_shutdown():
        arm.Run()
        rate.sleep()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == "__main__":
    main()
