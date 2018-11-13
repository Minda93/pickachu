// ========================================================
/* 
 * point class
 * --------------------------------------------------------*/
class Point {
    constructor() {
        this.pos = [0.0,0.0,0.0],
        this.euler = [0.0,0.0,0.0]
    }
}

// ========================================================
/* 
 * gomoku
 * --------------------------------------------------------*/
var ROW = 9;
var COL = 9;

var gomoku_pHome = new Point();
var gomoku_pChess = new Point();
var gomoku_pCenter = new Point();
var gomoku_pButton = new Point();
var gomoku_pBoard = [];
var gomoku_pBoard_1 = [new Point(),new Point(),new Point()];
var gomoku_pBoard_2 = [new Point(),new Point(),new Point()];


for(let i = 0;i<ROW*COL;i++){
    gomoku_pBoard.push(new Point());
}

// ========================================================
/* 
 * flaw
 * --------------------------------------------------------*/

var flaw_pHome = new Point();
var flaw_pCenter = new Point();
var flaw_pSuction = new Point();
var flaw_pFlaw = new Point();
var flaw_pNFlaw = new Point();

// ========================================================
/* 
 * air
 * --------------------------------------------------------*/

class Roll {
    constructor() {
        this.head = 0.0,
        this.front = 0.0,
        this.leftWing = 0.0,
        this.rightWing = 0.0,
        this.rear = 0.0,
        this.tail = 0.0
    }
}

var air_pHome = new Point();
var air_pCenter = new Point();
var air_pCamRight = new Point();
var air_pCamLeft = new Point();
var air_pSuction = new Point();
var air_pHead = new Point();
var air_pFront = new Point();
var air_pLeftWing = new Point();
var air_pRightWing = new Point();
var air_pRear = new Point();
var air_pTail = new Point();

var air_roll = new Roll();