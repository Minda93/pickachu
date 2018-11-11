#ifndef TDATAUNIT_H
#define TDATAUNIT_H
#include <fstream>
#include <string>
#include <stdlib.h>
#include <string.h>
#include <ros/package.h>
using namespace std;

string PATH = ros::package::getPath("usb_cam");

struct CameraParameter
{
    int  autoexposure;
    int  auto_white_balance;
    int  brightness;
    int  contrast;
    int  saturation;
    int  white_balance;
    string ParameterName;
};


class TdataUnit
{
public:
    TdataUnit();
    ~TdataUnit();
    void SaveCameraSetFiile();
    void LoadCameraSetFiile();
    float readvalue(fstream &fin, string title,bool mode);


    CameraParameter* CameraParameterValue;
};
extern TdataUnit* DataUnit;

#endif // TDATAUNIT_H
