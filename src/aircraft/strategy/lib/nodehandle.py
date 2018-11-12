#!/usr/bin/env python3
# -*- coding: utf-8 -*-+

import rospy
import rospkg

import subprocess

""" ros topic lib """
from std_msgs.msg import Bool,Int32
from geometry_msgs.msg import Twist
from aircraft.msg import ROI
from yolov3_ros.msg import ROI_array
""" ros service lib """
from arm_control.srv import armCmd,armCmdResponse

FILENAME = rospkg.RosPack().get_path('aircraft')+'/config/'+'param.yaml'


class NodeHandle(object):
    r"""
        strategy
            loadParam
            start
            behavior
            isBusy
        param
            pHome: home point
            pCenter:    above item point
            pObject:    set model place pos and orientation
            rollObject: set model roll of "picking" 
            

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
        self.__ROISuccess = False

        """ define param """
        self.__pHome = {'pos':[],'euler':[]}
        self.__pCenter = {'pos':[],'euler':[]}
        self.__pCamRight = {'pos':[],'euler':[]}
        self.__pCamLeft = {'pos':[],'euler':[]}
        self.__pSuction = {'pos':[],'euler':[]}
        self.__pHead = {'pos':[],'euler':[]}
        self.__pFront = {'pos':[],'euler':[]}
        self.__pLeftWing = {'pos':[],'euler':[]}
        self.__pRightWing = {'pos':[],'euler':[]}
        self.__pRear = {'pos':[],'euler':[]}
        self.__pTail = {'pos':[],'euler':[]}
        self.__pObject = {'Head':self.__pHead,'Front':self.__pFront,'LeftWing':self.__pLeftWing,\
                        'RightWing':self.__pRightWing,'Rear':self.__pRear,'Tail':self.__pTail}

        self.__rollObject = {'Head':0,'Front':0,'LeftWing':0,'RightWing':0,'Rear':0,'Tail':0}

        self.__ROICounter = {'Head':0,'Front':0,'LeftWing':0,'RightWing':0,'Rear':0,'Tail':0}

        self.__checkROI = 5
        self.__pixelRate = 0.2
        # self.__slideX = 130.0
        # self.__slideY = 30.0
        # self.__slideZ = 10      # why 130 30 10
        self.__scoreThreshold = 0.5
        self.__flawThreshold = 50
        
        """ get vision """
        self.__itemROI = {'name':'','score':-999.0,'x_min':-999,'x_Max':-999,'y_min':-999,'y_Max':-999}
        
        """ topic pub """

        """ topic sub """
        rospy.Subscriber("aircraft/save",Bool,self.Save_Param)
        
        rospy.Subscriber("aircraft/start",Bool,self.Sub_Start)
        rospy.Subscriber("aircraft/behavior_state",Int32,self.Sub_Behavior)
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

        self.__pCamLeft['pos'] = [0.0,0.0,0.0]
        self.__pCamLeft['euler'] = [0.0,0.0,0.0]

        self.__pCamRight['pos'] = [0.0,0.0,0.0]
        self.__pCamRight['euler'] = [0.0,0.0,0.0]

        self.__pSuction['pos'] = [0.0,0.0,0.0]
        self.__pSuction['euler'] = [0.0,0.0,0.0]

        self.__pHead['pos'] = [0.0,0.0,0.0]
        self.__pHead['euler'] = [0.0,0.0,0.0]

        self.__pFront['pos'] = [0.0,0.0,0.0]
        self.__pFront['euler'] = [0.0,0.0,0.0]

        self.__pLeftWing['pos'] = [0.0,0.0,0.0]
        self.__pLeftWing['euler'] = [0.0,0.0,0.0]

        self.__pRightWing['pos'] = [0.0,0.0,0.0]
        self.__pRightWing['euler'] = [0.0,0.0,0.0]

        self.__pRear['pos'] = [0.0,0.0,0.0]
        self.__pRear['euler'] = [0.0,0.0,0.0]

        self.__pTail['pos'] = [0.0,0.0,0.0]
        self.__pTail['euler'] = [0.0,0.0,0.0]
    
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

    def Sub_Item_ROI_Array(self,msg):
        """
            msg.ROS_list[i].class_name
            msg.ROS_list[i].score
            msg.ROS_list[i].x_min
            msg.ROS_list[i].x_Max
            msg.ROS_list[i].y_min
            msg.ROS_list[i].y_Max  
        """
        
        for i in range(len(msg.ROI_list)):
            # print(msg.ROI_list[0].class_name)
            if(msg.ROI_list[i].score > self.__scoreThreshold):
                self.__ROICounter[msg.ROI_list[i].class_name] += 1

            if(self.__ROICounter[self.__itemROI['name']] > self.checkROI):
                self.__ROISuccess = True
                self.__itemROI['name']  = msg.ROI_list[i].class_name 
                self.__itemROI['score'] = msg.ROI_list[i].score
                self.__itemROI['x_min'] = msg.ROI_list[i].x_min
                self.__itemROI['x_Max'] = msg.ROI_list[i].x_Max
                self.__itemROI['y_min'] = msg.ROI_list[i].y_min
                self.__itemROI['y_Max'] = msg.ROI_list[i].y_Max
                self.__ROICounter = {'Head':0,'Front':0,'LeftWing':0,'RightWing':0,'Rear':0,'Tail':0}
                break

    def Sub_Is_Grip(sefl,msg):
        self.__isGrip = msg.data

    """ save param """
    def Save_Param(self,msg):
        self.Set_Param()
        if (rospy.has_param('accupick3d/aircraft')):
            print('dump')
            subprocess.call(['rosparam','dump',FILENAME,'/accupick3d/aircraft'])
            self.Load_Param()
        else:
            print('Not found')

        
    def Load_Param(self):
        if (rospy.has_param('accupick3d/aircraft/pHome')):
            self.__pHome = rospy.get_param("accupick3d/aircraft/pHome")
        if (rospy.has_param('accupick3d/aircraft/pCenter')):
            self.__pCenter = rospy.get_param("accupick3d/aircraft/pCenter")
        if (rospy.has_param('accupick3d/aircraft/pCamRight')):
            self.__pCamRight = rospy.get_param("accupick3d/aircraft/pCamRight")
        if (rospy.has_param('accupick3d/aircraft/pCamLeft')):
            self.__pCamLeft = rospy.get_param("accupick3d/aircraft/pCamLeft")
        if (rospy.has_param('accupick3d/aircraft/pSuction')):
            self.__pSuction = rospy.get_param("accupick3d/aircraft/pSuction")
        if (rospy.has_param('accupick3d/aircraft/pHead')):
            self.__pFlaw = rospy.get_param("accupick3d/aircraft/pHead")
        if (rospy.has_param('accupick3d/aircraft/pFront')):
            self.__pNFlaw = rospy.get_param("accupick3d/aircraft/pFront")
        if (rospy.has_param('accupick3d/aircraft/pLeftWing')):
            self.__pNFlaw = rospy.get_param("accupick3d/aircraft/pLeftWing")
        if (rospy.has_param('accupick3d/aircraft/pRightWing')):
            self.__pNFlaw = rospy.get_param("accupick3d/aircraft/pRightWing")
        if (rospy.has_param('accupick3d/aircraft/pRear')):
            self.__pNFlaw = rospy.get_param("accupick3d/aircraft/pRear")
        if (rospy.has_param('accupick3d/aircraft/pTail')):
            self.__pNFlaw = rospy.get_param("accupick3d/aircraft/pTail")
        if (rospy.has_param('accupick3d/aircraft/rollObject')):
            self.__pNFlaw = rospy.get_param("accupick3d/aircraft/rollObject")

        if (rospy.has_param('accupick3d/aircraft/checkROI')):
            self.__checkROI = rospy.get_param("accupick3d/aircraft/checkROI")
        if (rospy.has_param('accupick3d/aircraft/pixelRate')):
            self.__pixelRate = rospy.get_param("accupick3d/aircraft/pixelRate")
        # if (rospy.has_param('accupick3d/flaw_detection/slideX')):
        #     self.__slideX = rospy.get_param("accupick3d/flaw_detection/slideX")
        # if (rospy.has_param('accupick3d/flaw_detection/slideY')):
        #     self.__slideY = rospy.get_param("accupick3d/flaw_detection/slideY")
        # if (rospy.has_param('accupick3d/flaw_detection/slideZ')):
        #     self.__slideZ = rospy.get_param("accupick3d/flaw_detection/slideZ")
        if (rospy.has_param('accupick3d/aircraft/score_threshold')):
            self.__scoreThreshold = rospy.get_param("accupick3d/aircraft/score_threshold")
        if (rospy.has_param('accupick3d/aircraft/rollObject')):
            self.__scoreThreshold = rospy.get_param("accupick3d/aircraft/rollObject")

    def Set_Param(self):
        rospy.set_param('accupick3d/aircraft/pHome', self.__pHome)
        rospy.set_param('accupick3d/aircraft/pCenter', self.__pCenter)
        rospy.set_param('accupick3d/aircraft/pCamRight', self.__pCamRight)
        rospy.set_param('accupick3d/aircraft/pCamLeft', self.__pCamLeft)
        rospy.set_param('accupick3d/aircraft/pSuction', self.__pSuction)
        rospy.set_param('accupick3d/aircraft/pHead', self.__pHead)
        rospy.set_param('accupick3d/aircraft/pFront', self.__pFront)
        rospy.set_param('accupick3d/aircraft/pLeftWing', self.__pLeftWing)
        rospy.set_param('accupick3d/aircraft/pRightWing', self.__pRightWing)
        rospy.set_param('accupick3d/aircraft/pRear', self.__pRear)
        rospy.set_param('accupick3d/aircraft/pTail', self.__pTail)
        rospy.set_param('accupick3d/aircraft/rollObject', self.__rollObject)

        rospy.set_param('accupick3d/aircraft/checkROI', self.__checkROI)
        rospy.set_param('accupick3d/aircraft/pixelRate', self.__pixelRate)
        # rospy.set_param('accupick3d/flaw_detection/slideX', self.__slideX)
        # rospy.set_param('accupick3d/flaw_detection/slideY', self.__slideY)
        # rospy.set_param('accupick3d/flaw_detection/slideZ', self.__slideZ)
        rospy.set_param('accupick3d/aircraft/score_threshold', self.__scoreThreshold)
        rospy.set_param('accupick3d/aircraft/flaw_threshold', self.__flawThreshold)

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
    def pCamRight(self):
        return self.__pCamRight
    @property
    def pCamLeft(self):
        return self.__pCamLeft
    @property
    def pSuction(self):
        return self.__pSuction
    # @property
    # def pFlaw(self):
    #     return self.__pFlaw
    # @property
    # def pNFlaw(self):
    #     return self.__pNFlaw

    @property
    def checkROI(self):
        return self.__checkROI
    @property
    def pixelRate(self):
        return self.__pixelRate
    # @property
    # def slideX(self):
    #     return self.__slideX
    # @property
    # def slideY(self):
    #     return self.__slideY
    # @property
    # def slideZ(self):
    #     return self.__slideZ
    @property
    def scoreThreshold(self):
        return self.__scoreThreshold
    @property
    def flawThreshold(self):
        return self.__flawThreshold
    @property
    def isGrip(self):
        return self.__isGrip

    @property
    def pHead(self):
        return self.__pHead
    
    @property
    def pLeftWing(self):
        return self.__pLeftWing
    
    @property
    def pFront(self):
        return self.__pFront
    
    @property
    def pRightWing(self):
        return self.__pRightWing
    
    @property
    def pTail(self):
        return self.__pTail
    @property
    def pObject(self):
        return self.__pObject

    @property
    def rollObject(self):
        return self.__rollObject

    """ vision """
    @property
    def itemROI(self):
        return self.__itemROI

    @property
    def ROISuccess(self):
        return self.__ROISuccess
    
    @ROISuccess.setter
    def ROISuccess(self,value):
        self.__ROISuccess = value