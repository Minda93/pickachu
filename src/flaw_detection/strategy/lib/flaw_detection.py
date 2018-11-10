#!/usr/bin/env python3
# -*- coding: utf-8 -*-+

import rospy
import rospkg

from lib.nodehandle import NodeHandle
from lib.counter import TimeCounter

""" lib """
from enum import Enum

CAMERA_ROW = 640
CAMERA_COL = 480

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
    INIT =  0
    MANUAL = 1
    HOME = 2
    CENTER = 3
    ITEM_CENTER = 4
    SLIDING = 5
    SUCTION = 6
    RELEASE_SUCTION = 7
    FLAW_BOX = 8
    NO_FLAW_BOX = 9
    DECIDE_BOX = 10

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
        strategy function
            INIT
            P2P
    """
    def __init__(self):
        self.nh = NodeHandle()

        self.__state = State.INIT.value
        self.__strategyBusy = -1
        self.__success = False

        self.__itemCounter = 0
        self.__flawConuter = 0
        self.__flaw = False

        self.__checkArrive = 0
    
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
                if(self.P2P_Strategy(self.nh.pHome)):
                    self.__state = State.CENTER.value

            elif(self.__state == State.CENTER.value):
                print('Center')
                if(self.P2P_Strategy(self.nh.pCenter)):
                    self.__state = State.ITEM_CENTER.value
            
            elif(self.__state == State.ITEM_CENTER.value):
                print('Item Center')
                pass
            
            elif(self.__state == State.SLIDING.value):
                print('Sliding')
                pass
            
            #########################################
            elif(self.__state == State.SUCTION.value):
                print('suction')
                pass
            #########################################
            elif(self.__state == State.RELEASE_SUCTION.value):
                print('release suction')
                pass
                    
            elif(self.__state == State.FLAW_BOX.value):
                print('Flaw box')
                if(self.P2P_Strategy(self.nh.pFlaw)):
                    self.__state = State.RELEASE_SUCTION.value

            elif(self.__state == State.NO_FLAW_BOX.value):
                print('NFlaw box')
                if(self.P2P_Strategy(self.nh.pNFlaw)):
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
            if(self.__success):
                self.__strategyBusy = 0
                self.__success = False

        elif(self.__strategyBusy == 0):
            if(self.nh.isBusy == True):
                self.__strategyBusy = 1
            else:
                print("Don't get pos")
        else:
            if(self.nh.isBusy == False):
                self.__strategyBusy = -1
                return True
        return False
    
    def Item_Center_Strategy(self):
        if(self.__checkArrive >= self.nh.checkROI):
            pass
        else:
            self.__checkArrive += 1
        return False
        
    def Manual_Strategy(self):
        pass

    """ fucntion """
    def Pixel_To_mm(self,x_dis,y_dis):
        return x_dis*self.nh.pixelRate,y_dis*self.nh.pixelRate