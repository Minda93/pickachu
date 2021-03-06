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
  Init_Param();

  /* publish */
  pubMove = nh.advertise<std_msgs::String>("/accupick3d/cmdString", 1);

  /* subscribe */
  subSave = nh.subscribe("/gomoku/save", 1, &NodeHandle::Sub_Save, this);
  subState = nh.subscribe("/gomoku/behavior_state", 1, &NodeHandle::Sub_State, this);

  subStart = nh.subscribe("/gomoku/start", 1, &NodeHandle::Sub_Start, this);
  subAgain = nh.subscribe("/gomoku/again", 1, &NodeHandle::Sub_Again, this);
  subSide = nh.subscribe("/gomoku/decide_side", 1, &NodeHandle::Sub_Side, this);
  // subPlayer = nh.subscribe("/gomoku/player_point", 1, &NodeHandle::Sub_Player, this);
  subPlayerButton = nh.subscribe("/gomoku/player_pushbutton", 1, &NodeHandle::Sub_Player_PushButton, this);

  subVBoard = nh.subscribe("/gomoku/vBoard", 1, &NodeHandle::Sub_vBoard, this);

  subPushButton = nh.subscribe("/gomoku/push_button", 1, &NodeHandle::Sub_PushButton, this);
  subRobotPos = nh.subscribe("/accupick3d/msgString", 1, &NodeHandle::Sub_RobotPos, this);
  subGripped = nh.subscribe("/right/is_grip", 1, &NodeHandle::Sub_is_grip, this);

  /* service */
  suction_service = nh.serviceClient<vacuum_cmd_msg::VacuumCmd>("/right/suction_cmd", 0);
  // callSuction = n.serviceClient<beginner_tutorials::AddTwoInts>("add_two_ints");
}

NodeHandle::~NodeHandle()
{
}

void NodeHandle::Init_Param()
{
  loadState = false;
  state = 0;

  again = 0;
  side = -1;

  pushButton = 0;

  player.decide = 0;

  is_grip = false;

  vBoard_flag = false;

  for(int i=0; i<81; i++)
    vBoard.push_back(0);
  // cout<<"vBoard[0].size : "<<vBoard.size()<<endl;
  
  // cout<<"vBoard2D[0].size : "<<vBoard2D[0].size()<<endl;
  pickChess_cnt = 0;
  chess_offset = 20;
  // eButton = 3;

  for (int i = 0; i < 6; i++)
  {
    errorPos.push_back(1.0);
  }
  Load_Param();
}

/*=========================================
 * 
 * Load and Save Param
 * 
 ==========================================*/

void NodeHandle::Load_Param()
{
  XmlRpc::XmlRpcValue list1;

  nh.getParam("/accupick3d/gomoku/pHome", list1);
  Set_Point_Value("home", list1["pos"], list1["euler"]);

  nh.getParam("/accupick3d/gomoku/pChess", list1);
  Set_Point_Value("chess", list1["pos"], list1["euler"]);

  nh.getParam("/accupick3d/gomoku/pBoardCenter", list1);
  Set_Point_Value("boardcenter", list1["pos"], list1["euler"]);

  nh.getParam("/accupick3d/gomoku/pButton", list1);
  Set_Point_Value("button", list1["pos"], list1["euler"]);

  nh.getParam("/accupick3d/gomoku/pBoard", list1);
  pBoard.clear();
  for (int i = 0; i < list1.size(); i++)
  {
    Set_Point_Value("board", list1[i]["pos"], list1[i]["euler"]);
  }

  nh.getParam("/accupick3d/gomoku/error_height", eButton);
}
/*=========================================
 * 
 * ros topic sub
 * 
 ==========================================*/
void NodeHandle::Sub_Save(const std_msgs::Bool msg)
{
  cout << "dump" << endl;
  string str = "rosparam dump ";
  str += FILENAME;
  str += STORE_FORM;
  system(str.c_str());
}

void NodeHandle::Sub_State(const std_msgs::Int32 msg)
{
  state = msg.data;
  loadState = true;
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
  // player.decide = 1;
}

void NodeHandle::Sub_vBoard(const std_msgs::Int32MultiArray msg)
{
  // cout<<"fuck "<<msg.data[0]<<endl;
  // if (msg.data.size() != 0) //maybe add protect
    if (vBoard.size() != 0)
    {
      vBoard.clear();
    }
    vBoard_flag = true;
    for (int i = 0; i < msg.data.size(); i++)
    {
      vBoard.push_back(msg.data[i]);
    }
    // cout<<"fuck "<<vBoard_flag<<endl;
}

void NodeHandle::Sub_Player_PushButton(const std_msgs::Bool msg)
{
  player.decide = msg.data;
}

void NodeHandle::Sub_PushButton(const std_msgs::Bool msg)
{
  // if(pushButton == 0)
  pushButton = msg.data;
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
  if (rAction == "GetPos")
  {
    int j = 0;
    for (int i = 7; i < msg.data.size(); i++)
    {
      if (msg.data[i] == ':')
      {
        str_ << data_;
        // cout<<"Data: "<<data_<<endl;
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
  // cout << endl
  //      << Robot.linear.x
  //      << endl
  //      << Robot.linear.y
  //      << endl
  //      << Robot.linear.z
  //      << endl
  //      << Robot.angular.x
  //      << endl
  //      << Robot.angular.y
  //      << endl
  //      << Robot.angular.z << endl;
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

     cout << "DataPos:"
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
     << pos.angular.z<<endl;

  msg.data = ss.str();
  pubMove.publish(msg);
  ros::Duration(0.1).sleep(); 
  pubMove.publish(msg);
  ros::Duration(0.1).sleep(); 
  pubMove.publish(msg);
}

/*=========================================
 * 
 * function
 * 
 ==========================================*/
void NodeHandle::Init_Load_State()
{
  loadState = false;
}

void NodeHandle::Init_Player()
{
  player.decide = 0;
}

void NodeHandle::Init_Again()
{
  again = 0;
}

void NodeHandle::Init_Push_Button()
{
  pushButton = 0;
}

void NodeHandle::Sub_is_grip(const std_msgs::Bool::ConstPtr &msg)
{
  is_grip = msg->data;
}

void NodeHandle::suction_cmd_client(vacuum_cmd_msg::VacuumCmd cmd)
{
  // suctionCmd = cmd;
  std::cout<<"Cmd.request.cmd : "<<cmd.request.cmd<< std::endl;
  if (suction_service.call(cmd))
  {
    std::cout << "suction service success = " << cmd.response.success << std::endl;
  }
  else
    std::cout << "fail to call suction_service." << std::endl;
}
geometry_msgs::Twist NodeHandle::Get_pChess(bool pick, bool armBusy)
{
  geometry_msgs::Twist Chess_pos = pChess;
  if( pick && !armBusy)
    pickChess_cnt = (pickChess_cnt < 3)? pickChess_cnt + 1 : 0;
  switch(pickChess_cnt)
  {
  case 0:
      Chess_pos.linear.x += chess_offset;
      Chess_pos.linear.y += chess_offset;
      break;
  case 1:
      Chess_pos.linear.x -= chess_offset;
      Chess_pos.linear.y += chess_offset;
      break;
  case 2:
      Chess_pos.linear.x -= chess_offset;
      Chess_pos.linear.y -= chess_offset;
      break;
  case 3:
      Chess_pos.linear.x += chess_offset;
      Chess_pos.linear.y -= chess_offset;
      break;
  }
  if(!pick)
    Chess_pos.linear.z += 120;
  return Chess_pos;
}
geometry_msgs::Twist NodeHandle::Get_pBoard_up(int i, int j)
{
  geometry_msgs::Twist board_up = Get_pBoard(i, j);
  board_up.linear.z += 100;
  return board_up;
}
/*=========================================
 * 
 * set param point value
 * 
 ==========================================*/

void NodeHandle::Set_Point_Value(string name, XmlRpc::XmlRpcValue &pos, XmlRpc::XmlRpcValue &euler)
{

  if (name == "home")
  {
    for (int j = 0; j < pos.size(); j++)
    {
      if (pos[j].getType() == XmlRpc::XmlRpcValue::TypeDouble)
      {
        if (j == 0)
          pHome.linear.x = static_cast<double>(pos[0]);
        else if (j == 1)
          pHome.linear.y = static_cast<double>(pos[1]);
        else if (j == 2)
          pHome.linear.z = static_cast<double>(pos[2]);
      }
      else
      {
        if (j == 0)
          pHome.linear.x = static_cast<int>(pos[0]);
        else if (j == 1)
          pHome.linear.y = static_cast<int>(pos[1]);
        else if (j == 2)
          pHome.linear.z = static_cast<int>(pos[2]);
      }
    }
    for (int j = 0; j < euler.size(); j++)
    {
      if (euler[j].getType() == XmlRpc::XmlRpcValue::TypeDouble)
      {
        if (j == 0)
          pHome.angular.x = static_cast<double>(euler[0]);
        else if (j == 1)
          pHome.angular.y = static_cast<double>(euler[1]);
        else if (j == 2)
          pHome.angular.z = static_cast<double>(euler[2]);
      }
      else
      {
        if (j == 0)
          pHome.angular.x = static_cast<int>(euler[0]);
        else if (j == 1)
          pHome.angular.y = static_cast<int>(euler[1]);
        else if (j == 2)
          pHome.angular.z = static_cast<int>(euler[2]);
      }
    }
  }
  else if (name == "chess")
  {
    for (int j = 0; j < pos.size(); j++)
    {
      if (pos[j].getType() == XmlRpc::XmlRpcValue::TypeDouble)
      {
        if (j == 0)
          pChess.linear.x = static_cast<double>(pos[0]);
        else if (j == 1)
          pChess.linear.y = static_cast<double>(pos[1]);
        else if (j == 2)
          pChess.linear.z = static_cast<double>(pos[2]);
      }
      else
      {
        if (j == 0)
          pChess.linear.x = static_cast<int>(pos[0]);
        else if (j == 1)
          pChess.linear.y = static_cast<int>(pos[1]);
        else if (j == 2)
          pChess.linear.z = static_cast<int>(pos[2]);
      }
    }
    for (int j = 0; j < euler.size(); j++)
    {
      if (euler[j].getType() == XmlRpc::XmlRpcValue::TypeDouble)
      {
        if (j == 0)
          pChess.angular.x = static_cast<double>(euler[0]);
        else if (j == 1)
          pChess.angular.y = static_cast<double>(euler[1]);
        else if (j == 2)
          pChess.angular.z = static_cast<double>(euler[2]);
      }
      else
      {
        if (j == 0)
          pChess.angular.x = static_cast<int>(euler[0]);
        else if (j == 1)
          pChess.angular.y = static_cast<int>(euler[1]);
        else if (j == 2)
          pChess.angular.z = static_cast<int>(euler[2]);
      }
    }
  }
  else if (name == "boardcenter")
  {
    for (int j = 0; j < pos.size(); j++)
    {
      if (pos[j].getType() == XmlRpc::XmlRpcValue::TypeDouble)
      {
        if (j == 0)
          pBoardCenter.linear.x = static_cast<double>(pos[0]);
        else if (j == 1)
          pBoardCenter.linear.y = static_cast<double>(pos[1]);
        else if (j == 2)
          pBoardCenter.linear.z = static_cast<double>(pos[2]);
      }
      else
      {
        if (j == 0)
          pBoardCenter.linear.x = static_cast<int>(pos[0]);
        else if (j == 1)
          pBoardCenter.linear.y = static_cast<int>(pos[1]);
        else if (j == 2)
          pBoardCenter.linear.z = static_cast<int>(pos[2]);
      }
    }
    for (int j = 0; j < euler.size(); j++)
    {
      if (euler[j].getType() == XmlRpc::XmlRpcValue::TypeDouble)
      {
        if (j == 0)
          pBoardCenter.angular.x = static_cast<double>(euler[0]);
        else if (j == 1)
          pBoardCenter.angular.y = static_cast<double>(euler[1]);
        else if (j == 2)
          pBoardCenter.angular.z = static_cast<double>(euler[2]);
      }
      else
      {
        if (j == 0)
          pBoardCenter.angular.x = static_cast<int>(euler[0]);
        else if (j == 1)
          pBoardCenter.angular.y = static_cast<int>(euler[1]);
        else if (j == 2)
          pBoardCenter.angular.z = static_cast<int>(euler[2]);
      }
    }
  }
  else if (name == "button")
  {
    for (int j = 0; j < pos.size(); j++)
    {
      if (pos[j].getType() == XmlRpc::XmlRpcValue::TypeDouble)
      {
        if (j == 0)
          pButton.linear.x = static_cast<double>(pos[0]);
        else if (j == 1)
          pButton.linear.y = static_cast<double>(pos[1]);
        else if (j == 2)
          pButton.linear.z = static_cast<double>(pos[2]);
      }
      else
      {
        if (j == 0)
          pButton.linear.x = static_cast<int>(pos[0]);
        else if (j == 1)
          pButton.linear.y = static_cast<int>(pos[1]);
        else if (j == 2)
          pButton.linear.z = static_cast<int>(pos[2]);
      }
    }
    for (int j = 0; j < euler.size(); j++)
    {
      if (euler[j].getType() == XmlRpc::XmlRpcValue::TypeDouble)
      {
        if (j == 0)
          pButton.angular.x = static_cast<double>(euler[0]);
        else if (j == 1)
          pButton.angular.y = static_cast<double>(euler[1]);
        else if (j == 2)
          pButton.angular.z = static_cast<double>(euler[2]);
      }
      else
      {
        if (j == 0)
          pButton.angular.x = static_cast<int>(euler[0]);
        else if (j == 1)
          pButton.angular.y = static_cast<int>(euler[1]);
        else if (j == 2)
          pButton.angular.z = static_cast<int>(euler[2]);
      }
    }
  }
  else if (name == "board")
  {
    geometry_msgs::Twist pos_;
    for (int j = 0; j < pos.size(); j++)
    {
      if (pos[j].getType() == XmlRpc::XmlRpcValue::TypeDouble)
      {
        if (j == 0)
          pos_.linear.x = static_cast<double>(pos[0]);
        else if (j == 1)
          pos_.linear.y = static_cast<double>(pos[1]);
        else if (j == 2)
          pos_.linear.z = static_cast<double>(pos[2]);
      }
      else
      {
        if (j == 0)
          pos_.linear.x = static_cast<int>(pos[0]);
        else if (j == 1)
          pos_.linear.y = static_cast<int>(pos[1]);
        else if (j == 2)
          pos_.linear.z = static_cast<int>(pos[2]);
      }
    }
    for (int j = 0; j < euler.size(); j++)
    {
      if (euler[j].getType() == XmlRpc::XmlRpcValue::TypeDouble)
      {
        if (j == 0)
          pos_.angular.x = static_cast<double>(euler[0]);
        else if (j == 1)
          pos_.angular.y = static_cast<double>(euler[1]);
        else if (j == 2)
          pos_.angular.z = static_cast<double>(euler[2]);
      }
      else
      {
        if (j == 0)
          pos_.angular.x = static_cast<int>(euler[0]);
        else if (j == 1)
          pos_.angular.y = static_cast<int>(euler[1]);
        else if (j == 2)
          pos_.angular.z = static_cast<int>(euler[2]);
      }
    }
    pBoard.push_back(pos_);
  }
}
