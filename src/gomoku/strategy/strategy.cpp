#include "strategy.hpp"

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <iostream>
#include <time.h>

using namespace std;

std::vector<double> NodeHandle::errorPos;
/*=========================================
 * 
 * friend OPERATORS
 * 
 ==========================================*/

double Round(double value, int num)
{
    double rate = 10;
    rate = pow(rate, num);
    return (roundf(value * rate) / rate);
}

bool operator==(const geometry_msgs::Twist pos1, const geometry_msgs::Twist pos2)
{
    // if (pos1.linear.x != pos2.linear.x)
    //     return false;
    // if (pos1.linear.y != pos2.linear.y)
    //     return false;
    // if (pos1.linear.z != pos2.linear.z)
    //     return false;
    // if (pos1.angular.x != pos2.angular.x)
    //     return false;
    // if (pos1.angular.y != pos2.angular.y)
    //     return false;
    // if (pos1.angular.z != pos2.angular.z)
    //     return false;

    if (Round(abs(pos1.linear.x - pos2.linear.x), ERROR_DECIMAL) > NodeHandle::errorPos[0])
        return false;
    if (Round(abs(pos1.linear.y - pos2.linear.y), ERROR_DECIMAL) > NodeHandle::errorPos[1])
        return false;
    if (Round(abs(pos1.linear.z - pos2.linear.z), ERROR_DECIMAL) > NodeHandle::errorPos[2])
        return false;
    if (Round(abs(pos1.angular.x - pos2.angular.x), ERROR_DECIMAL) > NodeHandle::errorPos[3])
        return false;
    if (Round(abs(pos1.angular.y - pos2.angular.y), ERROR_DECIMAL) > NodeHandle::errorPos[4])
        return false;
    if (Round(abs(pos1.angular.z - pos2.angular.z), ERROR_DECIMAL) > NodeHandle::errorPos[5])
        return false;

    return true;
}

/*=========================================
 * 
 * 建構
 * 
 ==========================================*/
Strategy::Strategy()
{
    Init_Param();
}

Strategy::~Strategy()
{
}

void Strategy::Init_Param()
{
    state = INIT;
    first = -1;
    pcState = 0;
    buttonState = 0;
    isBusy = false;
}

/*=========================================
 * 
 * process
 * 
 ==========================================*/

void Strategy::Process()
{
    if (nh.IS_Start())
    {
        if (nh.Get_Load_State() == true)
        {
            if (nh.Get_State() == 0)
            {
                state = INIT;
            }
            nh.Init_Load_State();
        }
        if (state == INIT)
        {
            Init_Param();
            Init_Gomoku();
            Show_Gomoku();
            Choose_First();
            state = CHOOSE_SIDE;
        }
        else if (state == CHOOSE_SIDE)
        {
            if (first == 0)
            {
                // PC_Strategy(SIDE_PC);
                // state = PLAYER;
                if (pcState == 0)
                {
                    PC_Strategy(SIDE_PC);
                    pcState = 1;
                }
                else if (Check_Decide())
                {
                    state = PUSH_BUTTON;
                    pcState = 0;
                }
            }
            else if (first == 1)
            {
                if (Player_1() != -1)
                {
                    state = PC;
                    Show_Gomoku();
                }
            }
            else
            {
                Cin_First(1);
                Who_First();
            }
        }
        else if (state == PLAYER)
        {
            if (first == -1)
            {
                state = END;
            }
            else
            {
                if (Player_1() != -1)
                {
                    state = PC;
                    Show_Gomoku();
                }
            }
        }
        else if (state == PC)
        {
            if (first == -1)
            {
                state = END;
            }
            else
            {
                if (pcState == 0)
                {
                    PC_Strategy(SIDE_PC);
                    pcState = 1;
                }
                else if (Check_Decide())
                {
                    printf("decide success: %d", pcState);
                    state = PUSH_BUTTON;
                    pcState = 0;
                }
                // PC_Strategy(SIDE_PC);
                // state = PLAYER;
            }
        }
        else if (state == PUSH_BUTTON)
        {
            if (Check_Push_Buttion())
            {
                printf("push button success: %d", buttonState);
                state = PLAYER;
            }
            else
            {
                printf("buttonState: %d", buttonState);
            }
        }
        else if (state == END)
        {
            if (nh.IS_Again() == 1)
            {
                nh.Init_Again();
                state = INIT;
                nh.Init_Param();
            }
            else if (nh.IS_Again() == -1)
            {
                printf("exit\n");
                exit(1);
            }
            else
            {
                Show_Gomoku();
                Line_Check(SIDE_PC);
                Line_Check(SIDE_PLAYER);
            }
        }
        else
        {
            ;
        }
    }
}

/*=========================================
 * 
 * gomoku
 * 
 ==========================================*/
void Strategy::Init_Gomoku()
{
    for (int i = 0; i < ROW; i++)
    {
        for (int j = 0; j < COL; j++)
        {
            gomoku[i][j] = NOCOLOR;
        }
    }
}

/* -----------------------------------------*/

void Strategy::Show_Gomoku()
{
    system("clear");
    cout << "  ";
    for (int j = 0; j < COL; j++)
    {
        cout << j << " ";
    }
    cout << "\n";

    for (int i = 0; i < ROW; i++)
    {
        cout << i << " ";
        for (int j = 0; j < COL; j++)
        {
            if (gomoku[i][j] == 1)
            {
                printf("X ");
            }
            else if (gomoku[i][j] == 2)
            {
                printf("O ");
            }
            else
            {
                printf("+ ");
            }
            //cout<<gomoku[i][j]<<" ";
        }
        cout << "\n";
    }
}
/* -----------------------------------------*/
int Strategy::Line_Check(SIDE s)
{
    /*	int i,j,k;*/
    int snc[6] = {0, 1, 10, 50, 1000, 10000}; //1 2 20 50
    int n, ns, nn, t;
    n = 0;
    for (int x = 0; x < ROW; x++)
    {
        for (int y = 0; y < COL; y++)
        {
            for (int j = 1; j <= 8; j++)
            {

                ns = nn = 1;
                for (int i = 0; i < 5; i++) //米
                {
                    if (((x + i) / ROW) <= 1)
                    {
                        if (j == 1)
                            t = gomoku[x][y - i]; //上
                        if (j == 2)
                            t = gomoku[x + i][y - i]; //右上
                        if (j == 3)
                            t = gomoku[x + i][y]; //右
                        if (j == 4)
                            t = gomoku[x + i][y + i]; //右下
                        if (j == 5)
                            t = gomoku[x][y + i]; //下
                        if (j == 6)
                            t = gomoku[x - i][y + i]; //左下
                        if (j == 7)
                            t = gomoku[x - i][y]; //左
                        if (j == 8)
                            t = gomoku[x - i][y - i]; //左上

                        if (t == s)
                            nn++;
                        else if (t != 0)
                            ns = 0;

                        if (nn > 5 && gomoku[x][y] == s)
                        {
                            Show_Gomoku();
                            if (s == 1)
                                printf("玩 家 獲勝!!\n");
                            if (s == 2)
                                printf("電 腦 獲勝!!\n");
                            first = -1;
                            n = -1;
                            return n;
                        }

                        if (ns)
                            n += snc[nn];
                    }
                }
            }
        }
    }
}

/*=========================================
 * 
 * strategy
 * 
 ==========================================*/

void Strategy::Choose_First()
{
    cout << "who go first" << endl;
    cout << "0 = computer" << endl;
    cout << "1 = human" << endl
         << endl;
}

/* -----------------------------------------*/

void Strategy::Cin_First(bool s)
{
    // printf("%d\n", first);
    if (s == 0)
    {
        cin >> first;
    }
    else
    {   
        //pc first
        if (nh.IS_PlayDecide())
        { 
            first = 0;
            pcColor = BLACK;
            playerColor = WHITE;
            nh.Init_Player();
            Delay(TIME);
        }// player first
        else if (nh.IS_PushButton())
        { 
            first = 1;
            pcColor = WHITE;
            playerColor = BLACK;
            nh.Init_Push_Button();
        }
        // first = nh.Get_Side();
        // printf("%d\n",first);
    }
}
/* -----------------------------------------*/

void Strategy::Who_First()
{
    if (first == 0)
    {
        cout << "computer first" << endl;
    }
    else if (first == 1)
    {
        cout << "human first" << endl;
    }
}

/* -----------------------------------------*/

int Strategy::Player_1(bool s) //玩家1
{
    if (s == 0)
    {
        cout << "輸入座標 x,y " << endl;
        int a, b;
        cin >> a;
        if (cin.get() == ',') //數字+逗號
        {
            cin >> b;
        }
        gomoku[a][b] = 1;
        Line_Check(SIDE_PLAYER);
        return gomoku[a][b];
    }
    else
    {   
        /* case 1 */
        // Player player = nh.Get_Player();
        // if (player.decide == 1)
        // {
        //     // if (gomoku[player.point.x][player.point.y])
        //     // {
        //     //     return -1;
        //     // }
        //     gomoku[player.point.x][player.point.y] = 1;
        //     Line_Check(SIDE_PLAYER);
        //     nh.Init_Player();
        //     return gomoku[player.point.x][player.point.y];
        // }
        // else
        // {
        //     return -1;
        // }

        /* case 2 */
        if(nh.IS_PlayDecide()){
            Delay(TIME);
            Transform_Board();
            Line_Check(SIDE_PLAYER);
            nh.Init_Player();
            return SIDE_PLAYER;
        }else{
            return -1;
        }
    }
}
/* -----------------------------------------*/
int Strategy::Weights(int s, int x, int y)
{
    int i, j, l;
    int snc[6] = {0, 1, 10, 50, 1000, 10000}; //1 2 20 50
    int n, ns, nn, t;
    n = 0;

    for (j = 1; j <= 8; j++)
    {
        for (l = -1; l < 1; l++)
        {
            ns = nn = 1;
            for (i = l; i < l + 5; i++) //米
            {
                if (j == 1)
                    t = gomoku[x][y - i]; //上
                if (j == 2)
                    t = gomoku[x + i][y - i]; //右上
                if (j == 3)
                    t = gomoku[x + i][y]; //右
                if (j == 4)
                    t = gomoku[x + i][y + i]; //右下
                if (j == 5)
                    t = gomoku[x][y + i]; //下
                if (j == 6)
                    t = gomoku[x - i][y + i]; //左下
                if (j == 7)
                    t = gomoku[x - i][y]; //左
                if (j == 8)
                    t = gomoku[x - i][y - i]; //左上

                if (t == s)
                    nn++;
                else if (t != 0)
                    ns = 0;
                if (ns)
                    n += snc[nn];
            }
        }
    }
    if (gomoku[x][y])
        n = 0;
    return n;
}
/* -----------------------------------------*/
// 判斷下棋點
int Strategy::PC_Strategy(SIDE s)
{
    int i, j;
    int cM;       //玩家最大值+電腦最大值
    int cN, iN;   //電腦這位置的值+ 玩家的
    int cMx, cMy; //下棋點x+y
    int rrM;      //隨機分配

    srand(time(NULL));
    //判斷電腦移動
    cM = 0;
    for (i = 0; i < ROW; i++)
        for (j = 0; j < COL; j++)
        {
            cN = Weights(2, i, j);
            iN = Weights(1, i, j); //求電腦與玩家的該空格分數
            if (iN > cN)
                cN = iN; //把較大者放到cN
            rrM = 0;
            if (cN == cM)
                rrM = rand() % 3 - 1; //若相等則隨機
            if (cN > cM + rrM)
            {
                cM = cN;
                cMx = i;
                cMy = j;
            }
        }
    if (state == CHOOSE_SIDE)
    {
        gomoku[ROW / 2][COL / 2] = s;
        chess.x = ROW / 2;
        chess.y = COL / 2;
    }
    else
    {
        gomoku[cMx][cMy] = s;
        chess.x = cMx;
        chess.y = cMy;
    }

    Line_Check(SIDE_PC);
    Show_Gomoku();
    return cMx * 100 + cMy;
}

/*=========================================
 * 
 * robot action
 * 
 ==========================================*/
/* case 3 and 6 problem */
bool Strategy::Check_Decide()
{
    switch (pcState)
    {
    case 1: // init home
        if (isBusy == false)
        {
            // nh.Pub_HomePos();
            nh.Pub_DataPos(nh.Get_pHome());
            isBusy = true;
        }
        else
        {
            nh.Pub_GetPos();
            if (nh.Get_Robot() == nh.Get_pHome())
            {
                pcState = 2;
                isBusy = false;
            }
        }
        return false;
    case 2: // move chess pos
        if (isBusy == false)
        {
            nh.Pub_DataPos(nh.Get_pChess());
            isBusy = true;
        }
        else
        {
            nh.Pub_GetPos();
            if (nh.Get_Robot() == nh.Get_pChess())
            {
                isBusy = false;
                if (nh.Is_grip())
                    pcState = 4;
                else
                    pcState = 3;
            }
        }
        return false;
    case 3: // Suction chess
        if (isBusy == false)
        {
            nh.Pub_DataPos(nh.Get_pChess());
            isBusy = true;
        }
        else
        {
            nh.Pub_GetPos();
            nh.suction_cmd_client(std::string("vacuumOn"));
            if (nh.Get_Robot() == nh.Get_pChess())
            {
                isBusy = false;
                pcState = 2;
            }
        }
        return false;
    case 4: // move board center pos
        if (isBusy == false)
        {
            nh.Pub_DataPos(nh.Get_pBoardCenter());
            isBusy = true;
        }
        else
        {
            nh.Pub_GetPos();
            if (nh.Get_Robot() == nh.Get_pBoardCenter())
            {
                isBusy = false;
                if (nh.Is_grip())
                    pcState = 5;
                else
                    return true;
            }
        }
        return false;
    case 5: // move board (i,j)
        if (isBusy == false)
        {
            nh.Pub_DataPos(nh.Get_pBoard(chess.x, chess.y));
            isBusy = true;
        }
        else
        {
            nh.Pub_GetPos();
            if (nh.Get_Robot() == nh.Get_pBoard(chess.x, chess.y))
            {
                isBusy = false;
                pcState = 7;
            }
        }
        return false;
    // case 6: // move to goal pos
    //     nh.Pub_DataPos(nh.Get_pChess());
    //     nh.Pub_GetPos();
    //     if (nh.Get_Robot() == nh.Get_pBoard(chess.x, chess.y))
    //     {
    //         pcState = 7;
    //     }
    //     return false;
    case 7: // plase chess
        nh.suction_cmd_client(std::string("vacuumOff"));
        pcState = 4;
        return false;
    default:
        printf("pcState error\n");
        return false;
    }
}

bool Strategy::Check_Push_Buttion()
{
    geometry_msgs::Twist robot_;
    switch (buttonState)
    {
    case 0: // go to button
        if (isBusy == false)
        {
            nh.Pub_DataPos(nh.Get_pButton());
            isBusy = true;
        }
        else
        {
            nh.Pub_GetPos();
            if (nh.Get_Robot() == nh.Get_pButton())
            {
                isBusy = false;

                /* for push button */
                // if (nh.IS_PushButton())
                // {
                //     buttonState = 2;
                //     nh.Init_Push_Button();
                // }
                // else
                // {
                //     buttonState = 1;
                // }

                /* for no push button */
                buttonState = 1;
            }
        }
        return false;
    case 1: // push button
        robot_ = nh.Get_pButton();
        robot_.linear.z += nh.Get_eButton();
        if (isBusy == false)
        {
            nh.Pub_DataPos(robot_);
            isBusy = true;
        }
        else
        {
            /* for push button */
            // if (nh.IS_PushButton())
            // {
            //     buttonState = 0;
            //     return false;
            // }

            // nh.Pub_GetPos();
            // if (nh.Get_Robot() == robot_)
            // {
            //     isBusy = false;
            //     buttonState = 0;
            // }

            /* for no push button */
            if (nh.Get_Robot() == robot_)
            {
                isBusy = false;
                buttonState = 3;
            }
        }
        return false;
    case 2: // go home
        if (isBusy == false)
        {
            // nh.Pub_HomePos();
            nh.Pub_DataPos(nh.Get_pHome());
            isBusy = true;
        }
        else
        {
            nh.Pub_GetPos();
            if (nh.Get_Robot() == nh.Get_pHome())
            {
                buttonState = 0;
                return true;
            }
        }
        return false;
    case 3:
        if (isBusy == false)
        {
            nh.Pub_DataPos(nh.Get_pButton());
            isBusy = true;
        }
        else
        {
            nh.Pub_GetPos();
            if (nh.Get_Robot() == nh.Get_pButton())
            {
                isBusy = false;
                buttonState = 2;
            }
        }
        return false;
    default:
        printf("buttonState error\n");
        return false;
    }
}

/*=========================================
 * 
 * show
 * 
 ==========================================*/

void Strategy::Show_Player()
{
    Player player = nh.Get_Player();
    cout << player.point.x << endl;
}

/*=========================================
 * 
 * tool
 * 
 ==========================================*/

void Strategy::Transform_Board()
{   
    if(nh.Check_vBorad_Size()){
        int color;
        for (int i = 0; i < ROW; i++)
        {
            for (int j = 0; j < COL; j++)
            {
                color = nh.Get_vBoard(i,j);
                if(color == pcColor){
                    gomoku[i][j] = SIDE_PC;
                }else if(color == playerColor){
                    gomoku[i][j] = SIDE_PLAYER;
                }else{
                    gomoku[i][j] = NOCOLOR;
                }
            }
        }
    }
}

void Strategy::Delay(double time){
    /* second */
    ros::Duration(time).sleep(); 
}