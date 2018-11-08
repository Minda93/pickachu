
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
                    default:
                        break;
                }
            }
        } else {
            console.log("SCAN_PARAM : default");
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