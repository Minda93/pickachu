function NewMotion()
{
  var num=document.getElementById('MotionTable').getElementsByTagName('div').length+1;
  var div=document.createElement('div');

  //div.id='M_'+num;
  for (var i = 1; i <= 2; i++) 
  {
    var input=document.createElement('input');
    input.type='text';
    //input.id='M_' + num + '_' + i;
    input.className='textbox';
    input.value=-1;
    div.appendChild(input);
  }
  for (var i = 1; i <= 40 ; i++) 
  {     
    if (i%2==1) 
    {
      var input=document.createElement('input');
      input.type='text';
      //input.id='MotionList_'+num+'_'+(i+1)/2;
      input.className='textbox';
      input.value=0;
      div.appendChild(input);
      
    }  
    if (i%2==0) 
    {
      var input=document.createElement('input');
      input.type='text';
      //input.id='Delay_'+num+'_'+i/2;
      input.className='textbox';
      input.value=0;
      div.appendChild(input);
    }
  }
  document.getElementById('MotionTable').appendChild(div);
  //for ( var i=1; i<=42 ;i++)
  //{
  //  document.getElementById('M_' + num).getElementsByClassName('textbox')[i-1].onchange = function() {changemotion()};
  //}
}
function DeleteMotion()
{
  var num=document.getElementById('MotionTable').getElementsByTagName('div').length;
  document.getElementById('MotionTable').removeChild(document.getElementById('MotionTable').getElementsByTagName('div')[num-1]);
}
function NewRelativePosition()
{
  var num=document.getElementById('RelativePositionTable').getElementsByTagName('div').length+1;
  var div=document.createElement('div');
  for (var i = 1; i <= 2 ; i++)
  {
    //div.id='P_'+num;
    var input=document.createElement('input');
    input.type='text';
    //input.id='P_' + num + '_' +i;
    input.className='textbox';
    input.value=-1;
    div.appendChild(input);
  } 
  for (var i = 1; i <= 21 ; i++) 
  {
    var input=document.createElement('input');
    input.type='text';
    //input.id='Position_'+num+'_'+i;
    input.className='textbox';
    input.value=0;
    div.appendChild(input);
  }  
  document.getElementById('RelativePositionTable').appendChild(div);
  //for ( var i = 1; i<=23; i++)
  //{
  //  document.getElementById('P_' + num).getElementsByClassName('textbox')[i-1].onchange = function() {changeposition()};
  //}
}
function NewRelativeSpeed()
{
  var num=document.getElementById('RelativeSpeedTable').getElementsByTagName('div').length+1;
  var div=document.createElement('div');  
  for (var i = 1; i <= 2; i++) 
  {
    //div.id='S_'+num;
    var input=document.createElement('input');
    input.type='text';
    //input.id='S_'+num+'_'+i;
    input.className='textbox';
    input.value=0;
    div.appendChild(input);
  }  
  for (var i = 1; i <= 21; i++) 
  {
    var input=document.createElement('input');
    input.type='text';
    //input.id='Speed_'+num+'_'+i;
    input.className='textbox';
    input.value=0;
    div.appendChild(input);
  }
  document.getElementById('RelativeSpeedTable').appendChild(div);
}
function NewAbsolutePosition()
{
  var num=document.getElementById('AbsolutePositionTable').getElementsByTagName('div').length+1;
  var div=document.createElement('div');
  for (var i = 1; i <= 2 ; i++)
  {
    //div.id='P_'+num;
    var input=document.createElement('input');
    input.type='text';
    //input.id='P_' + num + '_' +i;
    input.className='textbox';
    input.value=-1;
    div.appendChild(input);
  } 
  for (var i = 1; i <= 21 ; i++) 
  {
    var input=document.createElement('input');
    input.type='text';
    //input.id='Position_'+num+'_'+i;
    input.className='textbox';
    input.value=0;
    div.appendChild(input);
  }  
  document.getElementById('AbsolutePositionTable').appendChild(div);
  //for ( var i = 1; i<=23; i++)
  //{
  //  document.getElementById('P_' + num).getElementsByClassName('textbox')[i-1].onchange = function() {changeposition()};
  //}
}
function NewAbsoluteSpeed()
{
  var num=document.getElementById('AbsoluteSpeedTable').getElementsByTagName('div').length+1;
  var div=document.createElement('div');  
  for (var i = 1; i <= 2; i++) 
  {
    //div.id='S_'+num;
    var input=document.createElement('input');
    input.type='text';
    //input.id='S_'+num+'_'+i;
    input.className='textbox';
    input.value=0;
    div.appendChild(input);
  }  
  for (var i = 1; i <= 21; i++) 
  {
    var input=document.createElement('input');
    input.type='text';
    //input.id='Speed_'+num+'_'+i;
    input.className='textbox';
    input.value=0;
    div.appendChild(input);
  }
  document.getElementById('AbsoluteSpeedTable').appendChild(div);
}
function New()
{
  if(document.getElementById("MotionList").style.display == "initial")
  {
    NewMotion();
  }
  else if(document.getElementById("RelativeAngle").style.display == "initial" || document.getElementById("RelativeSpeed").style.display ==  "initial")
  {
    NewRelativePosition();
    NewRelativeSpeed();
  }
  else if(document.getElementById("AbsoluteAngle").style.display == "initial" || document.getElementById("AbsoluteSpeed").style.display ==  "initial")
  {
    NewAbsolutePosition();
    NewAbsoluteSpeed();
  }
}
function DeleteNew()
{
  if(document.getElementById("MotionList").style.display == "initial")
  {
    DeleteMotion()
  }
  else if(document.getElementById("RelativeAngle").style.display == "initial" || document.getElementById("RelativeSpeed").style.display ==  "initial")
  {
    var num=document.getElementById('RelativePositionTable').getElementsByTagName('div').length;
    document.getElementById('RelativePositionTable').removeChild(document.getElementById('RelativePositionTable').getElementsByTagName('div')[num-1]);
    var num=document.getElementById('RelativeSpeedTable').getElementsByTagName('div').length;
    document.getElementById('RelativeSpeedTable').removeChild(document.getElementById('RelativeSpeedTable').getElementsByTagName('div')[num-1]);
  }
  else if(document.getElementById("AbsoluteAngle").style.display == "initial" || document.getElementById("AbsoluteSpeed").style.display ==  "initial")
  {
    var num=document.getElementById('AbsolutePositionTable').getElementsByTagName('div').length;
    document.getElementById('AbsolutePositionTable').removeChild(document.getElementById('AbsolutePositionTable').getElementsByTagName('div')[num-1]);
    var num=document.getElementById('AbsoluteSpeedTable').getElementsByTagName('div').length;
    document.getElementById('AbsoluteSpeedTable').removeChild(document.getElementById('AbsoluteSpeedTable').getElementsByTagName('div')[num-1]);
  }
}
function MotionList(mode)
{
  switch(Number(mode))
  {
    case 0:
      document.getElementById("MotionList").style.display = "initial";
      document.getElementById("RelativeAngle").style.display = "none";
      document.getElementById("RelativeSpeed").style.display = "none";
      document.getElementById("AbsoluteAngle").style.display = "none";
      document.getElementById("AbsoluteSpeed").style.display = "none";
      break;
    case 1:
      document.getElementById("MotionList").style.display = "none";
      document.getElementById("RelativeAngle").style.display = "initial";
      document.getElementById("RelativeSpeed").style.display = "none";
      document.getElementById("AbsoluteAngle").style.display = "none";
      document.getElementById("AbsoluteSpeed").style.display = "none";
      break;
    case 2:
      document.getElementById("MotionList").style.display = "none";
      document.getElementById("RelativeAngle").style.display = "none";
      document.getElementById("RelativeSpeed").style.display = "initial";
      document.getElementById("AbsoluteAngle").style.display = "none";
      document.getElementById("AbsoluteSpeed").style.display = "none";
      break;
    case 3:
      document.getElementById("MotionList").style.display = "none";
      document.getElementById("RelativeAngle").style.display = "none";
      document.getElementById("RelativeSpeed").style.display = "none";
      document.getElementById("AbsoluteAngle").style.display = "initial";
      document.getElementById("AbsoluteSpeed").style.display = "none";
      break;
    case 4:
      document.getElementById("MotionList").style.display = "none";
      document.getElementById("RelativeAngle").style.display = "none";
      document.getElementById("RelativeSpeed").style.display = "none";
      document.getElementById("AbsoluteAngle").style.display = "none";
      document.getElementById("AbsoluteSpeed").style.display = "initial";
      break;
    }
}