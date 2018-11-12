function Init(){
    console.log("init");
    Init_Board();


    setTimeout(function(){
        Init_Gomoku_Param();
    },500);

    setTimeout(function(){
        Init_Flaw_Param();
    },500);
}