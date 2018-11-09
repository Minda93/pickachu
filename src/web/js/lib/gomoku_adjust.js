// ========================================================
/* 
 * gomoku fix point
 *
 * --------------------------------------------------------*/

document.getElementsByName("gomoku_pButtion")[0].addEventListener("click", function () {
    console.log('Home');
    let obj = document.getElementById("gomokuUIButton_label");
    Init_Gomoku_Fix_Point(0);
    obj.innerHTML = "home";
});

document.getElementsByName("gomoku_pButtion")[1].addEventListener("click", function () {
    console.log('chess');
    let obj = document.getElementById("gomokuUIButton_label");
    Init_Gomoku_Fix_Point(1);
    obj.innerHTML = "chess";
});

document.getElementsByName("gomoku_pButtion")[2].addEventListener("click", function () {
    console.log('center');
    let obj = document.getElementById("gomokuUIButton_label");
    Init_Gomoku_Fix_Point(2);
    obj.innerHTML = "center";
});

document.getElementsByName("gomoku_pButtion")[3].addEventListener("click", function () {
    console.log('button');
    let obj = document.getElementById("gomokuUIButton_label");
    Init_Gomoku_Fix_Point(3);
    obj.innerHTML = "button";
});


/* now point */
document.getElementById("gomokuUIButton_pNow").addEventListener("click", function () {
    console.log('gomoku nowpoint');
    Pub_GetPos();
    GetPos("gomokuUIButtion_pos");
});

/* confirm */
document.getElementById("gomokuUIButton_confirm").addEventListener("click", function () {
    console.log('gomoku confirm');
    let label = document.getElementById("gomokuUIButton_label").innerHTML;
    let pos = document.getElementsByName("gomokuUIButtion_pos");
    switch (label) {
        case 'home':
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    gomoku_pHome.pos[i] = parseFloat(pos[i].value);
                } else {
                    gomoku_pHome.euler[i - 3] = parseFloat(pos[i].value);
                }
            }
            console.log('home', gomoku_pHome.pos, gomoku_pHome.euler);
            Gomoku_Set_Param('home');
            break;
        case 'chess':
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    gomoku_pChess.pos[i] = parseFloat(pos[i].value);
                } else {
                    gomoku_pChess.euler[i - 3] = parseFloat(pos[i].value);
                }
            }
            console.log('chess', gomoku_pChess.pos, gomoku_pChess.euler);
            Gomoku_Set_Param('chess');
            break;
        case 'center':
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    gomoku_pCenter.pos[i] = parseFloat(pos[i].value);
                } else {
                    gomoku_pCenter.euler[i - 3] = parseFloat(pos[i].value);
                }
            }
            console.log('center', gomoku_pCenter.pos, gomoku_pCenter.euler);
            Gomoku_Set_Param('center');
            break;
        case 'button':
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    gomoku_pButton.pos[i] = parseFloat(pos[i].value);
                } else {
                    gomoku_pButton.euler[i - 3] = parseFloat(pos[i].value);
                }
            }
            
            console.log('button', gomoku_pButton.pos, gomoku_pButton.euler);
            Gomoku_Set_Param('button');
            break;
    }
    Pub_Gomoku_Save();
});

function Init_Gomoku_Fix_Point(state) {
    let pos = document.getElementsByName("gomokuUIButtion_pos");
    switch (state) {
        case 0:
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    pos[i].value = gomoku_pHome.pos[i];
                } else {
                    pos[i].value = gomoku_pHome.euler[i - 3];
                }
            }
            break;
        case 1:
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    pos[i].value = gomoku_pChess.pos[i];
                } else {
                    pos[i].value = gomoku_pChess.euler[i - 3];
                }
            }
            break;
        case 2:
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    pos[i].value = gomoku_pCenter.pos[i];
                } else {
                    pos[i].value = gomoku_pCenter.euler[i - 3];
                }
            }
            break;
        case 3:
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    pos[i].value = gomoku_pButton.pos[i];
                } else {
                    pos[i].value = gomoku_pButton.euler[i - 3];
                }
            }
            break;
    }
}

// ========================================================
/* 
 * gomoku board auto point
 *
 * --------------------------------------------------------*/
document.getElementsByName("gomokuUIBoard1_pNow")[0].addEventListener("click", function () {
    Pub_GetPos();
    GetPos_Board('board1', 0);
});

document.getElementsByName("gomokuUIBoard1_pNow")[1].addEventListener("click", function () {
    Pub_GetPos();
    GetPos_Board('board1', 1);
});

document.getElementsByName("gomokuUIBoard1_pNow")[2].addEventListener("click", function () {
    Pub_GetPos();
    GetPos_Board('board1', 2);
});

document.getElementById("gomokuUIBoard1_confirm").addEventListener("click", function () {
    let error = document.getElementsByName("gomokuUIBoard1_error");


    // for (let i = 0; i < ROW; i++) {
    //     for (let j = 0; j < COL; j++) {

    //     }
    // }
});

/* ======================================================= */

document.getElementsByName("gomokuUIBoard2_pNow")[0].addEventListener("click", function () {
    Pub_GetPos();
    GetPos_Board('board2', 0);
});

document.getElementsByName("gomokuUIBoard2_pNow")[1].addEventListener("click", function () {
    Pub_GetPos();
    GetPos_Board('board2', 1);
});

document.getElementsByName("gomokuUIBoard2_pNow")[2].addEventListener("click", function () {
    Pub_GetPos();
    GetPos_Board('board2', 2);
});

document.getElementById("gomokuUIBoard2_confirm").addEventListener("click", function () {

    // 分點公式
    gomoku_pBoard[0].euler = gomoku_pBoard_2[0].euler;
    gomoku_pBoard[0].pos = gomoku_pBoard_2[0].pos;
    gomoku_pBoard[(COL-1)].euler = gomoku_pBoard_2[1].euler;
    gomoku_pBoard[(COL-1)].pos = gomoku_pBoard_2[1].pos;
    gomoku_pBoard[(ROW-1) * COL].euler = gomoku_pBoard_2[2].euler;
    gomoku_pBoard[(ROW-1) * COL].pos = gomoku_pBoard_2[2].pos;
    for (let i = 1; i < COL - 1; i++) {
        gomoku_pBoard[i].euler = gomoku_pBoard[0].euler;
        gomoku_pBoard[i].pos[0] = ((i) * gomoku_pBoard_2[1].pos[0] + (COL - (i + 1)) * gomoku_pBoard_2[0].pos[0]) / (COL - 1);
        gomoku_pBoard[i].pos[1] = ((i) * gomoku_pBoard_2[1].pos[1] + (COL - (i + 1)) * gomoku_pBoard_2[0].pos[1]) / (COL - 1);
        gomoku_pBoard[i].pos[2] = ((i) * gomoku_pBoard_2[1].pos[2] + (COL - (i + 1)) * gomoku_pBoard_2[0].pos[2]) / (COL - 1);
    }

    for (let i = 1; i < ROW - 1; i++) {
        gomoku_pBoard[i * COL + 0].euler = gomoku_pBoard[0].euler;
        gomoku_pBoard[i * COL + 0].pos[0] = ((i) * gomoku_pBoard_2[2].pos[0] + (ROW - (i + 1)) * gomoku_pBoard_2[0].pos[0]) / (ROW - 1);
        gomoku_pBoard[i * COL + 0].pos[1] = ((i) * gomoku_pBoard_2[2].pos[1] + (ROW - (i + 1)) * gomoku_pBoard_2[0].pos[1]) / (ROW - 1);
        gomoku_pBoard[i * COL + 0].pos[2] = ((i) * gomoku_pBoard_2[2].pos[2] + (ROW - (i + 1)) * gomoku_pBoard_2[0].pos[2]) / (ROW - 1);
    }

    for (let i = 1; i < ROW; i++) {
        for (let j = 1; j < COL; j++) {
            gomoku_pBoard[i*COL+j].euler = gomoku_pBoard[0].euler;

            gomoku_pBoard[i*COL+j].pos[0] = gomoku_pBoard[i*COL+0].pos[0];
            gomoku_pBoard[i*COL+j].pos[1] = gomoku_pBoard[0*COL+j].pos[1];

            // 假設z固定
            gomoku_pBoard[i*COL+j].pos[2] = gomoku_pBoard[0].pos[2];
        }
    }

    Gomoku_Set_Param('board');
    Pub_Gomoku_Save();
});

function Init_Board() {
    for (let i = 0; i < ROW * COL; i++) {
        var board = document.getElementsByName("gomoku_pos");
        board[i].addEventListener("click", function () {
            let label = document.getElementById("gomokuUI_label");
            let pos = document.getElementsByName("gomokuUI_pos");
            let check = document.getElementById("gomoku_adjust");
            label.innerHTML = String(parseInt(i / ROW)) + "-" + String(i % ROW);
            for (let j = 0; j < pos.length; j++) {
                if (j < 3) {
                    pos[j].value = gomoku_pBoard[i].pos[j];
                } else {
                    pos[j].value = gomoku_pBoard[i].euler[j - 3];
                }
            }
            if(check.checked == false){
                console.log(String(parseInt(i / ROW)) + "-" + String(i % ROW));

                Call_ArmControl(gomoku_pBoard[parseInt(i / ROW)*COL+(i % ROW)]);
            }
        });
    }
}

// ========================================================
/* 
 * gomoku board point
 *
 * --------------------------------------------------------*/

document.getElementById("gomokuUI_pNow").addEventListener("click", function () {
    Pub_GetPos();
    GetPos("gomokuUI_pos");
});

document.getElementById("gomokuUI_confirm").addEventListener("click", function () {
    let label = document.getElementById("gomokuUI_label");
    let obj = document.getElementsByName("gomokuUI_pos");
    let str = label.innerHTML.split('-');
    for(let i = 0;i<obj.length;i++){
        if(i<3){
            gomoku_pBoard[parseInt(str[0])*COL+parseInt(str[1])].pos[i] = parseFloat(obj[i].value);
        }else{
            gomoku_pBoard[parseInt(str[0])*COL+parseInt(str[1])].euler[i-3] = parseFloat(obj[i].value);
        }
    }
    // console.log(str[0],str[1],gomoku_pBoard[parseInt(str[0])*COL+parseInt(str[1])]);
    Gomoku_Set_Param('board');
    Pub_Gomoku_Save();
});

// ========================================================
/* 
 * gomoku board close adjust
 *
 * --------------------------------------------------------*/

document.getElementById("gomoku_adjust").addEventListener("click", function () {
    if(this.checked == true){
        for(let i = 0;i<document.getElementsByName("gomoku_pos").length;i++)
            document.getElementsByName("gomoku_pos")[i].dataset.toggle = "modal";
    }else{
        for(let i = 0;i<document.getElementsByName("gomoku_pos").length;i++)
            document.getElementsByName("gomoku_pos")[i].dataset.toggle = "";
    }
    // Init_Board();
});