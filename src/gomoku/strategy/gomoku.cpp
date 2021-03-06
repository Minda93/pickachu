#include <iostream>
#include<stdio.h>
#include<stdlib.h>
#include <time.h>


using namespace std;

#define Row 10
#define Col 10
bool flag_human_first = 0;
int gomoku[Row][Col];
bool flag_game_end = 1;
static int step = 0;
bool flag_pc_first = 0;
typedef struct Coordinate          
{   
	int x;                         //行
	int y;                         //列
}Coordinate;


void init_gomoku()
{
	for (int i = 0 ; i < Row ; i++)
	{
		for (int j = 0 ; j<Col ; j++)
		{
			gomoku[i][j] = 0;
		}
	}

	system("pause");
}

void cout_gomoku()
{
	system("cls");
	cout<<"  ";
	for (int j = 0 ; j<Col ; j++)
	{
		cout<<j<<" ";
	}
	cout<<"\n";


	for (int i = 0 ; i < Row ; i++)
	{
		cout<<i<<" ";
		for (int j = 0 ; j<Col ; j++)
		{
			if(gomoku[i][j]==1)      {printf("X ");}
			else if(gomoku[i][j]==2)      {printf("O ");}
			else						{printf("+ ");}
			//cout<<gomoku[i][j]<<" ";
		}
		cout<<"\n";
	}

	system("pause");
}

void choose_first()
{
	cout<<"who go first"<<endl;
	cout<<"0 = computer"<<endl;
	cout<<"1 = human"<<endl;
}

void cin_first()
{

	cin>>flag_human_first;
	if (flag_human_first == 1)
	{
		flag_pc_first = 0;
	}else if (flag_human_first == 0)
	{
		flag_pc_first = 1;
	}
}

void who_first()
{
	if (flag_human_first == 0)
	{
		cout << "computer first" << endl;
	}
	else
	{
		cout << "human first" << endl;
	}
}

///////////////////////確認是否連線
int line_check(int s){
/*	int i,j,k;*/
 	int snc[6]={0,1,10,50,1000,10000}; //1 2 20 50
 	int n,ns,nn,t;
 	n=0;
	for (int x = 0 ; x < Row ; x++)
	{
		for (int y = 0; y< Col ; y++)
		{
			for(int j=1;j<=8;j++)
			{
				
					ns=nn=1;
					for(int i=0;i<5;i++)      //米
					{
						if ( ((x+i)/ Row) <= 1)
						{
							if(j==1)t=gomoku[ x ][y-i]; //上
							if(j==2)t=gomoku[x+i][y-i]; //右上
							if(j==3)t=gomoku[x+i][ y ]; //右
							if(j==4)t=gomoku[x+i][y+i]; //右下
							if(j==5)t=gomoku[ x ][y+i]; //下
							if(j==6)t=gomoku[x-i][y+i]; //左下
							if(j==7)t=gomoku[x-i][ y ]; //左
							if(j==8)t=gomoku[x-i][y-i]; //左上

							if     (t==s)nn++;
							else if(t!=0)ns=0;

							if(nn>5 && gomoku[x][y]==s)
							{
								cout_gomoku();
								if(s==1)printf("玩 家 獲勝!!");
								if(s==2)printf("電 腦 獲勝!!");
								system("pause");
								n=-1;
								return n;
							}

							if(ns)n+=snc[nn];
						}


					

					}
			}

		}


	}
}

int player_1() //玩家1
{
	cout<<"輸入座標 x,y "<<endl;
	int a,b;
	cin >> a ;
	if (cin.get()==',' ) //數字+逗號
	{
		cin>>b ;
	}
	gomoku[a][b]=1;
	line_check(1);
	return gomoku[a][b];
	
}

int player_2()	//玩家2
{
	cout<<"輸入座標 x,y "<<endl;
	int a,b;
	cin >> a ;
	if (cin.get()==',' ) // 數字+逗號
	{
		cin>>b ;
	}
	gomoku[a][b]=2;
	line_check(2);
	return gomoku[a][b];
	
}

int Weights(int s,int x,int y){
	int i,j,l;
	int snc[6]={0,1,10,50,1000,10000}; //1 2 20 50
	int n,ns,nn,t;
	n=0;

	for(j=1;j<=8;j++)
	{
		for(l=-1;l<1;l++)
		{
			ns=nn=1;
			for(i=l;i<l+5;i++)      //米
			{if(j==1)t=gomoku[ x ][y-i]; //上
			if(j==2)t=gomoku[x+i][y-i]; //右上
			if(j==3)t=gomoku[x+i][ y ]; //右
			if(j==4)t=gomoku[x+i][y+i]; //右下
			if(j==5)t=gomoku[ x ][y+i]; //下
			if(j==6)t=gomoku[x-i][y+i]; //左下
			if(j==7)t=gomoku[x-i][ y ]; //左
			if(j==8)t=gomoku[x-i][y-i]; //左上

			if     (t==s)nn++;
			else if(t!=0)ns=0;
			if(ns)n+=snc[nn];
			}
		}
	}
	if(gomoku[x][y])n=0;
	return n;
}
// 判斷下棋點
int pc(int s){
	int i,j;
	int cM;     //玩家最大值+電腦最大值
	int cN,iN;  //電腦這位置的值+ 玩家的
	int cMx,cMy;//下棋點x+y
	int rrM;    //隨機分配

	srand(time(NULL));
	//判斷電腦移動
	cM=0;
	for(i=0;i<Row;i++)
		for(j=0;j<Col;j++){
			cN=Weights(2,i,j);iN=Weights(1,i,j);                //求電腦與玩家的該空格分數
			if(iN>cN)cN=iN;                           //把較大者放到cN
			rrM=0;
			if(cN==cM)rrM=rand()%3-1;                //若相等則隨機
			if(cN>cM+rrM)
			{
				cM=cN;cMx=i;cMy=j;
			}
		}
		if (flag_pc_first == 1)
		{
			gomoku[Row/2][Col/2]=s;
			flag_pc_first = 0;

		}
		else if (flag_pc_first == 0)
		{
			gomoku[cMx][cMy]=s;
		}
		
		line_check(2);
		cout_gomoku();
		return cMx*100+cMy;

}

int main(void)
{
	int cMg;
	choose_first();
	cin_first();
	who_first();
	init_gomoku();
	cout_gomoku();
	while (flag_game_end == 1)
	{
		if (flag_human_first == 1)
		{
			while (flag_game_end)
			{
				player_1();
				cout_gomoku();
				pc(2);		
			}
		}else if (flag_human_first == 0)
		{
			pc(2);
			player_1();
			cout_gomoku();
			
		}
	}

	system("pause");
	return 0;

}
