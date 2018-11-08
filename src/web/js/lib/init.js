function Init(){
    console.log("init");
    Init_Board();


    setTimeout(function(){
        Init_Gomoku_Param();
    },500);
}