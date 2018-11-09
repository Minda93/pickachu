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