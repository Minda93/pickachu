

const Call_ArmControl = async (pos_) => {
    try {
        console.log(pos_);
        if(isBusy == false){
            var request = new ROSLIB.ServiceRequest({
                cmd: 'p2p',
                pos: pos_.pos,
                euler: pos_.euler
            }); 
            const control = await serviceControl.Call(request);

            console.log(control.success);
        }
    } catch (err) {
        console.log(err);
    }
};