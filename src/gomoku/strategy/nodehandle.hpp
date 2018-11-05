#include "ros/ros.h"
#include <std_msgs/Bool.h>
#include <std_msgs/Int32.h>
#include <std_msgs/String.h>
#include <geometry_msgs/Point.h>
#include <geometry_msgs/Twist.h>

#include "vacuum_cmd_msg/VacuumCmd.h"

#include <vector>

#define FILENAME ""

#define ROW 10
#define COL 10

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

    void Init_Player();
    void Init_Again();

    inline Player Get_Player() const { return player; };
    inline geometry_msgs::Twist Get_Robot() const { return Robot; };

    inline int Get_Side() const { return side; };
    inline bool IS_Start() const { return start; };
    inline int IS_Again() const { return again; };

    inline bool IS_GetChess() const { return getChess; };
    inline bool IS_PushButton() const { return pushButton; };

    inline bool Is_grip() const { return is_grip; };

    inline geometry_msgs::Twist Get_pHome() const { return pHome; };
    inline geometry_msgs::Twist Get_pChess() const { return pChess; };
    inline geometry_msgs::Twist Get_pBoardCenter() const { return pBoardCenter; };
    inline geometry_msgs::Twist Get_pButton() const { return pButton; };
    geometry_msgs::Twist Get_pBoard(int i,int j) const { return pBoard[i*COL+j]; };

    void Pub_GetPos();
    void Pub_HomePos();
    void Pub_DataPos(const geometry_msgs::Twist pos);
    void suction_cmd_client(std::string cmd);

    /* service */
    /* will build service */
    ros::ServiceClient callSuction; //string cmd, bool sucess

  private:
    /* subscribe */
    void Sub_Save(const std_msgs::Bool msg);

    void Sub_Player(const geometry_msgs::Point msg);
    void Sub_Start(const std_msgs::Bool msg);
    void Sub_Again(const std_msgs::Int32 msg);
    void Sub_Side(const std_msgs::Int32 msg);

    void Sub_PushButton(const std_msgs::Bool msg);
    void Sub_GetChess(const std_msgs::Bool msg);
    void Sub_RobotPos(const std_msgs::String msg);

    void Sub_is_grip(const std_msgs::Bool::ConstPtr& msg);
    

  private:
    ros::NodeHandle nh;

    /* publish */
    ros::Publisher pubMove; // DataPos, GetPos, HomePos

    /* subscribe */
    ros::Subscriber subSave;

    ros::Subscriber subStart;
    ros::Subscriber subAgain;
    ros::Subscriber subSide;
    ros::Subscriber subPlayer;
    // ros::Subscriber subPlayerButton;

    ros::Subscriber subPushButton; 
    ros::Subscriber subGetChess; // 是否吃到棋子 maybe delete
    ros::Subscriber subRobotPos;

    ros::Subscriber subGripped;
    ros::ServiceClient suction_service;

    bool start;
    int again;
    int side;

    bool is_grip;

    bool getChess;  

    bool pushButton; // same player.decide maybe delete

    Player player;
    geometry_msgs::Twist Robot;

    vacuum_cmd_msg::VacuumCmd suctionCmd;

    // Target pos
    geometry_msgs::Twist pHome;
    geometry_msgs::Twist pChess;
    geometry_msgs::Twist pBoardCenter;
    std::vector <geometry_msgs::Twist> pBoard;
    geometry_msgs::Twist pButton;
};