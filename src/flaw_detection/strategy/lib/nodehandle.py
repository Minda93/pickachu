#!/usr/bin/env python3
# -*- coding: utf-8 -*-+

import rospy
import rospkg

import subprocess

""" ros topic lib """
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist

FILENAME = rospkg.RosPack().get_path('flaw_detection')+'/config/'+'param.yaml'


class Pos(object):
    def __init__(self):
        self.pos = []
        self.euler = []

class NodeHandle(object):
    r"""
        strategy
            loadParam
            start
        param
            pHome
            pCenter
            pFlaw
            pNFlaw  
    """
    def __init__(self):
        self.__loadParam = False
        self.__start = False


        """ define param """
        self.__pHome = Pos()
        self.__pCenter = Pos()
        self.__pFlaw = Pos()
        self.__pNFlaw = Pos()
        
        """ topic pub """

        """ topic sub """
        rospy.Subscriber("accupick3d/save_param",Bool,self.Save_Param)
        
    def Save_Param(self,msg):
        self.Set_Param()
        if (rospy.has_param('accupick3d/flaw_detection')):
            print('dump')
            subprocess.call(['rosparam','dump',FILENAME,'/accupick3d/flaw_detection'])
            self.Load_Param()
        else:
            print('Not found')

        
    def Load_Param(self):
        if (rospy.has_param('accupick3d/flaw_detection/pHome')):
            self.__pHome = rospy.get_param("accupick3d/flaw_detection/pHome")
        if (rospy.has_param('accupick3d/flaw_detection/pCenter')):
            self.__pCenter = rospy.get_param("accupick3d/flaw_detection/pCenter")
        if (rospy.has_param('accupick3d/flaw_detection/pFlaw')):
            self.__pFlaw = rospy.get_param("accupick3d/flaw_detection/pFlaw")
        if (rospy.has_param('accupick3d/flaw_detection/pNFlaw')):
            self.__pNFlaw = rospy.get_param("accupick3d/flaw_detection/pNFlaw")

    def Set_Param(self):
        rospy.set_param('accupick3d/flaw_detection/pHome', self.__pHome)
        rospy.set_param('accupick3d/flaw_detection/pCenter', self.__pCenter)
        rospy.set_param('accupick3d/flaw_detection/pFlaw', self.__pFlaw)
        rospy.set_param('accupick3d/flaw_detection/pNFlaw', self.__pNFlaw)