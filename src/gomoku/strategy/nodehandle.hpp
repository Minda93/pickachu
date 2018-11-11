#include "ros/ros.h"
#include <ros/package.h>
#include <std_msgs/Bool.h>
#include <std_msgs/Int32.h>
#include <std_msgs/String.h>
#include <std_msgs/Int32MultiArray.h>
#include <geometry_msgs/Point.h>
#include <geometry_msgs/Twist.h>

#include "vacuum_cmd_msg/VacuumCmd.h"

#include <vector>

#define FILENAME ros::package::getPath("gomoku") + "/config/gomoku.yaml"
#define STORE_FORM " /accupick3d/gomoku"

#define ROW 9
#define COL 9

#define ERROR_DECIMAL 3

typedef struct Point
{
  int x;
  int y;
} Point;

typedef struct Player
{
  Point point;
  bool decide;
} Player;

class NodeHandle
{
public:
  NodeHandle();
  ~NodeHandle();

  void Init_Param();

  void Load_Param();
  void Set_Point_Value(std::string name, XmlRpc::XmlRpcValue &pos, XmlRpc::XmlRpcValue &euler);

  void Init_Load_State();
  void Init_Player();
  void Init_Push_Button();
  void Init_Again();

  inline bool Get_Load_State() const { return loadState; };
  inline int Get_State() const { return state; };

  inline Player Get_Player() const { return player; };
  inline geometry_msgs::Twist Get_Robot() const { return Robot; };

  inline int Get_Side() const { return side; };
  inline bool IS_Start() const { return start; };
  inline int IS_Again() const { return again; };

  inline bool IS_PlayDecide() const { return player.decide; };
  inline bool IS_PushButton() const { return pushButton; };

  inline bool Is_grip() const { return is_grip; };

  inline geometry_msgs::Twist Get_pHome() const { return pHome; };
  // inline geometry_msgs::Twist Get_pChess() const { return pChess; };
  inline geometry_msgs::Twist Get_pBoardCenter() const { return pBoardCenter; };
  inline geometry_msgs::Twist Get_pButton() const { return pButton; };
  geometry_msgs::Twist Get_pBoard(int i, int j) const { return pBoard[i * COL + j]; };
  geometry_msgs::Twist Get_pBoard_up(int i, int j);
  geometry_msgs::Twist Get_pChess(bool pick, bool armBusy);
  // inline double Get_ErrorPos(int i) const { return errorPos[i]; };
  inline double Get_eButton() const { return eButton; };
  inline int Get_vBoard(int i, int j) { return vBoard[i * COL + j]; };
  inline int Check_vBorad_Size() { return vBoard.size();};
  inline double Get_chess_offset() const { return chess_offset; };
  
  void Pub_GetPos();
  void Pub_HomePos();
  void Pub_DataPos(const geometry_msgs::Twist pos);
  void suction_cmd_client(std::string cmd);

  static std::vector<double> errorPos;

private:
  /* subscribe */
  void Sub_Save(const std_msgs::Bool msg);
  void Sub_State(const std_msgs::Int32 msg);

  void Sub_vBoard(const std_msgs::Int32MultiArray msg);

  void Sub_Player(const geometry_msgs::Point msg);
  void Sub_Player_PushButton(const std_msgs::Bool msg);
  void Sub_Start(const std_msgs::Bool msg);
  void Sub_Again(const std_msgs::Int32 msg);
  void Sub_Side(const std_msgs::Int32 msg);

  void Sub_PushButton(const std_msgs::Bool msg);
  void Sub_RobotPos(const std_msgs::String msg);

  void Sub_is_grip(const std_msgs::Bool::ConstPtr &msg);

private:
  ros::NodeHandle nh;

  /* publish */
  ros::Publisher pubMove; // DataPos, GetPos, HomePos

  /* subscribe */
  ros::Subscriber subSave;
  ros::Subscriber subState;

  ros::Subscriber subStart;
  ros::Subscriber subAgain;
  ros::Subscriber subSide;

  ros::Subscriber subVBoard;

  ros::Subscriber subPlayer;
  ros::Subscriber subPlayerButton;

  ros::Subscriber subPushButton;
  ros::Subscriber subRobotPos;

  ros::Subscriber subGripped;
  ros::ServiceClient suction_service;

  int state;
  bool loadState;

  bool start;
  int again;
  int side;

  int pickChess_cnt;
  double chess_offset;

  bool is_grip;

  bool pushButton;

  std::vector<int> vBoard;
  Player player;
  geometry_msgs::Twist Robot;

  vacuum_cmd_msg::VacuumCmd suctionCmd;

  // Target pos param
  geometry_msgs::Twist pHome;
  geometry_msgs::Twist pChess;
  geometry_msgs::Twist pBoardCenter;
  std::vector<geometry_msgs::Twist> pBoard;
  geometry_msgs::Twist pButton;
  double eButton; //push button error height
};