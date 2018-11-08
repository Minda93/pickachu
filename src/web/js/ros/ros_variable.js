
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

var topicCmdString = new RosTopic(ros, '/accupick3d/cmdString', '/std_msgs/String');
var topicMsgString = new RosTopic(ros, '/accupick3d/msgString', '/std_msgs/String')

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
var paramGomokupButton= new RosParam(ros, '/accupick3d/gomoku/pButton');



// =======================================================================
/* 
 * ros service
 */
/*--------------------------------------------------------*/

// var serviceLogin = new RosService(ros,'cloud_web/login','login');
