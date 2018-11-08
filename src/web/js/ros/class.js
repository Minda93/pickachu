/* 
Vision1.subscribe(function(msg) {
    return msg.data
}); 
*/

class RosTopic {
    constructor(rosConnect, name, type) {
        this.object = new ROSLIB.Topic({
            ros: rosConnect,
            name: name,
            messageType: type
        });
    }

    Pub(msg) {
        this.object.publish(msg);
    }

    Sub(){
        var _this = this;
        return new Promise(function(resolve) {
            _this.object.subscribe(function (msg) {
                resolve(msg);
            });
        });
    }
}
// =======================================================================
var delay = function (s) {
    return new Promise(function (resolve, reject) {
        setTimeout(resolve, s);
    });
};
class RosParam {
    constructor(rosConnect, name) {
        this.object = new ROSLIB.Param({
            ros: rosConnect,
            name: name,
        });
    }

    Set(value) {
        this.object.set(value);
    }

    Get() {
        var _this = this;
        return new Promise(function(resolve) {
            _this.object.get(function (value) {
                resolve(value);
            });
        }); 
    }
}
// =======================================================================
/* 
var request = new ROSLIB.ServiceRequest({
    receive: 1
}); 
*/

class RosService {
    constructor(rosConnect, name, type) {
        this.object = new ROSLIB.Service({
            ros: rosConnect,
            name: name,
            serviceType: type
        });
    }

    Call(request) {
        var _this = this;
        return new Promise(function(resolve) {
            _this.object.callService(request, function (res) {
                resolve(res);
            });
        }); 
    }
}