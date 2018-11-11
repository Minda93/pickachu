# Pickupthon
## 1.Envirment setting
1.1 Download weight and put paste in "yolov3_ros/model/"
```
https://l.facebook.com/l.php?u=https%3A%2F%2Fdrive.google.com%2Ffile%2Fd%2F15TyEzjodEoEJec6sh38In1EkzRTKAOYT%2Fview%3Fusp%3Dsharing%26fbclid%3DIwAR3pn2dIV08p7QyfSpIsLqPpKY49R0axgp7_dJw2ZJWqsgpc20HWMOlHmpw&h=AT2FubC5h167-6VFSb_VApMlqpuQCWaTjN_Eak4nZ5stsvPf5VcQZvIyYgmKTC8-xnuLKEH8MDWgCbnRjTb6Ct42bPuIbRN12EODyDYbkKZwdZ3bF1V3x_3qpQWp8g
```
1.2 Install dependence
```
sudo apt-get install ros-kinetic-usb-cam ros-kinetic-web-video-server ros-kinetic-rosbridge-server -y 
```
---
## 2.Run program
2.1 Run each command in differenet terminal
```
roslaunch usb_cam usbcam_start.launch
rosrun yolov3_ros yolo_video.py 
```
2.2 Open the GUI from "pickupthon/GUI/ImageProcessInterface.html"
