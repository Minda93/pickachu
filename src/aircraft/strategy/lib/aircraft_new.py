#!/usr/bin/env python3
# -*- coding: utf-8 -*-+

import rospy
import rospkg
import copy
from lib.nodehandle_new import NodeHandle
from lib.counter import TimeCounter

""" lib """
from enum import Enum

""" camera param """
CAMERA_ROW = 480
CAMERA_COL = 640

class State(Enum):
    r"""
        Init:
        Manual: 
        Home: go to home point
        Center:  go to track center point
        Item_Center: go to item center point
        CAM : go to left or right camPos
        Suction: open suction cup and move to object
        Release_Suction: release suction cup
        Flaw_box: go to flaw bow point
        No_Flaw_box: go to Nflaw bow point
        DECIDE_BOX: 
    """
    INIT            = 0
    MANUAL          = 1
    HOME            = 2
    CENTER          = 3
    CAM             = 4
    CAMLEFT         = 5
    ITEM_CENTER     = 6
    SUCTION         = 7
    PLACE           = 8
    RELEASE_SUCTION = 9
    DECIDE_PLACE    = 10
    ITEM_CENTER_FIRST = 11
    SUCTION_UP      = 12
    RESUC           = 13

class StepCenter(Enum):
    CAM             = 0
    DECIDE_PLACE    = 1

class Strategy(object):
    r"""
        variable
            nodehandle
                nh
            strategy
                state: strategy behavior
                strategyBusy: 
                    -1: call armCmd service
                    0 : check armCmd is for work
                    1 : execute
                success: check armCmd service
                itemCounter: calculate number of item
                flawConuter: calculate number of flaw
                flaw:
                    0: don't have flaw 
                    1: have flaw
                checkArrive: check item arrive
                pItemCenter: item center this time
        strategy function
            INIT
            P2P
            Item_Center
            Manual
        Tool
            Pixel_To_mm: vision center and item center error pixel to mm
            Delay: second
    """
    def __init__(self):
        self.nh = NodeHandle()

        self.__state = State.INIT.value
        self.__stepCenter = StepCenter.CAM.value
        self.__strategyBusy = -1
        
        self.__success = False
        self.__camSide = False
        self.__ROIFail = 0
        self.__checkArrive = 0
        self.__cntItemCenter = 0

        self.__pItemCenter = {'pos':[],'euler':[]}
        self.__ObjectName = ''
        self.__cam_pos = {'pos':[],'euler':[]}
    
    def Run(self):
        if(self.nh.start == True):
            if(self.nh.loadParam == True):
                self.__state = self.nh.behavior
                self.nh.loadParam = False

            if(self.__state == State.INIT.value):
                print('Init')
                if(self.Init_Strategy()):
                    self.__state = State.HOME.value

            elif(self.__state == State.HOME.value):
                print('Home') 
                print(self.nh.pHome['pos'],self.nh.pHome['euler'])
                if(self.P2P_Strategy(self.nh.pHome)):
                    self.__state = State.CENTER.value
                    self.__stepCenter = StepCenter.CAM.value
                    self.nh.itemCounter = 0

            elif(self.__state == State.CENTER.value):
                print('Center')
                if(self.P2P_Strategy(self.nh.pCenter)):
                    if(self.__stepCenter == StepCenter.CAM.value):
                        self.__state = State.CAM.value
                    elif(self.__stepCenter == StepCenter.DECIDE_PLACE.value):
                        if(self.nh.isGrip is True):
                            self.__state = State.DECIDE_PLACE.value
                        else:
                            self.__stepCenter = StepCenter.CAM.value
                            self.nh.Suction_cmd('vacuumOff')

            elif(self.__state == State.CAM.value):
                if(self.__camSide):
                    print('CAM_RIGHT')
                    self.__cam_pos = copy.deepcopy(self.nh.pCamRight)
                else:
                    print('CAM_LEFT')
                    self.__cam_pos = copy.deepcopy(self.nh.pCamLeft)
                if(self.P2P_Strategy(self.__cam_pos)):
                    self.__state = State.ITEM_CENTER_FIRST.value
                    self.__pItemCenter = {'pos':[],'euler':[]}

            elif(self.__state == State.ITEM_CENTER_FIRST.value):
                # print('Item Center')
                if(self.__ROIFail > 1000):
                    self.__ROIFail = 0
                    self.__camSide = not self.__camSide
                    self.__state = State.CAM.value
                if(self.Item_Center_Strategy()):
                    nh.goalObject = self.__ObjectName
                    self.__camSide = not self.__camSide
                    self.__state = State.ITEM_CENTER.value

            elif(self.__state == State.ITEM_CENTER.value):
                # print('Item Center')
                if(self.__ROIFail > 1000):
                    self.__ROIFail = 0
                    self.__camSide = not self.__camSide
                    self.__state = State.CAM.value
                if(self.Item_Center_Strategy()):
                    nh.goalObject = 'all'
                    self.__camSide = not self.__camSide
                    self.__state = State.SUCTION.value
                    self.nh.Suction_cmd('vacuumOn')

            #########################################
            elif(self.__state == State.SUCTION.value):
                print('suction')
                goal_pos = copy.deepcopy(self.__pItemCenter)
                goal_pos['pos'][2] = copy.deepcopy(self.nh.suctionZ[self.__ObjectName])
                print(goal_pos)
                if(self.P2P_Strategy(goal_pos)):
                    if(self.nh.isGrip is True):
                            self.__state = State.SUCTION_UP.value
                    else:
                        self.__state = State.RESUC.value
                    # self.__state = State.SUCTION_UP.value
                    # self.__state = State.CENTER.value
                    # self.__stepCenter = StepCenter.DECIDE_PLACE.value
                pass

            elif(self.__state == State.RESUC.value):
                print('re suction')
                goal_pos = copy.deepcopy(self.__pItemCenter)
                goal_pos['pos'][2] = copy.deepcopy(self.nh.pObject[self.__ObjectName][2]) - 10
                print(goal_pos)
                if(self.P2P_Strategy(goal_pos)):
                    self.__state = State.SUCTION_UP.value
                    # self.__state = State.CENTER.value
                    # self.__stepCenter = StepCenter.DECIDE_PLACE.value
                pass

            elif(self.__state == State.SUCTION_UP.value):
                print('suction_up')
                goal_pos = copy.deepcopy(self.__pItemCenter)
                goal_pos['pos'][2] = copy.deepcopy(self.__cam_pos['pos'][2])
                if(self.P2P_Strategy(goal_pos)):
                        if(self.nh.isGrip is True):
                            self.__state = State.DECIDE_PLACE.value
                        else:
                            self.__state = State.CENTER.value
                            self.__stepCenter = StepCenter.CAM.value
                            self.nh.Suction_cmd('vacuumOff')                    
                    # self.__state = State.CENTER.value
                    # self.__stepCenter = StepCenter.DECIDE_PLACE.value
                pass

            #########################################
            elif(self.__state == State.RELEASE_SUCTION.value):
                print('release suction')
                self.nh.Suction_cmd('vacuumOff')
                self.__state = State.DECIDE_PLACE.value
                self.__stepCenter = StepCenter.CAM.value
                self.nh.itemCounter = 0
                pass
                    
            elif(self.__state == State.DECIDE_PLACE.value):
                print(self.__ObjectName)
                goal_pos = copy.deepcopy(self.nh.pObject[self.__ObjectName])
                goal_pos['pos'][2] += 100
                if(self.P2P_Strategy(goal_pos)):
                    if(self.nh.isGrip is True):
                        self.__state = State.PLACE.value
                    else:
                        self.__state = State.CENTER.value
                        self.nh.Suction_cmd('vacuumOff')
                        

            elif(self.__state == State.PLACE.value):
                print('PLACE')
                if(self.P2P_Strategy(self.nh.pObject[self.__ObjectName])):
                    self.__state = State.RELEASE_SUCTION.value

            elif(self.__state == State.MANUAL.value):
                print('Manual')

            else:
                print('None')
    
    """ strategy """

    def Init_Strategy(self):
        return True
    
    def P2P_Strategy(self,location):
        if(self.__strategyBusy == -1):
            self.__success = self.nh.Arm_Contorl('p2p',location)
            if(self.__success == True):
                self.__strategyBusy = 0
                self.__success = False

        elif(self.__strategyBusy == 0):
            # if(self.nh.isBusy == True):
            #     self.__strategyBusy = 1
            # else:
            #     print("Don't get pos")
            self.__strategyBusy = 1
        else:
            if(self.nh.isBusy == False):
                self.__strategyBusy = -1
                return True
        return False
    
    def Item_Center_Strategy(self):
        if(self.nh.ROISuccess and len(self.__pItemCenter['pos']) == 0):
            x,y = self.Pixel_To_mm()
            self.__ObjectName = self.nh.itemROI['name']
            print('fuck  ',x,y)
            self.__pItemCenter['pos'].append(self.__cam_pos['pos'][0]+x)
            self.__pItemCenter['pos'].append(self.__cam_pos['pos'][1]+y+40)
            self.__pItemCenter['pos'].append(self.nh.pCenter)
            if(self.__pItemCenter['pos'][1] > 450):
                self.__pItemCenter['pos'][1] = 450

            self.__pItemCenter['euler'].append(self.nh.rollObject[self.__ObjectName])
            self.__pItemCenter['euler'].append(self.__cam_pos['euler'][1])
            self.__pItemCenter['euler'].append(self.__cam_pos['euler'][2])
            self.nh.ROISuccess = False
        elif(len(self.__pItemCenter['pos']) != 0):
            print('item center',self.__pItemCenter['pos'])
            return self.P2P_Strategy(self.__pItemCenter)
        else:
            self.__ROIFail += 1
        return False

    def Manual_Strategy(self):
        pass

    """ tool """
    def Pixel_To_mm(self):
        x = (self.nh.itemROI['x_min']+self.nh.itemROI['x_Max'])/2.0
        y = (self.nh.itemROI['y_min']+self.nh.itemROI['y_Max'])/2.0

        x_dis = -(x-(CAMERA_COL/2))
        y_dis = (y-(CAMERA_ROW/2))

        return x_dis*self.nh.pixelRate, y_dis*self.nh.pixelRate

    def Delay(self,time):
        """ second """
        d = rospy.Duration(time)
        rospy.sleep(d)