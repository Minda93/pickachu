#!/usr/bin/env python3
# -*- coding: utf-8 -*-+

import rospy
import rospkg

import subprocess

""" ros topic lib """
from std_msgs.msg import Bool,Int32
from geometry_msgs.msg import Twist

""" ros service lib """
from arm_control.srv import armCmd,armCmdResponse

FILENAME = rospkg.RosPack().get_path('flaw_detection')+'/config/'+'param.yaml'


class NodeHandle(object):
    r"""
        strategy
            loadParam
            start
            behavior
            isBusy
        param
            pHome
            pCenter
            pFlaw
            pNFlaw
        get vision
            pItem: get item center
            pItemFlaw: get flaw center
    """
    def __init__(self):
        """ strategy """
        self.__loadParam = False
        self.__start = 1
        self.__behavior = 0
        self.__isBusy = False

        """ define param """
        self.__pHome = {'pos':[],'euler':[]}
        self.__pCenter = {'pos':[],'euler':[]}
        self.__pFlaw = {'pos':[],'euler':[]}
        self.__pNFlaw = {'pos':[],'euler':[]}
        
        """ get vision """
        self.__pItem = []
        self.__pItemFlaw = []
        
        """ topic pub """

        """ topic sub """
        
        rospy.Subscriber("flaw_detection/save",Bool,self.Save_Param)
        
        rospy.Subscriber("flaw_detection/start",Bool,self.Sub_Start)
        rospy.Subscriber("flaw_detection/behavior_state",Int32,self.Sub_Behavior)
        rospy.Subscriber("/accupick3d/is_busy",Bool,self.Sub_Is_Busy)

        rospy.Subscriber("flaw_detection/pItem",Bool,self.Sub_pItem)
        rospy.Subscriber("flaw_detection/pItemFlaw",Bool,self.Sub_pItem_Flaw)

        self.Load_Param()
        # self.Test_Param()

    def Test_Param(self):
        self.__pHome['pos'] = [0.0,0.0,0.0]
        self.__pHome['euler'] = [0.0,0.0,0.0]

        self.__pCenter['pos'] = [0.0,0.0,0.0]
        self.__pCenter['euler'] = [0.0,0.0,0.0]

        self.__pFlaw['pos'] = [0.0,0.0,0.0]
        self.__pFlaw['euler'] = [0.0,0.0,0.0]

        self.__pNFlaw['pos'] = [0.0,0.0,0.0]
        self.__pNFlaw['euler'] = [0.0,0.0,0.0]
    
    """ sub """
    def Sub_Start(self,msg):
        self.__start = msg.data

    def Sub_Behavior(self,msg):
        self.__behavior = msg.data
        self.loadParam = True

    def Sub_Is_Busy(self,msg):
        self.__isBusy = msg.data

    def Sub_pItem(self,msg):
        pass

    def Sub_pItem_Flaw(self,msg):
        pass

    """ save param """
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

    """ service client """
    def Arm_Contorl(self,cmd,pos_):
        rospy.wait_for_service('/accupick3d/arm_contol')
        try:
            print(cmd,pos_['pos'],pos_['euler'])
            armControl = rospy.ServiceProxy('/accupick3d/arm_contol', armCmd)
            res = armControl(cmd, pos_['pos'],pos_['euler'])
            return res.success
        except (rospy.ServiceException, e):
            print("Service call failed: %s" %e)

    """ strategy """
    @property
    def loadParam(self):
        return self.__loadParam

    @loadParam.setter
    def loadParam(self, value):
        self.__loadParam = value
    
    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, value):
        self.__start = value

    @property
    def behavior(self):
        return self.__behavior

    @behavior.setter
    def behavior(self, value):
        self.__behavior = value

    @property
    def isBusy(self):
        return self.__isBusy

    """ param """
    @property
    def pHome(self):
        return self.__pHome
    @property
    def pCenter(self):
        return self.__pCenter
    @property
    def pFlaw(self):
        return self.__pFlaw
    @property
    def pNFlaw(self):
        return self.__pNFlaw


    """ vision """
    @property
    def pItem(self):
        return self.__pItem
    @property
    def pItemFlaw(self):
        return self.__pItemFlaw