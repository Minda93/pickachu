#include "tdataunit/tdataunit.hpp"

// TdataUnit* DataUnit = new TdataUnit();
TdataUnit::TdataUnit()
{
    CameraParameterValue = new CameraParameter;
    CameraParameterValue->autoexposure = 0;
    CameraParameterValue->auto_white_balance = 0;
    CameraParameterValue->brightness = 0;
    CameraParameterValue->contrast = 0;
    CameraParameterValue->saturation = 0;
    CameraParameterValue->white_balance = 0;
    CameraParameterValue->ParameterName = "[Camera Set Parameter]";   
}

TdataUnit::~TdataUnit()
{
    delete CameraParameterValue;
}

void TdataUnit::SaveCameraSetFiile()
{
    char path[200];
    printf("%s",path);
    strcpy(path, PATH.c_str());
    strcat(path, "/cam_param/CameraSet.ini");
    try
    {
//        ofstream OutFile(sFileName.c_str());
        ofstream OutFile(path);
        OutFile << CameraParameterValue->ParameterName;
        OutFile << "\n";
        OutFile << "autoexposure = ";
        OutFile << CameraParameterValue->autoexposure;
        OutFile << "\n";
        OutFile << "auto_white_balance = ";
        OutFile << CameraParameterValue->auto_white_balance;
        OutFile << "\n";
        OutFile << "brightness = ";
        OutFile << CameraParameterValue->brightness;
        OutFile << "\n";
        OutFile << "contrast = ";
        OutFile << CameraParameterValue->contrast;
        OutFile << "\n";
        OutFile << "saturation = ";
        OutFile << CameraParameterValue->saturation;
        OutFile << "\n";
        OutFile << "white_balance = ";
        OutFile << CameraParameterValue->white_balance;
        OutFile << "\n";

        OutFile.close();
    }
    catch( exception e )
    {
    }
}

void TdataUnit::LoadCameraSetFiile()
{

    fstream fin;
    char line[100]; 
    char path[200];
    strcpy(path, PATH.c_str());
    strcat(path, "/cam_param/CameraSet.ini");

    fin.open(path, ios::in);
    //fin.open(("../../Parameter/Color_Model_Data/ColorModelData.ini"), ios::in);
    try
    {
        fin.getline(line,sizeof(line),'\n');
        CameraParameterValue->autoexposure = readvalue(fin, "autoexposure", 0);
        CameraParameterValue->auto_white_balance = readvalue(fin, "auto_white_balance", 0);
        CameraParameterValue->brightness = readvalue(fin, "brightness", 0);
        CameraParameterValue->contrast = readvalue(fin, "contrast", 0);
        CameraParameterValue->saturation = readvalue(fin, "saturation", 0);
        CameraParameterValue->white_balance = readvalue(fin, "white_balance", 0);
        fin.close();
    }
    catch(exception e)
    {
    }
}

float TdataUnit::readvalue(fstream &fin, string title, bool mode)
{
    char line[100];
    char equal;
    while(1)
    {
        fin.getline(line,sizeof(line),' ');
        if((string)line == title)
        {
            fin.get(equal);
            if(equal == '=')
            {
                fin.getline(line,sizeof(line),'\n');
                break;
            }
        }
    }
    return (mode == false)?atoi(line):atof(line);

}

