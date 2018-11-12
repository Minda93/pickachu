#!/usr/bin/env python3
# -*- coding: utf-8 -*-+

import rospy
import rospkg
import subprocess

# rostopic msg 

from std_msgs.msg import String,Bool

from arm_control.srv import armCmd,armCmdResponse

class Robot(object):
    def __init__(self,cmd=None,pos=[],euler=[]):
        self.__cmd = cmd
        self.__pos = pos
        self.__euler = euler

    @property
    def cmd(self):
        return self.__cmd

    @cmd.setter
    def cmd(self, value):
        self.__cmd = value
    
    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, value):
        self.__pos = value

    @property
    def euler(self):
        return self.__euler

    @euler.setter
    def euler(self, value):
        self.__euler = value
    

class NodeHandle(object):
    r"""
        robot: now robot posture
        tRobot: target robot posture
    """
    def __init__(self):
        self.__robot = Robot()
        self.__tRobot = Robot()

        # self.__robot.pos = []
        # self.__robot.euler = []

        self.__error = [0.01,0.01,0.01,0.01,0.01,0.01]

        """ pub """
        self.pubCmdString  = rospy.Publisher('/accupick3d/cmdString',String, queue_size = 1)
        # self.pubCmd  = rospy.Publisher('/accupick3d/cmd',cmd, queue_size = 1)
        self.pubIsbusy  = rospy.Publisher('/accupick3d/is_busy',Bool, queue_size = 1)
        """ sub """
        rospy.Subscriber("accupick3d/msgString",String,self.Sub_RobotCmd)

        """ service """
        self.serverArm = rospy.Service('/accupick3d/arm_contol', armCmd, self.Arm_Cmd)

        self.Init()

    """ init """
    def Init(self):
        self.Pub_GetPos()
        self.Init_tRobot()
        self.Init_Robot()
        # self.Test_Robot()
    
    def Init_tRobot(self):
        self.__tRobot.cmd = 'none'
        self.__tRobot.pos = []
        self.__tRobot.euler = []

    def Init_Robot(self):
        self.__robot.pos = []
        self.__robot.euler = []

    def Test_Robot(self):
        self.__robot.pos = [0,0,0]
        self.__robot.euler = [0,10,20]

    """ publish """
    def Pub_GetPos(self):
        msg = String()
        msg.data = 'GetPos:'
        self.pubCmdString.publish(msg)
    
    def Pub_HomePos(self):
        msg = String()
        msg.data = 'HomePos:'
        self.pubCmdString.publish(msg)
    
    def Pub_DataPos(self,pos,euler):
        msg = String()
        msg.data = 'DataPos:'

        msg.data = msg.data + str(pos[0]) + ':'
        msg.data = msg.data + str(pos[1]) + ':'
        msg.data = msg.data + str(pos[2]) + ':'
        msg.data = msg.data + str(euler[0]) + ':'
        msg.data = msg.data + str(euler[1]) + ':'
        msg.data = msg.data + str(euler[2])  

        self.pubCmdString.publish(msg)
    
    def Pub_Take_Picture(self):
        # msg = cmd()
        # msg.cmd = 254
        # self.pubCmd.publish(msg)
        pass
    
    def Pub_Get_PICTURE(self):
        # msg = cmd()
        # msg.cmd = 255
        # self.pubCmd.publish(msg)
        pass
    
    def Pub_IsBusy(self,state):
        msg = Bool()
        msg.data = state
        self.pubIsbusy.publish(msg)  

    """ subscribe """
    def Sub_RobotCmd(self,msg):
        data_ = msg.data.split(':')
        
        if(data_[0] == 'Pos'):
            if(len(self.__robot.pos) != 0):
                self.__robot.pos = []
                self.__robot.euler = []
            self.__robot.pos.append(float(data_[1]))
            self.__robot.pos.append(float(data_[2]))
            self.__robot.pos.append(float(data_[3]))

            self.__robot.euler.append(float(data_[4]))
            self.__robot.euler.append(float(data_[5]))
            self.__robot.euler.append(float(data_[6]))
            
            # print(self.__robot.pos,self.__robot.euler)"""  """

    """ service  """
    def Arm_Cmd(self,req):
        if(self.__tRobot.cmd == 'none'):
            self.__tRobot.cmd = req.cmd
            self.__tRobot.pos = req.pos
            self.__tRobot.euler = req.euler
        else:
            print('busy')

        print(self.__tRobot.cmd,self.__tRobot.pos,self.__tRobot.euler)
        return armCmdResponse(True)

    @property
    def robot(self):
        return self.__robot
    
    @property
    def tRobot(self):
        return self.__tRobot
    
    @tRobot.setter
    def tRobot(self, value):
        self.__tRobot = value

    @property
    def error(self):
        return self.__error


