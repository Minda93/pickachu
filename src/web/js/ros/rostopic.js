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
        if (str[0] == 'GetPos') {
            for (let i = 1; i < str.length; i++) {
                obj[i - 1].value = str[i];
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

        if (str[0] == 'GetPos') {
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

/*========================================================*/
/*
    /accupick3d/is_busy
 */
/*--------------------------------------------------------*/
topicIsBusy.object.subscribe(function (msg) {
    isBusy = msg.data;
});

/*========================================================*/
/*========================================================*/

/*========================================================*/
/*
    gomoku test button
 */
/*--------------------------------------------------------*/

document.getElementsByName("gomoku_tButtion")[0].addEventListener("click", function () {
    Call_ArmControl(gomoku_pHome);
    console.log("Call Home");
});

document.getElementsByName("gomoku_tButtion")[1].addEventListener("click", function () {
    let pos_ = new Point();
    pos_.pos[0] = gomoku_pChess.pos[0];
    pos_.pos[1] = gomoku_pChess.pos[1];
    pos_.pos[2] = gomoku_pChess.pos[2];
    pos_.euler = gomoku_pChess.euler;

    pos_.pos[2] += parseFloat(document.getElementsByName("gomoku_pElement")[0].value);
    Call_ArmControl(pos_);
    console.log("Call UpChess");
});

document.getElementsByName("gomoku_tButtion")[2].addEventListener("click", function () {
    Call_ArmControl(gomoku_pChess);
    console.log("Call Chess");
});

document.getElementsByName("gomoku_tButtion")[3].addEventListener("click", function () {
    Call_ArmControl(gomoku_pCenter);
    console.log("Call Center");
});

document.getElementsByName("gomoku_tButtion")[4].addEventListener("click", function () {
    let pos_ = new Point();
    pos_.pos[0] = gomoku_pButton.pos[0];
    pos_.pos[1] = gomoku_pButton.pos[1];
    pos_.pos[2] = gomoku_pButton.pos[2];
    pos_.euler = gomoku_pButton.euler;

    pos_.pos[2] += parseFloat(document.getElementsByName("gomoku_pElement")[0].value);
    Call_ArmControl(pos_);
    console.log("Call Button");
});

document.getElementsByName("gomoku_tButtion")[5].addEventListener("click", function () {
    Call_ArmControl(gomoku_pButton);
    console.log("Call pushButton");
});

/*========================================================*/
/*
    /gomoku/save
 */
/*--------------------------------------------------------*/
function Pub_Gomoku_Save() {
    var msg = new ROSLIB.Message({
        data: true
    });
    topicGomokuSave.Pub(msg);
}

document.getElementById("gomoku_paramSave").addEventListener("click", function () {
    Pub_Gomoku_Save();
    console.log('save');
});

document.getElementById("gomoku_paramSet").addEventListener("click", function () {
    let valueList = document.getElementsByName("gomoku_pElement");

    paramGomokuErrorHeight.Set(parseFloat(valueList[0].value));

});

/*========================================================*/
/*
    gomoku tool
 */
/*--------------------------------------------------------*/
document.getElementById("gomoku_Init").addEventListener("click", function () {
    var msg = new ROSLIB.Message({
        data: 0
    });
    topicGomokuState.Pub(msg);
});

document.getElementById("gomoku_Start").addEventListener("click", function () {
    var msg = new ROSLIB.Message({
        data: true
    });
    topicGomokuStart.Pub(msg);
});

document.getElementById("gomoku_Stop").addEventListener("click", function () {
    var msg = new ROSLIB.Message({
        data: false
    });
    topicGomokuStart.Pub(msg);
});

document.getElementById("gomoku_Side").addEventListener("click", function () {
    let value = parseInt(document.getElementById("gomoku_sideValue").value);
    var msg = new ROSLIB.Message({
        data: value
    });
    topicGomokuSide.Pub(msg);
});

/*========================================================*/
/*========================================================*/

/*========================================================*/
/*
    flaw tool
 */
/*--------------------------------------------------------*/

document.getElementById("flaw_Init").addEventListener("click", function () {
    var msg = new ROSLIB.Message({
        data: 0
    });
    topicFlawState.Pub(msg);
});

document.getElementById("flaw_Start").addEventListener("click", function () {
    var msg = new ROSLIB.Message({
        data: true
    });
    topicFlawStart.Pub(msg);
});

document.getElementById("flaw_Stop").addEventListener("click", function () {
    var msg = new ROSLIB.Message({
        data: false
    });
    topicFlawStart.Pub(msg);
});


/*========================================================*/
/*
    flaw save
 */
/*--------------------------------------------------------*/

function Pub_Flaw_Save() {
    let msg = new ROSLIB.Message({
        data: true
    });
    topicFlawSave.Pub(msg);
}

document.getElementById("flaw_paramSave").addEventListener("click", function () {
    Pub_Flaw_Save();
    console.log('save');
});

document.getElementById("flaw_paramSet").addEventListener("click", function () {
    let valueList = document.getElementsByName("flaw_pElement");

    paramFlawCheckROI.Set(parseFloat(valueList[0].value));
    paramFlawPixelRate.Set(parseFloat(valueList[1].value));
    paramFlawSlideX.Set(parseFloat(valueList[2].value));
    paramFlawSlideY.Set(parseFloat(valueList[3].value));
    paramFlawSlideZ.Set(parseFloat(valueList[4].value));
    paramFlawScoreTh.Set(parseFloat(valueList[5].value));
    paramFlawFlawTh.Set(parseFloat(valueList[6].value));

});

/*========================================================*/
/*
    flaw test button
 */
/*--------------------------------------------------------*/

document.getElementsByName("flaw_tButtion")[0].addEventListener("click", function () {
    Call_ArmControl(flaw_pHome);
    console.log("Call Home");
});

document.getElementsByName("flaw_tButtion")[1].addEventListener("click", function () {
    Call_ArmControl(flaw_pCenter);
    console.log("Call Center");
});

document.getElementsByName("flaw_tButtion")[2].addEventListener("click", function () {
    Call_ArmControl(flaw_pSuction);
    console.log("Call Scuction");
});

document.getElementsByName("flaw_tButtion")[3].addEventListener("click", function () {
    Call_ArmControl(flaw_pFlaw);
    console.log("Call Flaw");
});

document.getElementsByName("flaw_tButtion")[4].addEventListener("click", function () {
    Call_ArmControl(flaw_pNFlaw);
    console.log("Call NFlaw");
});

/*========================================================*/
/*========================================================*/

/*========================================================*/
/*
    air tool
 */
/*--------------------------------------------------------*/

document.getElementById("air_Init").addEventListener("click", function () {
    var msg = new ROSLIB.Message({
        data: 0
    });
    topicAirState.Pub(msg);
});

document.getElementById("air_Start").addEventListener("click", function () {
    var msg = new ROSLIB.Message({
        data: true
    });
    topicAirStart.Pub(msg);
});

document.getElementById("air_Stop").addEventListener("click", function () {
    var msg = new ROSLIB.Message({
        data: false
    });
    topicAirStart.Pub(msg);
});

/*========================================================*/
/*
    air save
 */
/*--------------------------------------------------------*/

function Pub_Air_Save() {
    let msg = new ROSLIB.Message({
        data: true
    });
    topicAirSave.Pub(msg);
}

document.getElementById("air_paramSave").addEventListener("click", function () {
    Pub_Air_Save();
    console.log('save');
});

document.getElementById("air_paramSet").addEventListener("click", function () {
    let valueList = document.getElementsByName("air_pElement");

    air_roll.Head = parseFloat(valueList[0].value);
    air_roll.Front = parseFloat(valueList[1].value);
    air_roll.LeftWing = parseFloat(valueList[2].value);
    air_roll.RightWing = parseFloat(valueList[3].value);
    air_roll.Rear = parseFloat(valueList[4].value);
    air_roll.Tail = parseFloat(valueList[5].value);

    paramAirRollObject.Set(air_roll);
    paramAirCheckROI.Set(parseFloat(valueList[6].value));
    paramAirPixelRate.Set(parseFloat(valueList[7].value));
    paramAirScoreTh.Set(parseFloat(valueList[8].value));

    air_suctionZ.Head = parseFloat(valueList[9].value);
    air_suctionZ.Front = parseFloat(valueList[10].value);
    air_suctionZ.LeftWing = parseFloat(valueList[11].value);
    air_suctionZ.RightWing = parseFloat(valueList[12].value);
    air_suctionZ.Rear = parseFloat(valueList[13].value);
    air_suctionZ.Tail = parseFloat(valueList[14].value);

    paramAirSucctionZ.Set(air_suctionZ);
});

/*========================================================*/
/*
    air test button
 */
/*--------------------------------------------------------*/

document.getElementsByName("air_tButtion")[0].addEventListener("click", function () {
    Call_ArmControl(air_pHome);
    console.log("Call Home");
});

document.getElementsByName("air_tButtion")[1].addEventListener("click", function () {
    Call_ArmControl(air_pCenter);
    console.log("Call Center");
});

document.getElementsByName("air_tButtion")[2].addEventListener("click", function () {
    Call_ArmControl(air_pCamRight);
    console.log("Call camRight");
});

document.getElementsByName("air_tButtion")[3].addEventListener("click", function () {
    Call_ArmControl(air_pCamLeft);
    console.log("Call CamLeft");
});

document.getElementsByName("air_tButtion")[4].addEventListener("click", function () {
    Call_ArmControl(air_pSuction);
    console.log("Call Suction");
});

document.getElementsByName("air_tButtion")[5].addEventListener("click", function () {
    Call_ArmControl(air_pHead);
    console.log("Call Head");
});

document.getElementsByName("air_tButtion")[6].addEventListener("click", function () {
    Call_ArmControl(air_pFront);
    console.log("Call Front");
});

document.getElementsByName("air_tButtion")[7].addEventListener("click", function () {
    Call_ArmControl(air_pLeftWing);
    console.log("Call LeftWing");
});

document.getElementsByName("air_tButtion")[8].addEventListener("click", function () {
    Call_ArmControl(air_pRightWing);
    console.log("Call RightWing");
});

document.getElementsByName("air_tButtion")[9].addEventListener("click", function () {
    Call_ArmControl(air_pRear);
    console.log("Call Rear");
});

document.getElementsByName("air_tButtion")[10].addEventListener("click", function () {
    Call_ArmControl(air_pTail);
    console.log("Call Tail");
});