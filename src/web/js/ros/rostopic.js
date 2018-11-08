/* node list

    
*/
/*========================================================*/
/*
    /accupick3d/cmdString
 */
/*--------------------------------------------------------*/
//pub GetPos
function Pub_GetPos() {
    var msg = new ROSLIB.Message({
        data: 'GetPos:'
    });
    topicCmdString.Pub(msg);
}

/*========================================================*/
/*
    /accupick3d/msgString
 */
/*--------------------------------------------------------*/
//sub GetPos
/*
    case GetPos for input
    case GetPos_Board for no input ex: board1 and board2
*/
const GetPos = async (name) => {
    try {
        const param = await topicMsgString.Sub();
        str = param.data.split(":");

        let obj = document.getElementsByName(name);
        if(str[0] == 'Pos'){
            for(let i = 1;i<str.length;i++){
                obj[i-1].value = str[i];
            }
        }
        console.log(name, param);
    } catch (err) {
        console.log(err);
    }
};

const GetPos_Board = async (name, i) => {
    try {
        const param = await topicMsgString.Sub();
        str = param.data.split(":");

        if (str[0] == 'Pos') {
            switch (name) {
                case 'board1':
                    gomoku_pBoard_1[i].pos[0] = parseFloat(str[1]);
                    gomoku_pBoard_1[i].pos[1] = parseFloat(str[2]);
                    gomoku_pBoard_1[i].pos[2] = parseFloat(str[3]);
                    gomoku_pBoard_1[i].euler[0] = parseFloat(str[4]);
                    gomoku_pBoard_1[i].euler[1] = parseFloat(str[5]);
                    gomoku_pBoard_1[i].euler[2] = parseFloat(str[6]);
                    break;
                case 'board2':
                    gomoku_pBoard_2[i].pos[0] = parseFloat(str[1]);
                    gomoku_pBoard_2[i].pos[1] = parseFloat(str[2]);
                    gomoku_pBoard_2[i].pos[2] = parseFloat(str[3]);
                    gomoku_pBoard_2[i].euler[0] = parseFloat(str[4]);
                    gomoku_pBoard_2[i].euler[1] = parseFloat(str[5]);
                    gomoku_pBoard_2[i].euler[2] = parseFloat(str[6]);
                    break;
                default:
                    break;
            }
        }
        // console.log(gomoku_pBoard_1);
        console.log(gomoku_pBoard_2);
    } catch (err) {
        console.log(err);
    }
};