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


// =======================================================================
/* 
 * ros param
 */
/*--------------------------------------------------------*/

var paramGomoku = new RosParam(ros, '/accupick3d/gomoku');
var paramGomokupHome = new RosParam(ros, '/accupick3d/gomoku/pHome');
var paramGomokupChess = new RosParam(ros, '/accupick3d/gomoku/pChess');
var paramGomokupBoardCenter = new RosParam(ros, '/accupick3d/gomoku/pBoardCenter');
var paramGomokupBoard = new RosParam(ros, '/accupick3d/gomoku/pBoard');
var paramGomokupButton = new RosParam(ros, '/accupick3d/gomoku/pButton');
var paramGomokuErrorHeight = new RosParam(ros, '/accupick3d/gomoku/error_height');

// =======================================================================
/* 
 * ros service
 */
/*--------------------------------------------------------*/

var serviceControl = new RosService(ros, '/accupick3d/arm_contol', 'armCmd');