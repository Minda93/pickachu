#include "nodehandle.hpp"

#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <iostream>

using namespace std;

/*=========================================
 * 
 * 建構
 * 
 ==========================================*/

NodeHandle::NodeHandle()
{
  start = 0;
  again = 0;
  side = -1;

  getChess = 0;

  pushButton = 0;

  player.decide = 0;

  /* publish */
  pubMove = nh.advertise<std_msgs::String>("/accupick3d/cmdString", 1);

  /* subscribe */
  subSave = nh.subscribe("/gomoku/save", 1, &NodeHandle::Sub_Save, this);

  subStart = nh.subscribe("/gomoku/start", 1, &NodeHandle::Sub_Start, this);
  subAgain = nh.subscribe("/gomoku/again", 1, &NodeHandle::Sub_Again, this);
  subSide = nh.subscribe("/gomoku/decide_side", 1, &NodeHandle::Sub_Side, this);
  subPlayer = nh.subscribe("/gomoku/player_point", 1, &NodeHandle::Sub_Player, this);

  subPushButton = nh.subscribe("/accupick3d/push_button", 1, &NodeHandle::Sub_PushButton, this);
  subGetChess = nh.subscribe("/accupick3d/get_chess", 1, &NodeHandle::Sub_GetChess, this);
  subRobotPos = nh.subscribe("/accupick3d/msgString", 1, &NodeHandle::Sub_RobotPos, this);

  /* service */
  // callSuction = n.serviceClient<beginner_tutorials::AddTwoInts>("add_two_ints");
}

NodeHandle::~NodeHandle()
{
}

/*=========================================
 * 
 * ros topic sub
 * 
 ==========================================*/
void NodeHandle::Sub_Save(const std_msgs::Bool msg)
{
}

void NodeHandle::Sub_Start(const std_msgs::Bool msg)
{
  start = msg.data;
}

void NodeHandle::Sub_Again(const std_msgs::Int32 msg)
{
  again = msg.data;
}

void NodeHandle::Sub_Side(const std_msgs::Int32 msg)
{
  side = msg.data;
}

void NodeHandle::Sub_Player(const geometry_msgs::Point msg)
{
  player.point.x = int(msg.x);
  player.point.y = int(msg.y);
  player.decide = 1;
}

void NodeHandle::Sub_PushButton(const std_msgs::Bool msg)
{
  //
}

void NodeHandle::Sub_GetChess(const std_msgs::Bool msg)
{
  getChess = msg.data;
}

void NodeHandle::Sub_RobotPos(const std_msgs::String msg)
{
  string rAction = "";
  string data_ = "";
  stringstream str_;

  for (int i = 0; i < msg.data.size(); i++)
  {
    if (msg.data[i] == ':')
    {
      break;
    }
    else
    {
      rAction += msg.data[i];
    }
  }
  if (rAction == "Pos")
  {
    int j = 0;
    for (int i = 4; i < msg.data.size(); i++)
    {
      if (msg.data[i] == ':')
      {
        str_ << data_;
        switch (j)
        {
        case 0:
          str_ >> Robot.linear.x;
          break;
        case 1:
          str_ >> Robot.linear.y;
          break;
        case 2:
          str_ >> Robot.linear.z;
          break;
        case 3:
          str_ >> Robot.angular.x;
          break;
        case 4:
          str_ >> Robot.angular.y;
          break;
        default:
          break;
        }
        j++;
        data_ = "";
        str_.clear();
      }
      else
      {
        data_ += msg.data[i];
      }
    }
    str_ << data_;
    str_ >> Robot.angular.z;
  }

  // cout<<data_<<endl;
  cout << endl
       << Robot.linear.x
       << endl
       << Robot.linear.y
       << endl
       << Robot.linear.z
       << endl
       << Robot.angular.x
       << endl
       << Robot.angular.y
       << endl
       << Robot.angular.z << endl;
}

/*=========================================
 * 
 * ros topic pub
 * 
 ==========================================*/
void NodeHandle::Pub_GetPos()
{
  std_msgs::String msg;
  msg.data = "GetPos:";
  pubMove.publish(msg);
}

void NodeHandle::Pub_HomePos()
{
  std_msgs::String msg;
  msg.data = "HomePos:";
  pubMove.publish(msg);
}

void NodeHandle::Pub_DataPos(const geometry_msgs::Twist pos)
{
  std_msgs::String msg;
  std::stringstream ss;

  ss << "DataPos:"
     << pos.linear.x
     << ":"
     << pos.linear.y
     << ":"
     << pos.linear.z
     << ":"
     << pos.angular.x
     << ":"
     << pos.angular.y
     << ":"
     << pos.angular.z;

  msg.data = ss.str();
  pubMove.publish(msg);
}

/*=========================================
 * 
 * function
 * 
 ==========================================*/

void NodeHandle::Init_Player()
{
  player.decide = 0;
}

void NodeHandle::Init_Again()
{
  again = 0;
}