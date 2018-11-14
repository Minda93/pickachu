#include "nodehandle.hpp"

#define TIME 3

enum ACTION
{
    INIT,
    CHOOSE_SIDE,
    PLAYER,
    PC,
    PLAY_CHESS,
    PUSH_BUTTON,
    END,
    STOP
};

enum SIDE 
{
    SIDE_PLAYER = 1,
    SIDE_PC
};

/* 
  first black 
*/
enum COLOR 
{ 
    WHITE = -1,
    NOCOLOR = 0,
    BLACK = 1
};

class Strategy
{
  /* friend OPERATORS */
    friend bool operator==(const geometry_msgs::Twist pos1,const geometry_msgs::Twist pos2);
  public:
    Strategy();
    ~Strategy();
    

    void Process();

    void Init_Param();
    void Init_Gomoku();
    void Show_Gomoku();
    int Line_Check(SIDE s);

    void Choose_First();
    void Cin_First(bool s = 1);
    void Who_First();
    
    int Player_1(bool s = 1);
    int Weights(int s, int x, int y);
    int PC_Strategy(SIDE s);

    bool Check_Decide();
    bool Check_Push_Buttion();

    void Show_Player();

    /* tool */
    void Transform_Board();
    void Delay(double time);

  private:
    NodeHandle nh;

  private:
    // bool gameStart;
    // int step;
    int first;
    bool isBusy;

    bool isChess;
    int pcColor;
    int playerColor;

    int pcState; //robot decide state 
    int buttonState;  //push button state

    // int firstState;
    ACTION state;
    
    Point chess;  //pc decide chess x:row y:col
    int gomoku[ROW][COL];

};