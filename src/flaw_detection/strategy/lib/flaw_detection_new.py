#!/usr/bin/env python3
# -*- coding: utf-8 -*-+

import rospy
import rospkg
import copy
from lib.nodehandle import NodeHandle
from lib.counter import TimeCounter

""" lib """
from enum import Enum

""" camera param """
CAMERA_ROW = 480
CAMERA_COL = 640
CAMERA_Y_ERROR = 30
DELAY_SLIDING = 1

class State(Enum):
    r"""
        Init:
        Manual: 
        Home: go to home point
        Center:  go to track center point
        Item_Center: go to item center point
        Sliding : Slide above item 
        Suction: open suction cup
        Release_Suction: release suction cup
        Flaw_box: go to flaw bow point
        No_Flaw_box: go to Nflaw bow point
        DECIDE_BOX: 
    """
    INIT            = 0
    MANUAL          = 1
    HOME            = 2
    CENTER          = 3
    ITEM_CENTER     = 4
    SLIDING         = 5
    SUCTION         = 6
    RELEASE_SUCTION = 7
    FLAW_BOX        = 8
    NO_FLAW_BOX     = 9
    DECIDE_BOX      = 10
    DOWNFLAW        = 11
    DOWNNFLAW       = 12

class StepCenter(Enum):
    ITEM_CENTER     = 0
    SUCTION         = 1
    DECIDE_BOX      = 2

class StepSliding(Enum):
    GO_LTOP        = 0
    GO_RTOP        = 1
    GO_RBOTTOM     = 2
    GO_LBOTTOM     = 3
    GO_BACK        = 4

    GO_CTOP        = 5
    GO_CBOTOM      = 6

    GO_LCTOP        = 7
    GO_LCBOTTOM      = 8
    GO_RCTOP        = 9
    GO_RCBOTTOM      = 10

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
        self.__stepCenter = StepCenter.ITEM_CENTER.value
        self.__stepSliding = StepSliding.GO_LTOP.value
        # self.__state = State.INIT.value
        self.__strategyBusy = -1
        self.__success = False

        # self.__itemCounter = 0
        # self.__flawConuter = 0
        self.__flaw = False

        self.__checkArrive = 0
        self.__pItemCenter = {'pos':[],'euler':[]}
        
        self.__pSliding = {'pos':[],'euler':[]}

        self.__slidingStep = 0

        self.__reSuc = 0
    
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
                    self.__stepCenter = StepCenter.ITEM_CENTER.value
                    self.nh.itemCounter = 0

            elif(self.__state == State.CENTER.value):
                print('Center')
                goal_pos = copy.deepcopy(self.nh.pCenter)
                if(self.__stepCenter is not StepCenter.ITEM_CENTER.value):
                    goal_pos['pos'][2] = 500
                if(self.P2P_Strategy(goal_pos)):
                    if(self.__stepCenter == StepCenter.ITEM_CENTER.value):
                        self.__checkArrive = 0
                        # if(self.nh.itemCounter > self.nh.checkROI):
                        self.__state = State.ITEM_CENTER.value
                        self.__pItemCenter = {'pos':[],'euler':[]}  #####
                    elif(self.__stepCenter == StepCenter.SUCTION.value):
                        self.__state = State.SUCTION.value
                    elif(self.__stepCenter == StepCenter.DECIDE_BOX.value):
                        if(self.nh.isGrip is True):
                            self.__reSuc  = 0
                            self.__state = State.DECIDE_BOX.value
                        else:
                            self.__reSuc += 1
                            self.__state = State.SUCTION.value
                            self.nh.Suction_cmd('vacuumOff')
            
            elif(self.__state == State.ITEM_CENTER.value):
                # print('Item Center')
                if(self.Item_Center_Strategy()):
                    self.__state = State.SLIDING.value
            
            elif(self.__state == State.SLIDING.value):
                print('Sliding')
                if(self.Sliding_Strategy()):
                    self.__state = State.CENTER.value
                    self.__stepCenter = StepCenter.SUCTION.value
                pass
            
            #########################################
            elif(self.__state == State.SUCTION.value):
                print('suction')
                goal_pos = copy.deepcopy(self.__pItemCenter)
                goal_pos['pos'][2] = copy.deepcopy(self.nh.pSuction['pos'][2])
                if(self.__reSuc is not 0):
                    goal_pos['euler'][0] += (2*(self.__reSuc % 2) - 1) * 20
                if(self.P2P_Strategy(goal_pos)):
                    self.nh.Suction_cmd('vacuumOn')
                    self.__state = State.CENTER.value
                    self.__stepCenter = StepCenter.DECIDE_BOX.value
                pass
            #########################################
            elif(self.__state == State.RELEASE_SUCTION.value):
                print('release suction')
                self.nh.Suction_cmd('vacuumOff')
                # self.__state = State.CENTER.value
                # self.__stepCenter = StepCenter.ITEM_CENTER.value
                self.nh.itemCounter = 0
                self.__pItemCenter = {'pos':[],'euler':[]}
                if(self.__flaw):
                    self.__state = State.FLAW_BOX.value
                else:
                    self.__state = State.NO_FLAW_BOX.value
                pass
                    
            elif(self.__state == State.FLAW_BOX.value):
                print('Flaw box',self.nh.flawConuter)
                if(self.P2P_Strategy(self.nh.pFlaw)):
                    if(self.nh.isGrip is True):
                        self.__state = State.DOWNFLAW.value
                    else:
                        self.__state = State.CENTER.value
                        self.__stepCenter = StepCenter.ITEM_CENTER.value
                    

            elif(self.__state == State.DOWNFLAW.value):
                goal_pos = copy.deepcopy(self.nh.pFlaw)
                goal_pos['pos'][2] -= 100
                print('Flaw box',self.nh.flawConuter)
                if(self.P2P_Strategy(goal_pos)):
                    self.__state = State.RELEASE_SUCTION.value

            elif(self.__state == State.NO_FLAW_BOX.value):
                print('NFlaw box',self.nh.flawConuter)
                if(self.P2P_Strategy(self.nh.pNFlaw)):
                    if(self.nh.isGrip is True):
                        self.__state = State.DOWNNFLAW.value
                    else:
                        self.__state = State.CENTER.value
                        self.__stepCenter = StepCenter.ITEM_CENTER.value

            elif(self.__state == State.DOWNNFLAW.value):
                goal_pos = copy.deepcopy(self.nh.pNFlaw)
                goal_pos['pos'][2] -= 100
                print('NFlaw box',self.nh.flawConuter)
                if(self.P2P_Strategy(goal_pos)):
                    self.__state = State.RELEASE_SUCTION.value

            elif(self.__state == State.DECIDE_BOX.value):
                if(self.__flaw):
                    self.__state = State.FLAW_BOX.value
                else:
                    self.__state = State.NO_FLAW_BOX.value

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
                print('fuck!!!!!!!!!!!!!')
                return True
        return False
    
    def Item_Center_Strategy(self):
        print('item center arrive',self.__checkArrive,self.nh.checkROI)
        if(self.__checkArrive >= self.nh.checkROI):
            if(self.nh.itemROI['name'] == 'metal' and len(self.__pItemCenter['pos']) == 0):
                x,y = self.Pixel_To_mm()
                print('fuck  ',x,y)
                self.__pItemCenter['pos'].append(self.nh.pCenter['pos'][0]+x)
                self.__pItemCenter['pos'].append(self.nh.pCenter['pos'][1]+y+CAMERA_Y_ERROR)
                self.__pItemCenter['pos'].append(self.nh.pCenter['pos'][2]-50)

                # if(self.__pItemCenter['pos'][1] > 450):
                #     self.__pItemCenter['pos'][1] = 450

                self.__pItemCenter['euler'].append(self.nh.pCenter['euler'][0])
                self.__pItemCenter['euler'].append(self.nh.pCenter['euler'][1])
                self.__pItemCenter['euler'].append(self.nh.pCenter['euler'][2])
            elif(len(self.__pItemCenter['pos']) != 0):
                print('item center',self.__pItemCenter['pos'])
                return self.P2P_Strategy(self.__pItemCenter)
                
        else:
            if(self.nh.itemROI['name'] == 'metal'):
                if(self.nh.itemROI['score'] >= self.nh.scoreThreshold):
                    self.__checkArrive += 1
                    self.nh.itemROI = {'name':'','score':-999.0,'x_min':-999,'x_Max':-999,'y_min':-999,'y_Max':-999}
        return False
    
    def Sliding_Strategy(self):
        # if(self.__slidingStep == 0):
        #     if(len(self.__pSliding['pos']) == 0):
        #         self.__pSliding['pos'].append(self.__pItemCenter['pos'][0])
        #         self.__pSliding['pos'].append(self.__pItemCenter['pos'][1])
        #         self.__pSliding['pos'].append(self.__pItemCenter['pos'][2]+self.nh.slideZ)

        #         self.__pSliding['euler'].append(self.__pItemCenter['euler'][0])
        #         self.__pSliding['euler'].append(self.__pItemCenter['euler'][1])
        #         self.__pSliding['euler'].append(self.__pItemCenter['euler'][2])
        #     elif(len(self.__pItemCenter['pos']) != 0):
        #         if(self.P2P_Strategy(self.__pItemCenter)):
        #             self.__slidingStep = 1
        # return False
        ################################################################
        # print('sliding item center',self.__pItemCenter['pos'])
        print('sliding flawcounter: ',self.nh.flawConuter)
        if(self.__stepSliding == StepSliding.GO_LTOP.value):
            goal_pos = copy.deepcopy(self.__pItemCenter)
            # print('fuck11111111',goal_pos['pos'])
            goal_pos['pos'][0] -= self.nh.slideX
            goal_pos['pos'][1]  = (goal_pos['pos'][1]-CAMERA_Y_ERROR)+self.nh.slideY
            goal_pos['pos'][2]  = self.nh.slideZ
            # print('fuck222222',goal_pos['pos'])
            # if(self.P2P_Strategy(goal_pos)):
            #     self.__stepSliding = StepSliding.GO_CTOP.value
            #     self.nh.flawConuter = 0
            #     self.__flaw = False

            if(self.P2P_Strategy(goal_pos)):
                self.__stepSliding = StepSliding.GO_LCTOP.value
                self.nh.flawConuter = 0
                self.__flaw = False

        elif(self.__stepSliding == StepSliding.GO_LCTOP.value):
            goal_pos = copy.deepcopy(self.__pItemCenter)
            # print('fuck11111111',goal_pos['pos'])
            goal_pos['pos'][0] -= 50
            goal_pos['pos'][1]  = (goal_pos['pos'][1]-CAMERA_Y_ERROR)+self.nh.slideY
            goal_pos['pos'][2]  = self.nh.slideZ
            # print('fuck222222',goal_pos['pos'])
            if(self.P2P_Strategy(goal_pos)):
                self.Delay(DELAY_SLIDING)
                if(self.nh.flawConuter >= self.nh.flawThreshold):
                    self.__stepSliding = StepSliding.GO_BACK.value
                    self.__flaw = True
                else:
                    self.__stepSliding = StepSliding.GO_CTOP.value

        elif(self.__stepSliding == StepSliding.GO_CTOP.value):
            goal_pos = copy.deepcopy(self.__pItemCenter)
            # print('fuck11111111',goal_pos['pos'])
            goal_pos['pos'][1]  = (goal_pos['pos'][1]-CAMERA_Y_ERROR)+self.nh.slideY
            goal_pos['pos'][2]  = self.nh.slideZ
            # print('fuck222222',goal_pos['pos'])
            if(self.P2P_Strategy(goal_pos)):
                if(self.nh.flawConuter >= self.nh.flawThreshold):
                    self.__stepSliding = StepSliding.GO_BACK.value
                    self.__flaw = True
                else:
                    # self.__stepSliding = StepSliding.GO_RTOP.value
                    self.__stepSliding = StepSliding.GO_RCTOP.value
        
        elif(self.__stepSliding == StepSliding.GO_RCTOP.value):
            goal_pos = copy.deepcopy(self.__pItemCenter)
            # print('fuck11111111',goal_pos['pos'])
            goal_pos['pos'][0] += 50
            goal_pos['pos'][1]  = (goal_pos['pos'][1]-CAMERA_Y_ERROR)+self.nh.slideY
            goal_pos['pos'][2]  = self.nh.slideZ
            # print('fuck222222',goal_pos['pos'])
            if(self.P2P_Strategy(goal_pos)):
                self.Delay(DELAY_SLIDING)
                if(self.nh.flawConuter >= self.nh.flawThreshold):
                    self.__stepSliding = StepSliding.GO_BACK.value
                    self.__flaw = True
                else:
                    self.__stepSliding = StepSliding.GO_RTOP.value

        elif(self.__stepSliding == StepSliding.GO_RTOP.value):
            goal_pos = copy.deepcopy(self.__pItemCenter)
            # print('11111111',goal_pos)
            goal_pos['pos'][0] += self.nh.slideX
            goal_pos['pos'][1]  = (goal_pos['pos'][1]-CAMERA_Y_ERROR)+self.nh.slideY
            goal_pos['pos'][2]  = self.nh.slideZ
            # print('22222222',goal_pos)
            if(self.P2P_Strategy(goal_pos)):
                if(self.nh.flawConuter >= self.nh.flawThreshold):
                    self.__stepSliding = StepSliding.GO_BACK.value
                    self.__flaw = True
                else:
                    self.__stepSliding = StepSliding.GO_RBOTTOM.value

        elif(self.__stepSliding == StepSliding.GO_RBOTTOM.value):
            goal_pos = copy.deepcopy(self.__pItemCenter)
            goal_pos['pos'][0] += self.nh.slideX
            goal_pos['pos'][1]  = (goal_pos['pos'][1]-CAMERA_Y_ERROR)-self.nh.slideY
            goal_pos['pos'][2]  = self.nh.slideZ
            if(self.P2P_Strategy(goal_pos)):
                if(self.nh.flawConuter >= self.nh.flawThreshold):
                    self.__stepSliding = StepSliding.GO_BACK.value
                    self.__flaw = True
                else:
                    # self.__stepSliding = StepSliding.GO_CBOTOM.value
                    self.__stepSliding = StepSliding.GO_RCBOTTOM.value
        
        elif(self.__stepSliding == StepSliding.GO_RCBOTTOM.value):
            goal_pos = copy.deepcopy(self.__pItemCenter)
            goal_pos['pos'][0] += 50
            goal_pos['pos'][1]  = (goal_pos['pos'][1]-CAMERA_Y_ERROR)-self.nh.slideY
            goal_pos['pos'][2]  = self.nh.slideZ
            if(self.P2P_Strategy(goal_pos)):
                self.Delay(DELAY_SLIDING)
                if(self.nh.flawConuter >= self.nh.flawThreshold):
                    self.__stepSliding = StepSliding.GO_BACK.value
                    self.__flaw = True
                else:
                    self.__stepSliding = StepSliding.GO_CBOTOM.value

        elif(self.__stepSliding == StepSliding.GO_CBOTOM.value):
            goal_pos = copy.deepcopy(self.__pItemCenter)
            # print('fuck11111111',goal_pos['pos'])
            goal_pos['pos'][1]  = (goal_pos['pos'][1]-CAMERA_Y_ERROR)-self.nh.slideY
            goal_pos['pos'][2]  = self.nh.slideZ
            # print('fuck222222',goal_pos['pos'])
            if(self.P2P_Strategy(goal_pos)):
                if(self.nh.flawConuter >= self.nh.flawThreshold):
                    self.__stepSliding = StepSliding.GO_BACK.value
                    self.__flaw = True
                else:
                    # self.__stepSliding = StepSliding.GO_LBOTTOM.value
                    self.__stepSliding = StepSliding.GO_LCBOTTOM.value
        
        elif(self.__stepSliding == StepSliding.GO_LCBOTTOM.value):
            goal_pos = copy.deepcopy(self.__pItemCenter)
            # print('fuck11111111',goal_pos['pos'])
            goal_pos['pos'][0] -= 50
            goal_pos['pos'][1]  = (goal_pos['pos'][1]-CAMERA_Y_ERROR)-self.nh.slideY
            goal_pos['pos'][2]  = self.nh.slideZ
            # print('fuck222222',goal_pos['pos'])
            if(self.P2P_Strategy(goal_pos)):
                self.Delay(DELAY_SLIDING)
                if(self.nh.flawConuter >= self.nh.flawThreshold):
                    self.__stepSliding = StepSliding.GO_BACK.value
                    self.__flaw = True
                else:
                    self.__stepSliding = StepSliding.GO_LBOTTOM.value


        elif(self.__stepSliding == StepSliding.GO_LBOTTOM.value):
            goal_pos = copy.deepcopy(self.__pItemCenter)
            goal_pos['pos'][0] -= self.nh.slideX
            goal_pos['pos'][1]  = (goal_pos['pos'][1]-CAMERA_Y_ERROR)-self.nh.slideY
            goal_pos['pos'][2]  = self.nh.slideZ
            if(self.P2P_Strategy(goal_pos)):
                if(self.nh.flawConuter >= self.nh.flawThreshold):
                    self.__flaw = True
                self.__stepSliding = StepSliding.GO_BACK.value

        elif(self.__stepSliding == StepSliding.GO_BACK.value):
            if(self.P2P_Strategy(self.__pItemCenter)):
                self.__stepSliding = StepSliding.GO_LTOP.value
                return True
        return False

    def Manual_Strategy(self):
        pass

    """ tool """
    def Pixel_To_mm(self):
        x = (self.nh.itemROI['x_min']+self.nh.itemROI['x_Max'])/2.0
        y = (self.nh.itemROI['y_min']+self.nh.itemROI['y_Max'])/2.0

        # y_dis = -((CAMERA_ROW/2)-x)
        # x_dis = -((CAMERA_COL/2)-y)

        x_dis = (x-(CAMERA_COL/2))
        y_dis = -(y-(CAMERA_ROW/2))

        return x_dis*self.nh.pixelRate, y_dis*self.nh.pixelRate

    def Delay(self,time):
        """ second """
        d = rospy.Duration(time)
        rospy.sleep(d)