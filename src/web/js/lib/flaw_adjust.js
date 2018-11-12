// ========================================================
/* 
 * flaw fix point
 *
 * --------------------------------------------------------*/
function Init_Flaw_Fix_Point(state) {
    let pos = document.getElementsByName("flawUI_pos");
    switch (state) {
        case 0:
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    pos[i].value = flaw_pHome.pos[i];
                } else {
                    pos[i].value = flaw_pHome.euler[i - 3];
                }
            }
            break;
        case 1:
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    pos[i].value = flaw_pCenter.pos[i];
                } else {
                    pos[i].value = flaw_pCenter.euler[i - 3];
                }
            }
            break;
        case 2:
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    pos[i].value = flaw_pSuction.pos[i];
                } else {
                    pos[i].value = flaw_pSuction.euler[i - 3];
                }
            }
            break;
        case 3:
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    pos[i].value = flaw_pFlaw.pos[i];
                } else {
                    pos[i].value = flaw_pFlaw.euler[i - 3];
                }
            }
            break;
        case 4:
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    pos[i].value = flaw_pNFlaw.pos[i];
                } else {
                    pos[i].value = flaw_pNFlaw.euler[i - 3];
                }
            }
            break;
        default:
            console.log('not state')
    }
}


document.getElementsByName("flaw_pButtion")[0].addEventListener("click", function () {
    console.log('Home');
    let obj = document.getElementById("flawUI_label");
    Init_Flaw_Fix_Point(0);
    obj.innerHTML = "home";
});

document.getElementsByName("flaw_pButtion")[1].addEventListener("click", function () {
    console.log('Center');
    let obj = document.getElementById("flawUI_label");
    Init_Flaw_Fix_Point(1);
    obj.innerHTML = "center";
});


document.getElementsByName("flaw_pButtion")[2].addEventListener("click", function () {
    console.log('Suction');
    let obj = document.getElementById("flawUI_label");
    Init_Flaw_Fix_Point(2);
    obj.innerHTML = "suction";
});

document.getElementsByName("flaw_pButtion")[3].addEventListener("click", function () {
    console.log('Flaw');
    let obj = document.getElementById("flawUI_label");
    Init_Flaw_Fix_Point(3);
    obj.innerHTML = "flaw";
});

document.getElementsByName("flaw_pButtion")[4].addEventListener("click", function () {
    console.log('NFlaw');
    let obj = document.getElementById("flawUI_label");
    Init_Flaw_Fix_Point(4);
    obj.innerHTML = "nflaw";
});


/* now point */
document.getElementById("flawUI_pNow").addEventListener("click", function () {
    console.log('flaw nowpoint');
    Pub_GetPos();
    GetPos("flawUI_pos");
});

/* confirm */
document.getElementById("flawUI_confirm").addEventListener("click", function () {
    console.log('flaw confirm');
    let label = document.getElementById("flawUI_label").innerHTML;
    let pos = document.getElementsByName("flawUI_pos");
    switch (label) {
        case 'home':
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    flaw_pHome.pos[i] = parseFloat(pos[i].value);
                } else {
                    flaw_pHome.euler[i - 3] = parseFloat(pos[i].value);
                }
            }
            console.log('home', flaw_pHome.pos, flaw_pHome.euler);
            Flaw_Set_Param('home');
            break;
        case 'center':
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    flaw_pCenter.pos[i] = parseFloat(pos[i].value);
                } else {
                    flaw_pCenter.euler[i - 3] = parseFloat(pos[i].value);
                }
            }
            console.log('center', flaw_pCenter.pos, flaw_pCenter.euler);
            Flaw_Set_Param('center');
            break;
        case 'suction':
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    flaw_pSuction.pos[i] = parseFloat(pos[i].value);
                } else {
                    flaw_pSuction.euler[i - 3] = parseFloat(pos[i].value);
                }
            }
            console.log('suction', flaw_pSuction.pos, flaw_pSuction.euler);
            Flaw_Set_Param('suction');
            break;
        case 'flaw':
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    flaw_pFlaw.pos[i] = parseFloat(pos[i].value);
                } else {
                    flaw_pFlaw.euler[i - 3] = parseFloat(pos[i].value);
                }
            }
            console.log('flaw', flaw_pFlaw.pos, flaw_pFlaw.euler);
            Flaw_Set_Param('flaw');
            break;
        case 'nflaw':
            for (let i = 0; i < pos.length; i++) {
                if (i < 3) {
                    flaw_pNFlaw.pos[i] = parseFloat(pos[i].value);
                } else {
                    flaw_pNFlaw.euler[i - 3] = parseFloat(pos[i].value);
                }
            }
            console.log('nflaw', flaw_pNFlaw.pos, flaw_pNFlaw.euler);
            Flaw_Set_Param('nflaw');
            break;
        default:
            console.log('not label')
    }
});

// ========================================================
/* 
 * flaw fix point
 *
 * --------------------------------------------------------*/