#!/usr/bin/env python
import rospy
import rospkg
from std_msgs.msg import Bool
from std_msgs.msg import Int32MultiArray
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
lower_white = np.array([0,0,178])
upper_white = np.array([255,255,215])
white_hough_param = hough_param()
white_hough_param.dp        = 1.02
white_hough_param.minDistx  = 20  
white_hough_param.minDisty  = 20  
white_hough_param.param1    = 100
white_hough_param.param2    = 15
white_hough_param.minRadius = 8  
white_hough_param.maxRadius = 12  

lower_black = np.array([0,0,65])
upper_black = np.array([255,255,255])
black_hough_param = hough_param()
black_hough_param.dp        = 1.5
black_hough_param.minDistx  = 20  
black_hough_param.minDisty  = 20  
black_hough_param.param1    = 100
black_hough_param.param2    = 20
black_hough_param.minRadius = 10  
black_hough_param.maxRadius = 12  

def draw_chess(image,circles,(R,G,B)):
    output_image = image.copy()
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            x,y,r=i[0],i[1],i[2]
            cv2.circle(output_image,(x,y),r,(R,G,B),2)
            # draw the center of the circle
            cv2.circle(output_image,(x,y),2,(R,G,B),3)
    return output_image

def Initial_checkerboard():
    checkerboard=list()
    for h in range(9):
        for w in range(9):
            checkerboard.append(0)
    return checkerboard
recognized_board = Initial_checkerboard()

def recognizing(image,Bcircles,Wcircles,Line_show=False,Board_show=False):
    global recognized_board
    board = Int32MultiArray()

    output_image = image.copy()
    column = [0,22,44,66,88,110,132,154,176,200]    
    row = [0,22,44,66,88,107,129,151,173,195]
    offset_x,offset_y = 220,148
    n_column = [220, 242, 264, 286, 308, 330, 352, 374, 396, 420]
    n_row    = [150, 172, 194, 216, 238, 260, 282, 304, 326, 348]
    if Bcircles is not None and Wcircles is not None:
        for h in range(9):
            for w in range(9):
                Bcircles = np.uint16(np.around(Bcircles))
                Wcircles = np.uint16(np.around(Wcircles))
                for i in Bcircles[0,:]:
                    x,y,r=int(i[0]),int(i[1]),i[2]
                    if x >= n_column[h] and x < n_column[h+1] and \
                    y >= n_row[w] and y < n_row[w+1] :
                        recognized_board[h * 9 + w] = 1
                        print("get one black")
                for j in Wcircles[0,:]:
                    x,y,r=int(j[0]),int(j[1]),j[2]
                    if x >= n_column[h] and x < n_column[h+1] and \
                    y >= n_row[w]  and y < n_row[w+1]  and (recognized_board[h * 9 + w] == 0):
                        recognized_board[h * 9 + w] = -1
                        print("get one white")
        output_image_tmp = draw_chess(output_image,Bcircles,(0,255,0))
        output_image = draw_chess(output_image_tmp,Wcircles,(0,0,255))
    if Line_show:
        for i in range(len(column)):
            cv2.line(output_image,(n_column[i],n_row[0]),(n_column[i],n_row[9]), (0, 0, 255), 1)
        for i in range(len(row)):
            cv2.line(output_image,(n_column[0],n_row[i]),(n_column[9],n_row[i]), (0, 255, 255), 1)
    if Board_show:
        print("^^^^^^^^^^^^^^^^^^^^^^^^^")
        for h in range(9):
            w=0
            print(recognized_board[h*9+w],\
                  recognized_board[h*9+w+1],\
                  recognized_board[h*9+w+2],\
                  recognized_board[h*9+w+3],\
                  recognized_board[h*9+w+4],\
                  recognized_board[h*9+w+5],\
                  recognized_board[h*9+w+6],\
                  recognized_board[h*9+w+7],\
                  recognized_board[h*9+w+8])
            for w in range(9):
                board.data.append(recognized_board[h*9+w])
        print("vvvvvvvvvvvvvvvvvvvvvvvvvv")
    return output_image,board

def image_source_callback(data):
    global ori_image
    global gray_image
    global hsv
    global image_flag
    global white_hough_param
    try:
        ori_image = bridge.imgmsg_to_cv2(data, "bgr8")

        # gray_image = cv2.cvtColor(ori_image,cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(ori_image,cv2.COLOR_BGR2HSV)
        hsv_white = cv2.inRange(hsv, lower_white, upper_white)
        hsv_black = cv2.inRange(hsv, lower_black, upper_black)

        Wcircles = cv2.HoughCircles(hsv_white,cv2.HOUGH_GRADIENT,white_hough_param.dp,white_hough_param.minDistx,param1=white_hough_param.param1,param2=white_hough_param.param2,minRadius=white_hough_param.minRadius,maxRadius=white_hough_param.maxRadius)#min = 100 max = 200 
        Bcircles = cv2.HoughCircles(hsv_black,cv2.HOUGH_GRADIENT,black_hough_param.dp,black_hough_param.minDistx,param1=black_hough_param.param1,param2=black_hough_param.param2,minRadius=black_hough_param.minRadius,maxRadius=black_hough_param.maxRadius)#min = 100 max = 200 
        
        # result_tmp = draw_chess(ori_image,Bcircles,(0,255,0))
        # result = draw_chess(result_tmp,Wcircles,(0,0,255))
        
        result,board_ = recognizing(ori_image,Bcircles,Wcircles,True,True)

        # gray_image_pub.publish(bridge.cv2_to_imgmsg(gray_image, "mono8"))
        hsv_white_pub.publish(bridge.cv2_to_imgmsg(hsv_white, "mono8"))
        hsv_black_pub.publish(bridge.cv2_to_imgmsg(hsv_black, "mono8"))

        
        board_pub.publish(board_)
    except CvBridgeError as e:
      print(e)
      
    # cv2.imshow("ORI Image", ori_image)
    # cv2.imshow('GRAY Image',gray_image)
    cv2.imshow('White_hsv',hsv_white)
    cv2.imshow('Black_hsv',hsv_black)
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
    
def set_White_Param_callback(data):
    global lower_white
    global upper_white
    global white_hough_param
    print(white_hough_param)
    lower_white = np.array([data.lower.Brightness,data.lower.Contras,data.lower.Saturation])
    upper_white = np.array([data.upper.Brightness,data.upper.Contras,data.upper.Saturation])
    white_hough_param.dp        = data.circle.dp
    white_hough_param.minDistx  = data.circle.minDistx  
    white_hough_param.minDisty  = data.circle.minDisty  
    white_hough_param.param1    = data.circle.param1
    white_hough_param.param2    = data.circle.param2
    white_hough_param.minRadius = data.circle.minRadius  
    white_hough_param.maxRadius = data.circle.maxRadius  

def set_Black_Param_callback(data):
    global lower_black
    global upper_black
    global black_hough_param
    print(black_hough_param)
    lower_black = np.array([data.lower.Brightness,data.lower.Contras,data.lower.Saturation])
    upper_black = np.array([data.upper.Brightness,data.upper.Contras,data.upper.Saturation])
    black_hough_param.dp        = data.circle.dp
    black_hough_param.minDistx  = data.circle.minDistx  
    black_hough_param.minDisty  = data.circle.minDisty  
    black_hough_param.param1    = data.circle.param1
    black_hough_param.param2    = data.circle.param2
    black_hough_param.minRadius = data.circle.minRadius  
    black_hough_param.maxRadius = data.circle.maxRadius  

if __name__ == '__main__':
    rospy.init_node('circle_deteced', anonymous=True)

    # gray_image_pub = rospy.Publisher("/object/gray_image",Image_ros,queue_size=10)
    hsv_white_pub  = rospy.Publisher("/object/hsv_white_image",Image_ros,queue_size=10)
    hsv_black_pub  = rospy.Publisher("/object/hsv_black_image",Image_ros,queue_size=10)
    metal_circle_pub = rospy.Publisher("/object/metal_ROI",ROI,queue_size=10)
    board_pub = rospy.Publisher("/gomoku/vBoard",Int32MultiArray,queue_size=10)

    ros_sub = rospy.Subscriber("/usb_cam/image_raw",Image_ros,image_source_callback)
    param_white_sub = rospy.Subscriber("/object/parameters_save_White",deteced_param,set_White_Param_callback)
    param_black_sub = rospy.Subscriber("/object/parameters_save_Black",deteced_param,set_Black_Param_callback)
    try:
        deteced_()
    except rospy.ROSInterruptException:
        pass
    close()