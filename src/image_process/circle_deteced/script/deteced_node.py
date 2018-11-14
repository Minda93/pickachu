#!/usr/bin/env python
import rospy
import rospkg
from std_msgs.msg import Bool
from yolov3_ros.msg import ROI
from sensor_msgs.msg import Image as Image_ros
from circle_deteced.msg import deteced_param
from circle_deteced.msg import hough_param
from circle_deteced.msg import hsv_param
from cv_bridge import CvBridge, CvBridgeError

import cv2 
import numpy as np
import glob
import os
import subprocess

bridge = CvBridge()
ori_image = np.ndarray(0)
gray_image = np.ndarray(0)
hsv = np.ndarray(0)

image_flag = False
lower_white = np.array([0,0,205])
upper_white = np.array([180,255,255])
hough_param = hough_param()
hough_param.dp        = 1
hough_param.minDistx  = 20  
hough_param.minDisty  = 20  
hough_param.param1    = 100
hough_param.param2    = 20
hough_param.minRadius = 10  
hough_param.maxRadius = 30  

def White_chess(image,Wcircles):
    output_image = image.copy()
    if Wcircles is not None:
            Wcircles = np.uint16(np.around(Wcircles))
            for i in Wcircles[0,:]:
                # draw the outer circle
                cv2.circle(output_image,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(output_image,(i[0],i[1]),2,(0,0,255),3)
    return output_image

def image_source_callback(data):
    global ori_image
    global gray_image
    global hsv
    global image_flag
    global hough_param
    try:
        ori_image = bridge.imgmsg_to_cv2(data, "bgr8")

        # gray_image = cv2.cvtColor(ori_image,cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(ori_image,cv2.COLOR_BGR2HSV)
        hsv_white = cv2.inRange(hsv, lower_white, upper_white)

        Wcircles = cv2.HoughCircles(hsv_white,cv2.HOUGH_GRADIENT,hough_param.dp,hough_param.minDistx,param1=hough_param.param1,param2=hough_param.param2,minRadius=hough_param.minRadius,maxRadius=hough_param.maxRadius)#min = 100 max = 200 
        result = White_chess(ori_image,Wcircles)
        
        # gray_image_pub.publish(bridge.cv2_to_imgmsg(gray_image, "mono8"))
        hsv_white_pub.publish(bridge.cv2_to_imgmsg(hsv_white, "mono8"))
    except CvBridgeError as e:
      print(e)
      
    cv2.imshow("ORI Image", ori_image)
    # cv2.imshow('GRAY Image',gray_image)
    cv2.imshow('White_hsv',hsv_white)
    cv2.imshow('result',result)
    cv2.waitKey(3)
    image_flag = True


def deteced_():
    global ori_image
    global gray_image
    global hsv
    global image_flag
    rate = rospy.Rate(30) # 10hz
    while not rospy.is_shutdown():
        # if image_flag :
        rate.sleep()
        image_flag = False
def close():
    cv2.destroyAllWindows()
    
def set_Param_callback(data):
    global lower_white
    global upper_white
    global hough_param

    lower_white = np.array([data.lower[0].Brightness,data.lower[0].Contras,data.lower[0].Saturation])
    upper_white = np.array([data.upper[0].Brightness,data.upper[0].Contras,data.upper[0].Saturation])
    hough_param.dp        = data.circle[0].dp
    hough_param.minDistx  = data.circle[0].minDistx  
    hough_param.minDisty  = data.circle[0].minDisty  
    hough_param.param1    = data.circle[0].param1
    hough_param.param2    = data.circle[0].param2
    hough_param.minRadius = data.circle[0].minRadius  
    hough_param.maxRadius = data.circle[0].maxRadius  

# """ save param """
# def Save_Param(msg):
#     FILENAME = rospkg.RosPack().get_path('circle_deteced')+'/config/'+'param.yaml'
#     print(FILENAME)
#     subprocess.call(['rosparam','dump',FILENAME,'/circle_detected/parameters'])
#     Set_Param()
#     if (rospy.has_param('/circle_detected/parameters')):
#         print('dump')
#         subprocess.call(['rosparam','dump',FILENAME,'/circle_detected/parameters'])
#         Load_Param()
#     else:
#         print('Not found')
    
# def Load_Param():
#     global lower_white
#     global upper_white
#     global hough_param
#     if (rospy.has_param('/circle_detected/parameters/lower')):
#         lower = rospy.get_param("/circle_detected/parameters/lower")
#         lower_white =np.ndarray(lower)
#     if (rospy.has_param('/circle_detected/parameters/upper')):
#         upper = rospy.get_param("/circle_detected/parameters/upper")
#         upper_white =np.ndarray(upper)
#     if (rospy.has_param('/circle_detected/parameters/hough')):
#         hough_param = rospy.get_param("/circle_detected/parameters/hough")  

# def Set_Param():
#     global lower_white
#     global upper_white
#     global hough_param
#     print(1)
#     # rospy.set_param('/circle_detected/parameters/lower',lower)
#     # rospy.set_param('/circle_detected/parameters/upper',upper)
#     rospy.set_param('circle_detected/parameters/hough',hough_param)
#     print(2)

if __name__ == '__main__':
    rospy.init_node('circle_deteced', anonymous=True)

    # gray_image_pub = rospy.Publisher("/object/gray_image",Image_ros,queue_size=10)
    hsv_white_pub  = rospy.Publisher("/object/hsv_white_image",Image_ros,queue_size=10)
    metal_circle_pub = rospy.Publisher("/object/metal_ROI",ROI,queue_size=10)

    ros_sub = rospy.Subscriber("/usb_cam/image_raw",Image_ros,image_source_callback)
    param_sub = rospy.Subscriber("/object/parameters_save",deteced_param,set_Param_callback)
    try:
        deteced_()
    except rospy.ROSInterruptException:
        pass
    close()