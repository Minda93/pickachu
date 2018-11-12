#!/usr/bin/env python3
# -*- coding: utf-8 -*-+

import rospy
import rospkg

import subprocess

""" ros topic lib """
from std_msgs.msg import Bool,Int32
from geometry_msgs.msg import Twist
from flaw_detection.msg import ROI
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
            pHome: home point
            pCenter:  above item point
            pFlaw:  flaw box point
            pNFlaw: Nflaw box point

            checkROI: 
            pixelRate: 
            slide_x: move slide x distance
            slide_y: move slide y distance
            scoreThreshold: detect flaw score threshold
            flawThreshold: calculate number of flaw threshold
        get vision
            itemROI: get item center
    """
    def __init__(self):
        """ strategy """
        self.__loadParam = False
        self.__start = 0
        self.__behavior = 0
        self.__isBusy = False
        self.__isGrip = False

        """ define param """
        self.__pHome = {'pos':[],'euler':[]}
        self.__pCenter = {'pos':[],'euler':[]}
        self.__pSuction = {'pos':[],'euler':[]}
        self.__pFlaw = {'pos':[],'euler':[]}
        self.__pNFlaw = {'pos':[],'euler':[]}

        self.__checkROI = 100
        self.__pixelRate = 0.2
        self.__slideX = 130.0
        self.__slideY = 30.0
        self.__slideZ = 10      # why 130 30 10
        self.__scoreThreshold = 0.5
        self.__flawThreshold = 1000
        
        """ get vision """
        self.__itemROI = {'name':'','score':-999.0,'x_min':-999,'x_Max':-999,'y_min':-999,'y_Max':-999}
        
        """ topic pub """

        """ topic sub """
        rospy.Subscriber("flaw_detection/save",Bool,self.Save_Param)
        
        rospy.Subscriber("flaw_detection/start",Bool,self.Sub_Start)
        rospy.Subscriber("flaw_detection/behavior_state",Int32,self.Sub_Behavior)
        rospy.Subscriber("/accupick3d/is_busy",Bool,self.Sub_Is_Busy)

        rospy.Subscriber("/object/ROI",ROI,self.Sub_Item_ROI)
        rospy.Subscriber('right/is_grip',Bool,self.Sub_Is_Grip)

        self.Load_Param()
        # self.Test_Param()

    def Test_Param(self):
        self.__pHome['pos'] = [0.0,0.0,0.0]
        self.__pHome['euler'] = [0.0,0.0,0.0]

        self.__pCenter['pos'] = [0.0,0.0,0.0]
        self.__pCenter['euler'] = [0.0,0.0,0.0]

        self.__pSuction['pos'] = [0.0,0.0,0.0]
        self.__pSuction['euler'] = [0.0,0.0,0.0]

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

    def Sub_Item_ROI(self,msg):
        self.__itemROI['name'] = msg.class_name
        self.__itemROI['score'] = msg.score
        self.__itemROI['x_min'] = msg.x_min
        self.__itemROI['x_Max'] = msg.x_Max
        self.__itemROI['y_min'] = msg.y_min
        self.__itemROI['y_Max'] = msg.y_Max

    def Sub_Is_Grip(sefl,msg):
        self.__isGrip = msg.data

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
        if (rospy.has_param('accupick3d/flaw_detection/pSuction')):
            self.__pSuction = rospy.get_param("accupick3d/flaw_detection/pSuction")
        if (rospy.has_param('accupick3d/flaw_detection/pFlaw')):
            self.__pFlaw = rospy.get_param("accupick3d/flaw_detection/pFlaw")
        if (rospy.has_param('accupick3d/flaw_detection/pNFlaw')):
            self.__pNFlaw = rospy.get_param("accupick3d/flaw_detection/pNFlaw")
        
        if (rospy.has_param('accupick3d/flaw_detection/checkROI')):
            self.__checkROI = rospy.get_param("accupick3d/flaw_detection/checkROI")
        if (rospy.has_param('accupick3d/flaw_detection/pixelRate')):
            self.__pixelRate = rospy.get_param("accupick3d/flaw_detection/pixelRate")
        if (rospy.has_param('accupick3d/flaw_detection/slideX')):
            self.__slideX = rospy.get_param("accupick3d/flaw_detection/slideX")
        if (rospy.has_param('accupick3d/flaw_detection/slideY')):
            self.__slideY = rospy.get_param("accupick3d/flaw_detection/slideY")
        if (rospy.has_param('accupick3d/flaw_detection/slideZ')):
            self.__slideZ = rospy.get_param("accupick3d/flaw_detection/slideZ")
        if (rospy.has_param('accupick3d/flaw_detection/score_threshold')):
            self.__scoreThreshold = rospy.get_param("accupick3d/flaw_detection/score_threshold")
        if (rospy.has_param('accupick3d/flaw_detection/flaw_threshold')):
            self.__flawThreshold = rospy.get_param("accupick3d/flaw_detection/flaw_threshold")

    def Set_Param(self):
        rospy.set_param('accupick3d/flaw_detection/pHome', self.__pHome)
        rospy.set_param('accupick3d/flaw_detection/pCenter', self.__pCenter)
        rospy.set_param('accupick3d/flaw_detection/pSuction', self.__pSuction)
        rospy.set_param('accupick3d/flaw_detection/pFlaw', self.__pFlaw)
        rospy.set_param('accupick3d/flaw_detection/pNFlaw', self.__pNFlaw)

        rospy.set_param('accupick3d/flaw_detection/checkROI', self.__checkROI)
        rospy.set_param('accupick3d/flaw_detection/pixelRate', self.__pixelRate)
        rospy.set_param('accupick3d/flaw_detection/slideX', self.__slideX)
        rospy.set_param('accupick3d/flaw_detection/slideY', self.__slideY)
        rospy.set_param('accupick3d/flaw_detection/slideZ', self.__slideZ)
        rospy.set_param('accupick3d/flaw_detection/score_threshold', self.__scoreThreshold)
        rospy.set_param('accupick3d/flaw_detection/flaw_threshold', self.__flawThreshold)

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

    def Suction_cmd(self, cmd):
        # suction_service = self.name + '/suction_cmd'
        # try:
        #     rospy.wait_for_service(suction_service, timeout=1.)
        # except rospy.ROSException as e:
        #     rospy.logwarn('wait_for_service timeout')
        #     self.robot_cmd_client(cmd)
        rospy.wait_for_service('right/suction_cmd')
        try:
            client = rospy.ServiceProxy(
                'right/suction_cmd',
                VacuumCmd
            )
            res = client(cmd)
            print(res)
        except (rospy.ServiceException, e):
            print("Service call (Vacuum) failed: %s" % e)

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
    def pSuction(self):
        return self.__pSuction
    @property
    def pFlaw(self):
        return self.__pFlaw
    @property
    def pNFlaw(self):
        return self.__pNFlaw

    @property
    def checkROI(self):
        return self.__checkROI
    @property
    def pixelRate(self):
        return self.__pixelRate
    @property
    def slideX(self):
        return self.__slideX
    @property
    def slideY(self):
        return self.__slideY
    @property
    def slideZ(self):
        return self.__slideZ
    @property
    def scoreThreshold(self):
        return self.__scoreThreshold
    @property
    def flawThreshold(self):
        return self.__flawThreshold
    @property
    def isGrip(self):
        return self.__isGrip

    """ vision """
    @property
    def itemROI(self):
        return self.__itemROI