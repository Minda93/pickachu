// =======================================================================
/*  ros topic  

    Rostopic(connect, name, type)
        connect: ros 連到的IP 
            ex: connect = new ROSLIB.Ros({ursl:'ws://127.0.0.1:9090'});
        name: ros topic name 
        type: ros topic messageType

        function 
            pub(msg): ros topic publish
                msg: roslib message (根據type不同 內容會改變)
                    ex: var msg = new ROSLIB.Message({
                            data: value
                        });
            一直監聽(目前辦法)
                宣告變數名稱.object.subscribe(function(msg) {});
                msg: roslib message (根據type不同 內容會改變)
                    ex: start.object.subscribe(function(msg){return msg.data});

*/
var isBusy = false;
var topicCmdString = new RosTopic(ros, '/accupick3d/cmdString', '/std_msgs/String');
var topicMsgString = new RosTopic(ros, '/accupick3d/msgString', '/std_msgs/String');
var topicIsBusy = new RosTopic(ros, '/accupick3d/is_busy', '/std_msgs/Bool');

// gomoku
var topicGomokuSave = new RosTopic(ros, '/gomoku/save', '/std_msgs/Bool');
var topicGomokuStart = new RosTopic(ros, '/gomoku/start', '/std_msgs/Bool');
var topicGomokuSide = new RosTopic(ros, '/gomoku/decide_side', '/std_msgs/Int32');
var topicGomokuState = new RosTopic(ros, '/gomoku/behavior_state', '/std_msgs/Int32');


// flaw
var topicFlawSave = new RosTopic(ros, '/flaw_detection/save', '/std_msgs/Bool');
var topicFlawStart = new RosTopic(ros, '/flaw_detection/start', '/std_msgs/Bool');
var topicFlawState = new RosTopic(ros, '/flaw_detection/behavior_state', '/std_msgs/Int32');

// air
var topicAirSave = new RosTopic(ros, '/aircraft/save', '/std_msgs/Bool');
var topicAirStart = new RosTopic(ros, '/aircraft/start', '/std_msgs/Bool');
var topicAirState = new RosTopic(ros, '/aircraft/behavior_state', '/std_msgs/Int32');

// =======================================================================
/* 
 * ros param
 */
/*--------------------------------------------------------*/

/* gomoku point */
var paramGomoku = new RosParam(ros, '/accupick3d/gomoku');
var paramGomokupHome = new RosParam(ros, '/accupick3d/gomoku/pHome');
var paramGomokupChess = new RosParam(ros, '/accupick3d/gomoku/pChess');
var paramGomokupBoardCenter = new RosParam(ros, '/accupick3d/gomoku/pBoardCenter');
var paramGomokupBoard = new RosParam(ros, '/accupick3d/gomoku/pBoard');
var paramGomokupButton = new RosParam(ros, '/accupick3d/gomoku/pButton');
/* gomoku param */
var paramGomokuErrorHeight = new RosParam(ros, '/accupick3d/gomoku/error_height');

/* flaw point */
var paramFlaw = new RosParam(ros, '/accupick3d/flaw_detection');
var paramFlawpHome = new RosParam(ros, '/accupick3d/flaw_detection/pHome');
var paramFlawpCenter = new RosParam(ros, '/accupick3d/flaw_detection/pCenter');
var paramFlawpSuction = new RosParam(ros, '/accupick3d/flaw_detection/pSuction');
var paramFlawpFlaw = new RosParam(ros, '/accupick3d/flaw_detection/pFlaw');
var paramFlawpNFlaw = new RosParam(ros, '/accupick3d/flaw_detection/pNFlaw');
/* flaw param */
var paramFlawCheckROI = new RosParam(ros, '/accupick3d/flaw_detection/checkROI');
var paramFlawPixelRate = new RosParam(ros, '/accupick3d/flaw_detection/pixelRate');
var paramFlawSlideX = new RosParam(ros, '/accupick3d/flaw_detection/slideX');
var paramFlawSlideY = new RosParam(ros, '/accupick3d/flaw_detection/slideY');
var paramFlawSlideZ = new RosParam(ros, '/accupick3d/flaw_detection/slideZ');
var paramFlawScoreTh = new RosParam(ros, '/accupick3d/flaw_detection/score_threshold');
var paramFlawFlawTh = new RosParam(ros, '/accupick3d/flaw_detection/flaw_threshold');

/* air point */
var paramAir = new RosParam(ros, '/accupick3d/aircraft');
var paramAirpHome = new RosParam(ros, 'accupick3d/aircraft/pHome');
var paramAirpCenter = new RosParam(ros, 'accupick3d/aircraft/pCenter');
var paramAirpCamRight = new RosParam(ros, 'accupick3d/aircraft/pCamRight');
var paramAirpCamLeft = new RosParam(ros, 'accupick3d/aircraft/pCamLeft');
var paramAirpSuction = new RosParam(ros, 'accupick3d/aircraft/pSuction');
var paramAirpHead = new RosParam(ros, 'accupick3d/aircraft/pHead');
var paramAirpFront = new RosParam(ros, 'accupick3d/aircraft/pFront');
var paramAirpLeftWing = new RosParam(ros, 'accupick3d/aircraft/pLeftWing');
var paramAirpRightWing = new RosParam(ros, 'accupick3d/aircraft/pRightWing');
var paramAirpRear = new RosParam(ros, 'accupick3d/aircraft/pRear');
var paramAirpTail = new RosParam(ros, 'accupick3d/aircraft/pTail');

/* air param */
var paramAirRollObject = new RosParam(ros, '/accupick3d/aircraft/rollObject');
var paramAirCheckROI = new RosParam(ros, '/accupick3d/aircraft/checkROI');
var paramAirPixelRate = new RosParam(ros, '/accupick3d/aircraft/pixelRate');
var paramAirScoreTh = new RosParam(ros, '/accupick3d/aircraft/score_threshold');
var paramAirSucctionZ = new RosParam(ros, '/accupick3d/aircraft/suctionZ');

// =======================================================================
/* 
 * ros service
 */
/*--------------------------------------------------------*/

var serviceControl = new RosService(ros, '/accupick3d/arm_contol', 'armCmd');