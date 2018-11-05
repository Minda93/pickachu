// #include "ros/ros.h"
#include "strategy.hpp"
// #include "nodehandle.hpp"


#include <stdio.h>
#include <stdlib.h>
#include <iostream>

using namespace std;

int main(int argc,char **argv){
    ros::init(argc, argv, "gomoku_strategy");
    
    Strategy strategy;

    ros::Rate loop_rate(30);

    while(ros::ok()){

        strategy.Process();

        ros::spinOnce();
        loop_rate.sleep();
    }
    return 0;
}

