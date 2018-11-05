#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>
#include "ros/ros.h"
#include <std_msgs/Bool.h>
#include <std_msgs/Int32.h>
#include <std_msgs/String.h>

#include "vacuum_cmd_msg/VacuumCmd.h"


class SuctionTask
{
private:
    string name;
    int fail_cnt;
    bool gripped;
    
    ros::Subscriber is_grip_sub;
    ros::ServiceClient suction_service;

public:
    SuctionTask();
    ~SuctionTask();

    void robot_cmd_client(string cmd);
    void gripper_vaccum_on();
    void gripper_vaccum_off();
    void gripper_calibration();
    void gripper_set_max();
    void gripper_set_min();
    void gripper_suction_up();
    void gripper_suction_down();
    void gripper_suction_deg();
    void is_grip_callback();
    bool is_grip();

}