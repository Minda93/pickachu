#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import sys
import argparse
from yolo import YOLO, detect_video
from PIL import Image
import os
from timeit import default_timer as timer
import numpy as np
from yolov3_ros.msg import ROI
from yolov3_ros.msg import ROI_array
from yolov3_ros.msg import Suck_point

import threading
import time
import roslib
roslib.load_manifest('yolov3_ros')
import cv2
from sensor_msgs.msg import Image as Image_ros
from cv_bridge import CvBridge, CvBridgeError
bridge = CvBridge()
# sys.path.insert(1,'/home/iclab/.local/lib/python3.5/site-packages')
cv_image = np.ndarray(0)
image_flag = False

def detect_img(yolo):
    while True:
        img = input('Input image filename:')
        try:
            image = Image.open(img)
        except:
            print('Open Error! Try again!')
            continue
        else:
            r_image = yolo.detect_image(image)
            r_image.show()
    yolo.close_session()

def estimation_suck_point(data):
    msg = Suck_point()
    if data.class_name == "metal":
        center_x = (data.x_min + data.x_Max)/2
        center_y = (data.y_min + data.y_Max)/2
        width = data.x_Max-data.x_min
        height = data.y_Max-data.y_min
        delta = width - height
        if delta < -10:
            msg.Ax = center_x
            msg.Bx = center_x
            msg.Ay = center_y + (height/4)
            msg.By = center_y - (height/4)
        elif delta > 10:
            msg.Ax = center_x + (width/4)            
            msg.Bx = center_x - (width/4)
            msg.Ay = center_y
            msg.By = center_y
        else:
            msg.Ax = center_x - (width/4)
            msg.Bx = center_x - (width/4)
            msg.Ay = center_y + (height/4)
            msg.By = center_y + (height/4)
        suckpoint_pub.publish(msg)
    return msg

def clone_detect_video(yolo, video_path, output_path=""):
    global image_flag
    print("yolo type = "+str(type(yolo)))
    # import cv2
    # # video_path = "/home/iclab/Downloads/Humans_HD_Stock_Video.mp4"
    # video_path = 0
    # vid = cv2.VideoCapture(video_path)

    # if not vid.isOpened():
    #     raise IOError("Couldn't open webcam or video")
    # video_FourCC    = int(vid.get(cv2.CAP_PROP_FOURCC))
    # video_fps       = vid.get(cv2.CAP_PROP_FPS)
    # video_size      = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
    #                     int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    isOutput = True if output_path != "" else False
    # if isOutput:
    #     print("!!! TYPE:", type(output_path), type(video_FourCC), type(video_fps), type(video_size))
    #     out = cv2.VideoWriter(output_path, video_FourCC, video_fps, video_size)
    accum_time = 0
    curr_fps = 0
    fps = "FPS: ??"
    prev_time = timer()
    while not rospy.is_shutdown():
        if image_flag:
            suck_msg = None
            # return_value, frame = vid.read()
            # image = Image.fromarray(frame)
            image = Image.fromarray(cv_image)
            image,ROI_array_recive = yolo.detect_image(image)
            if ROI_array_recive!=None:
                ROI_array_msg = ROI_array()
                for i in range(len(ROI_array_recive)):
                    ROI_msg = ROI()
                    print("class_name type = " + str(ROI_array_recive[i][0]))
                    print("score type = "      + str(ROI_array_recive[i][1]))
                    print("x_min type = "      + str(ROI_array_recive[i][2]))
                    print("x_Max type = "      + str(ROI_array_recive[i][3]))
                    print("y_min type = "      + str(ROI_array_recive[i][4]))
                    print("y_Max type = "      + str(ROI_array_recive[i][5]))

                    ROI_msg.class_name = str(ROI_array_recive[i][0])
                    ROI_msg.score      = float(ROI_array_recive[i][1])
                    ROI_msg.x_min      = int(ROI_array_recive[i][2])
                    ROI_msg.x_Max      = int(ROI_array_recive[i][3])
                    ROI_msg.y_min      = int(ROI_array_recive[i][4])
                    ROI_msg.y_Max      = int(ROI_array_recive[i][5])
                    
                    ROI_array_msg.ROI_list.append(ROI_msg)
                    suck_msg = estimation_suck_point(ROI_msg)
                roi_array_pub.publish(ROI_array_msg)
            else:
                print("no object now")
            result = np.asarray(image)
            curr_time = timer()
            exec_time = curr_time - prev_time
            prev_time = curr_time
            accum_time = accum_time + exec_time
            curr_fps = curr_fps + 1
            if accum_time > 1:
                accum_time = accum_time - 1
                fps = "FPS: " + str(curr_fps)
                curr_fps = 0
            cv2.putText(result, text=fps, org=(3, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.50, color=(255, 0, 0), thickness=2)
            if suck_msg!=None:
                cv2.circle(result, (suck_msg.Ax,suck_msg.Ay), 10, 195)
                cv2.circle(result, (suck_msg.Bx,suck_msg.By), 10, 60)
            resultimg_pub.publish(bridge.cv2_to_imgmsg(result, "bgr8"))
            # cv2.namedWindow("result", cv2.WINDOW_NORMAL)
            # cv2.imshow("result", result)
            # if isOutput:
            #     out.write(result)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
        image_flag = False
def callback(data):
    global cv_image
    global image_flag
    try:
      cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    # cv2.imshow("Image window", cv_image)
    # cv2.waitKey(3)
    image_flag = True

FLAGS = None
rospy.init_node('image_converter', anonymous=True)
roi_array_pub = rospy.Publisher("/object/ROI_array",ROI_array,queue_size=10)
suckpoint_pub = rospy.Publisher("/object/suckpoint",Suck_point,queue_size=10)
resultimg_pub = rospy.Publisher("/object/result_img",Image_ros,queue_size=10)

# ros_sub = rospy.Subscriber("/camera/rgb/image_raw",Image_ros,callback)
ros_sub = rospy.Subscriber("/usb_cam/image_raw",Image_ros,callback)
if __name__ == '__main__':

    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        '--model', type=str,
        help='path to model weight file, default ' + YOLO.get_defaults("model_path")
    )
    
    parser.add_argument(
        '--anchors', type=str,
        help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
    )

    parser.add_argument(
        '--classes', type=str,
        help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
    )

    parser.add_argument(
        '--gpu_num', type=int,
        help='Number of GPU to use, default ' + str(YOLO.get_defaults("gpu_num"))
    )

    parser.add_argument(
        '--image', default=False, action="store_true",
        help='Image detection mode, will ignore all positional arguments'
    )
    '''
    Command line positional arguments -- for video detection mode
    '''
    parser.add_argument(
        "--input", nargs='?', type=str,required=False,default='./path2your_video',
        help = "Video input path"
    )

    parser.add_argument(
        "--output", nargs='?', type=str, default="",
        help = "[Optional] Video output path"
    )

    FLAGS = parser.parse_args()

    if FLAGS.image:
        """
        Image detection mode, disregard any remaining command line arguments
        """
        print("Image detection mode")
        if "input" in FLAGS:
            print(" Ignoring remaining command line arguments: " + FLAGS.input + "," + FLAGS.output)
        detect_img(YOLO(**vars(FLAGS)))
    elif "input" in FLAGS:
        # detect_video(YOLO(**vars(FLAGS)), FLAGS.input, FLAGS.output)
        clone_detect_video(YOLO(**vars(FLAGS)), FLAGS.input, FLAGS.output)
    else:
        print("Must specify at least video_input_path.  See usage with --help.")
    print("End of this code YOLOV3!!")
