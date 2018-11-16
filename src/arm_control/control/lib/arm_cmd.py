#!/usr/bin/env python3
# -*- coding: utf-8 -*-+

import rospy
import rospkg

from lib.nodehandle import NodeHandle,Robot

""" lib """
from enum import Enum
import math
import copy

ERROR_POS = 1

class Cmd(Enum):
    NONE = 'none'
    P2P = 'p2p'
    MOVE = 'move'  # not use
    MOVE_POS = 'mPos'
    MOVE_EULER = 'mEuler' # not use
    HOME = 'home' # not use
    TAKE_PICTURE = 'takePicture' # not use
    GET_PICTURE = 'getPicture' # not use

    
class ArmCmd(object):
    r"""
        cmd
            p2p
            takePicture
            getPicture
            home: pickathon define home
            none  
    """
    def __init__(self):
        self.nh = NodeHandle()
        self.__isBusy = False

        self.__counterTh = 150
        self.__counter = 0
        self.__tmpPos = Robot()
    
    def Run(self):
        if(self.nh.tRobot.cmd == Cmd.P2P.value):
            # print('p2p')
            self.P2P_Cmd()
        elif(self.nh.tRobot.cmd == Cmd.MOVE.value):
            print('move')
            self.Move_Cmd()
        elif(self.nh.tRobot.cmd == Cmd.MOVE_POS.value):
            print('move pos')
            self.Move_Pose_Cmd()
        elif(self.nh.tRobot.cmd == Cmd.MOVE_EULER.value):
            print('move euler')
            self.Move_Euler_Cmd()
        elif(self.nh.tRobot.cmd == Cmd.TAKE_PICTURE.value):
            print('take picture')
            self.Take_Picture_Cmd()
        elif(self.nh.tRobot.cmd == Cmd.GET_PICTURE.value):
            print('get picture')
            self.Get_Picture_Cmd()
        elif(self.nh.tRobot.cmd == Cmd.HOME.value):
            print('home')
            # self.Home_Cmd()
        else:
            # print('none')
            pass
        
    """ cmd """
    def P2P_Cmd(self):
        self.nh.Pub_GetPos()
        # print(self.nh.robot.pos)
        if(self.nh.robot.pos != []):
            if(self.Is_Same_Pos(self.nh.robot,self.nh.tRobot,ERROR_POS)):
                print('success')
                self.__isBusy = False
                self.nh.Init_tRobot()
                self.nh.Init_Robot()
            else:
                if(self.__isBusy == False):
                    self.nh.Pub_DataPos(self.nh.tRobot.pos,self.nh.tRobot.euler)
                    self.nh.Pub_DataPos(self.nh.tRobot.pos,self.nh.tRobot.euler)
                    self.nh.Pub_DataPos(self.nh.tRobot.pos,self.nh.tRobot.euler)
                    self.__isBusy = True
                # print('p2p: not this point')
        else:
            # print("fuck Get Pos")
            pass

        self.nh.Pub_IsBusy(self.__isBusy)
        
    def Move_Cmd(self):
        pass

    def Move_Pose_Cmd(self):
        self.nh.Pub_GetPos()
        if(self.nh.robot.pos != []):
            if(self.__isBusy == False):
                self.__isBusy = True
                pos = []
                for i in range(3):
                    pos.append(self.nh.robot.pos[i] + self.nh.tRobot.pos[i])

                self.nh.tRobot.pos = pos
                self.nh.Pub_DataPos(self.nh.tRobot.pos,self.nh.robot.euler)
            else:
                if(self.Is_Same_Pos(self.nh.robot,self.nh.tRobot,ERROR_POS)):
                    print('success')
                    self.__isBusy = False
                    self.nh.Init_tRobot()
                    self.nh.Init_Robot()
        else:
            print("fuck Get Pos")

        # rospy.Timer(rospy.Duration(3.0), self.nh.Init_Robot)    
        self.nh.Pub_IsBusy(self.__isBusy)

    def Move_Euler_Cmd(self):
        pass
                
    def Take_Picture_Cmd(self):
        self.nh.Pub_Take_Picture()
        self.nh.Init_tRobot()

    def Get_Picture_Cmd(self):
        self.nh.Pub_Get_PICTURE()
        self.nh.Init_tRobot()
    
    def Home_Cmd(self):
        self.nh.Init_tRobot()

    """ function """
    def Is_Same_Pos(self,robot,target,state = 0):
        r"""
            input 
                robot  -> class Robot
                target -> class Robot
                state
                    0: round
                    1: error
        """
        print('same pose counter: ' ,self.__counter)
        if(len(self.__tmpPos.pos) == 0):
            # if(robot.pos != []):
            self.__tmpPos = copy.deepcopy(robot)
        else:
            flag = 0
            for i in range(6):
                if(i < 3):
                    if(round(abs(robot.pos[i]-self.__tmpPos.pos[i]),5) < self.nh.error[i]):
                        flag = 1
                    else:
                        flag = 0
                else:
                    if(round(abs(robot.euler[i-3]-self.__tmpPos.euler[i-3]),5) < self.nh.error[i]):
                        flag = 1
                    else:
                        flag = 0
            if(flag == 1):
                self.__counter += 1
                self.__tmpPos = copy.deepcopy(robot)
            else:
                self.__counter  = 0

        if(self.__counter > self.__counterTh):
            self.nh.Pub_DataPos(target.pos,target.euler)
            # self.nh.Pub_DataPos(target.pos,target.euler)
            # self.nh.Pub_DataPos(target.pos,target.euler)
            self.__counter  = 0
            return False

        if(state == 0):
            for i in range(3):
                if(round(robot.pos[i],2) != round(target.pos[i],2)):
                    return False
            for i in range(3):
                if(round(robot.euler[i],2) != round(target.euler[i],2)):
                    return False
            return True
        elif(state == 1):
            for i in range(6):
                if(i < 3):
                    # print("fuck",i)
                    if(round(abs(robot.pos[i]-target.pos[i]),5) > self.nh.error[i]):
                        return False
                else:
                    # print("fuck2",i)
                    if(round(abs(robot.euler[i-3]-target.euler[i-3]),5) > self.nh.error[i]):
                        return False
            return True
    def Pub_Busy(self):
        pass
