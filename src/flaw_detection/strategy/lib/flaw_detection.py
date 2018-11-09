#!/usr/bin/env python3
# -*- coding: utf-8 -*-+

import rospy
import rospkg

from lib.nodehandle import NodeHandle

""" lib """
from enum import Enum

class State(Enum):
    INIT =  0
    MANUAL = 1
    HOME = 2
    CENTER = 3
    ITEM_CENTER = 4
    FLAW_CENTER = 5
    SLIDING = 6
    SUCKTION = 7
    FLAW_BOX = 8
    NO_FLAW_BOX = 9

class Strategy(object):
    def __init__(self):
        self.nh = NodeHandle()

        self.__state = State.INIT.value
        self.__strategyBusy = -1
        self.__success = False
    
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
                if(self.Home_Strategy()):
                    self.__state = -1
            elif(self.__state == State.CENTER.value):
                print('Center')

            elif(self.__state == State.MANUAL.value):
                print('Manual')

            else:
                print('None')
    
    def Init_Strategy(self):
        return True
    
    def Home_Strategy(self):
        if(self.__strategyBusy == -1):
            self.__success = self.nh.Arm_Contorl('p2p',self.nh.pHome)
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
                self.__strategyBusy = 0
                return True
        return False
        
    def Manual_Strategy(self):
        pass