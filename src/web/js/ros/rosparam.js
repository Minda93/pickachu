/*========================================================*/
/*
    gomoku node
 */
/*--------------------------------------------------------*/

const Init_Gomoku_Param = async () => {
    try {
        const param = await paramGomoku.Get();
        if (param != null) {
            for (var item in param) {
                switch (item) {
                    case "pHome":
                        gomoku_pHome = param.pHome;
                        break;
                    case "pChess":
                        gomoku_pChess = param.pChess;
                        break;
                    case "pBoardCenter":
                        gomoku_pCenter = param.pBoardCenter;
                        break;
                    case "pButton":
                        gomoku_pButton = param.pButton;
                        break;
                    case "pBoard":
                        gomoku_pBoard = param.pBoard;
                        break;
                    case "error_height":
                        document.getElementsByName("gomoku_pElement")[0].value = param.error_height;
                        break;
                    default:
                        break;
                }
            }
        } else {
            console.log("Gomoku_PARAM : default");
        }
    } catch (err) {
        console.log(err);
    }
};

function Gomoku_Set_Param(name) {
    switch (name) {
        case 'home':
            paramGomokupHome.Set(gomoku_pHome);
            break;
        case 'chess':
            paramGomokupChess.Set(gomoku_pChess);
            break;
        case 'center':
            paramGomokupBoardCenter.Set(gomoku_pCenter);
            break;
        case 'board':
            paramGomokupBoard.Set(gomoku_pBoard);
            break;
        case 'button':
            paramGomokupButton.Set(gomoku_pButton);
            break;
        default:
            break;
    }
}

/*========================================================*/
/*
    flaw node
 */
/*--------------------------------------------------------*/

const Init_Flaw_Param = async () => {
    try {
        const param = await paramFlaw.Get();
        if (param != null) {
            for (var item in param) {
                switch (item) {
                    case "pHome":
                        flaw_pHome = param.pHome;
                        break;
                    case "pCenter":
                        flaw_pCenter = param.pCenter;
                        break;
                    case "pSuction":
                        flaw_pSuction = param.pSuction;
                        break;
                    case "pFlaw":
                        flaw_pFlaw = param.pFlaw;
                        break;
                    case "pNFlaw":
                        flaw_pNFlaw = param.pNFlaw;
                        break;
                    case "checkROI":
                        document.getElementsByName("flaw_pElement")[0].value = param.checkROI;
                        break;
                    case "pixelRate":
                        document.getElementsByName("flaw_pElement")[1].value = param.pixelRate;
                        break;
                    case "slideX":
                        document.getElementsByName("flaw_pElement")[2].value = param.slideX;
                        break;
                    case "slideY":
                        document.getElementsByName("flaw_pElement")[3].value = param.slideY;
                        break;
                    case "slideZ":
                        document.getElementsByName("flaw_pElement")[4].value = param.slideZ;
                        break;
                    case "score_threshold":
                        document.getElementsByName("flaw_pElement")[5].value = param.score_threshold;
                        break;
                    case "flaw_threshold":
                        document.getElementsByName("flaw_pElement")[6].value = param.flaw_threshold;
                        break;
                    default:
                        break;
                }
            }
        } else {
            console.log("Flaw_PARAM : default");
        }
    } catch (err) {
        console.log(err);
    }
};

function Flaw_Set_Param(name) {
    switch (name) {
        case 'home':
            paramFlawpHome.Set(flaw_pHome);
            break;
        case 'center':
            paramFlawpCenter.Set(flaw_pCenter);
            break;
        case 'suction':
            paramFlawpSuction.Set(flaw_pSuction);
            break;
        case 'flaw':
            paramFlawpFlaw.Set(flaw_pFlaw);
            break;
        case 'nflaw':
            paramFlawpNFlaw.Set(flaw_pNFlaw);
            break;
        default:
            break;
    }
}

/*========================================================*/
/*
    air node
 */
/*--------------------------------------------------------*/

const Init_Air_Param = async () => {
    try {
        const param = await paramFlaw.Get();
        if (param != null) {
            for (var item in param) {
                switch (item) {
                    case "pHome":
                        air_pHome = param.pHome;
                        break;
                    case "pCenter":
                        air_pCenter = param.pCenter;
                        break;
                    case "pCamRight":
                        air_pCamRight = param.pCamRight;
                        break;
                    case "pCamLeft":
                        air_pCamLeft = param.pCamLeft;
                        break;
                    case "pSuction":
                        air_pSuction = param.pSuction;
                        break;
                    case "pHead":
                        air_pHead = param.pHead;
                        break;
                    case "pFront":
                        air_pFront = param.pFront;
                        break;
                    case "pLeftWing":
                        air_pLeftWing = param.pLeftWing;
                        break;
                    case "pRightWing":
                        air_pRightWing = param.pRightWing;
                        break;
                    case "pRear":
                        air_pRear = param.pRear;
                        break;
                    case "pTail":
                        air_pTail = param.pTail;
                        break;
                    case "rollObject":
                        document.getElementsByName("air_pElement")[0].value = param.rollObject.Head;
                        document.getElementsByName("air_pElement")[1].value = param.rollObject.Front;
                        document.getElementsByName("air_pElement")[2].value = param.rollObject.LeftWing;
                        document.getElementsByName("air_pElement")[3].value = param.rollObject.RightWing;
                        document.getElementsByName("air_pElement")[4].value = param.rollObject.Rear;
                        document.getElementsByName("air_pElement")[5].value = param.rollObject.Tail;
                        break;
                    case "checkROI":
                        document.getElementsByName("air_pElement")[6].value = param.checkROI;
                        break;
                    case "pixelRate":
                        document.getElementsByName("air_pElement")[7].value = param.pixelRate;
                        break;
                    case "score_threshold":
                        document.getElementsByName("air_pElement")[8].value = param.score_threshold;
                        break;
                    default:
                        break;
                }
            }
        } else {
            console.log("Air_PARAM : default");
        }
    } catch (err) {
        console.log(err);
    }
};

function Air_Set_Param(name) {
    switch (name) {
        case 'home':
            paramAirpHome.Set(air_pHome);
            break;
        case 'center':
            paramAirpCenter.Set(air_pCenter);
            break;
        case 'camright':
            paramAirpCamRight.Set(air_pCamRight);
            break;
        case 'camleft':
            paramAirpCamLeft.Set(air_pCamLeft);
            break;
        case 'suction':
            paramAirpSuction.Set(air_pSuction);
            break;
        case 'head':
            paramAirpHead.Set(air_pHead);
            break;
        case 'front':
            paramAirpFront.Set(air_pFront);
            break;
        case 'leftwing':
            paramAirpLeftWing.Set(air_pLeftWing);
            break;
        case 'rightwing':
            paramAirpRightWing.Set(air_pRightWing);
            break;
        case 'rear':
            paramAirpRear.Set(air_pRear);
            break;
        case 'tail':
            paramAirpTail.Set(air_pTail);
            break;
        default:
            break;
    }
}