// ========================================================
/* 
 * air fix point
 *
 * --------------------------------------------------------*/
function Init_Air_Fix_Point(state) {
    let pos = document.getElementsByName("airUI_pos");
    switch (state) {
        case 0:
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    pos[i].value = air_pHome.pos[i];
                } else {
                    pos[i].value = air_pHome.euler[i - 3];
                }
            }
            break;
        case 1:
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    pos[i].value = air_pCenter.pos[i];
                } else {
                    pos[i].value = air_pCenter.euler[i - 3];
                }
            }
            break;
        case 2:
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    pos[i].value = air_pCamRight.pos[i];
                } else {
                    pos[i].value = air_pCamRight.euler[i - 3];
                }
            }
            break;
        case 3:
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    pos[i].value = air_pCamLeft.pos[i];
                } else {
                    pos[i].value = air_pCamLeft.euler[i - 3];
                }
            }
            break;
        case 4:
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    pos[i].value = air_pSuction.pos[i];
                } else {
                    pos[i].value = air_pSuction.euler[i - 3];
                }
            }
            break;
        case 5:
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    pos[i].value = air_pHead.pos[i];
                } else {
                    pos[i].value = air_pHead.euler[i - 3];
                }
            }
            break;
        case 6:
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    pos[i].value = air_pFront.pos[i];
                } else {
                    pos[i].value = air_pFront.euler[i - 3];
                }
            }
            break;
        case 7:
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    pos[i].value = air_pLeftWing.pos[i];
                } else {
                    pos[i].value = air_pLeftWing.euler[i - 3];
                }
            }
            break;
        case 8:
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    pos[i].value = air_pRightWing.pos[i];
                } else {
                    pos[i].value = air_pRightWing.euler[i - 3];
                }
            }
            break;
        case 9:
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    pos[i].value = air_pRear.pos[i];
                } else {
                    pos[i].value = air_pRear.euler[i - 3];
                }
            }
            break;
        case 10:
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    pos[i].value = air_pTail.pos[i];
                } else {
                    pos[i].value = air_pTail.euler[i - 3];
                }
            }
            break;
        default:
            console.log('not state')
    }
}

/* param button */
document.getElementsByName("air_pButtion")[0].addEventListener("click", function () {
    console.log('Home');
    let obj = document.getElementById("airUI_label");
    Init_Air_Fix_Point(0);
    obj.innerHTML = "home";
});

document.getElementsByName("air_pButtion")[1].addEventListener("click", function () {
    console.log('Center');
    let obj = document.getElementById("airUI_label");
    Init_Air_Fix_Point(1);
    obj.innerHTML = "center";
});

document.getElementsByName("air_pButtion")[2].addEventListener("click", function () {
    console.log('CamRight');
    let obj = document.getElementById("airUI_label");
    Init_Air_Fix_Point(2);
    obj.innerHTML = "camright";
});

document.getElementsByName("air_pButtion")[3].addEventListener("click", function () {
    console.log('CamLeft');
    let obj = document.getElementById("airUI_label");
    Init_Air_Fix_Point(3);
    obj.innerHTML = "camleft";
});

document.getElementsByName("air_pButtion")[4].addEventListener("click", function () {
    console.log('Suction');
    let obj = document.getElementById("airUI_label");
    Init_Air_Fix_Point(4);
    obj.innerHTML = "suction";
});

document.getElementsByName("air_pButtion")[5].addEventListener("click", function () {
    console.log('Head');
    let obj = document.getElementById("airUI_label");
    Init_Air_Fix_Point(5);
    obj.innerHTML = "head";
});

document.getElementsByName("air_pButtion")[6].addEventListener("click", function () {
    console.log('Front');
    let obj = document.getElementById("airUI_label");
    Init_Air_Fix_Point(6);
    obj.innerHTML = "front";
});

document.getElementsByName("air_pButtion")[7].addEventListener("click", function () {
    console.log('LeftWing');
    let obj = document.getElementById("airUI_label");
    Init_Air_Fix_Point(7);
    obj.innerHTML = "leftwing";
});

document.getElementsByName("air_pButtion")[8].addEventListener("click", function () {
    console.log('RightWing');
    let obj = document.getElementById("airUI_label");
    Init_Air_Fix_Point(8);
    obj.innerHTML = "rightwing";
});

document.getElementsByName("air_pButtion")[9].addEventListener("click", function () {
    console.log('Rear');
    let obj = document.getElementById("airUI_label");
    Init_Air_Fix_Point(9);
    obj.innerHTML = "rear";
});

document.getElementsByName("air_pButtion")[10].addEventListener("click", function () {
    console.log('Tail');
    let obj = document.getElementById("airUI_label");
    Init_Air_Fix_Point(10);
    obj.innerHTML = "tail";
});


/* now point */
document.getElementById("airUI_pNow").addEventListener("click", function () {
    console.log('air nowpoint');
    Pub_GetPos();
    GetPos("airUI_pos");
});

/* confirm */
document.getElementById("airUI_confirm").addEventListener("click", function () {
    console.log('air confirm');
    let label = document.getElementById("airUI_label").innerHTML;
    let pos = document.getElementsByName("airUI_pos");
    switch (label) {
        case 'home':
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    air_pHome.pos[i] = parseFloat(pos[i].value);
                } else {
                    air_pHome.euler[i - 3] = parseFloat(pos[i].value);
                }
            }
            console.log('home', air_pHome.pos, air_pHome.euler);
            Air_Set_Param('home');
            break;
        case 'center':
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    air_pCenter.pos[i] = parseFloat(pos[i].value);
                } else {
                    air_pCenter.euler[i - 3] = parseFloat(pos[i].value);
                }
            }
            console.log('center', air_pCenter.pos, air_pCenter.euler);
            Air_Set_Param('center');
            break;
        case 'camright':
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    air_pCamRight.pos[i] = parseFloat(pos[i].value);
                } else {
                    air_pCamRight.euler[i - 3] = parseFloat(pos[i].value);
                }
            }
            console.log('camright', air_pCamRight.pos, air_pCamRight.euler);
            Air_Set_Param('camright');
            break;
        case 'camleft':
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    air_pCamLeft.pos[i] = parseFloat(pos[i].value);
                } else {
                    air_pCamLeft.euler[i - 3] = parseFloat(pos[i].value);
                }
            }
            console.log('camleft', air_pCamLeft.pos, air_pCamLeft.euler);
            Air_Set_Param('camleft');
            break;
        case 'suction':
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    air_pSuction.pos[i] = parseFloat(pos[i].value);
                } else {
                    air_pSuction.euler[i - 3] = parseFloat(pos[i].value);
                }
            }
            console.log('suction', air_pSuction.pos, air_pSuction.euler);
            Air_Set_Param('suction');
            break;
        case 'head':
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    air_pHead.pos[i] = parseFloat(pos[i].value);
                } else {
                    air_pHead.euler[i - 3] = parseFloat(pos[i].value);
                }
            }
            console.log('head', air_pHead.pos, air_pHead.euler);
            Air_Set_Param('head');
            break;
        case 'front':
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    air_pFront.pos[i] = parseFloat(pos[i].value);
                } else {
                    air_pFront.euler[i - 3] = parseFloat(pos[i].value);
                }
            }
            console.log('front', air_pFront.pos, air_pFront.euler);
            Air_Set_Param('front');
            break;
        case 'leftwing':
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    air_pLeftWing.pos[i] = parseFloat(pos[i].value);
                } else {
                    air_pLeftWing.euler[i - 3] = parseFloat(pos[i].value);
                }
            }
            console.log('leftwing', air_pLeftWing.pos, air_pLeftWing.euler);
            Air_Set_Param('leftwing');
            break;
        case 'rightwing':
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    air_pRightWing.pos[i] = parseFloat(pos[i].value);
                } else {
                    air_pRightWing.euler[i - 3] = parseFloat(pos[i].value);
                }
            }
            console.log('rightwing', air_pRightWing.pos, air_pRightWing.euler);
            Air_Set_Param('rightwing');
            break;
        case 'rear':
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    air_pRear.pos[i] = parseFloat(pos[i].value);
                } else {
                    air_pRear.euler[i - 3] = parseFloat(pos[i].value);
                }
            }
            console.log('rear', air_pRear.pos, air_pRear.euler);
            Air_Set_Param('rear');
            break;
        case 'tail':
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    air_pTail.pos[i] = parseFloat(pos[i].value);
                } else {
                    air_pTail.euler[i - 3] = parseFloat(pos[i].value);
                }
            }
            console.log('tail', air_pTail.pos, air_pTail.euler);
            Air_Set_Param('tail');
            break;
        default:
            console.log('not label')
    }
});