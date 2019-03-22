<h1> Hardware interface of Soccerbots </h1>

<h2> Nodes and their utilities </h2><br>
* xbeebotsend.py -> commucicates from base xbee to all the robots. Does message frame generation, message encoding, converts local vx,vy and wz into w1,w2,w3 (inverse kinematics).<br>  
* globtoloc.py -> converts global twist messages to local twist messages for robot by using camera feedback. <br>  
* control.py -> control for go to goal based planning, vectory trajectory planning to be added soon.  <br>
* joystick.py -> egacy joystick for direct global velocity commands (control.py must not be run along with it)<br>