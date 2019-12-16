#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from sensor_msgs.msg import CameraInfo
from geometry_msgs.msg import Twist
import XBee_Threaded
from time import sleep
from math import exp
print 'Turn on the bots'
print 'Enter port  number /dev/ttyUSB'
st="/dev/ttyUSB"
port = raw_input()
xbee = XBee_Threaded.XBee(st+port)
print "connected"
r = 50.760/1000 # metres
R = 150.000/1000 # metres
wz = 0.5 #rps
w1b1 = 0
w2b1 = 0
w3b1 = 0
w1b2 = 0
w2b2 = 0
w3b2 = 0
w1b3 = 0
w2b3 = 0
w3b3 = 0
w1b4 = 0
w2b4 = 0
w3b4 = 0
d1 = 0
d2 = 0
d3 = 0
d4 = 0
k1 = 0
k2 = 0
k3 = 0
k4 = 0

t_flag = 0
t = 0
t0 = 0
t1 = 0
t2 = 0
t3 = 0
state1 = [0,0,0]
state2 = [0,0,0]
state3 = [0,0,0]
state4 = [0,0,0]

count1 = [0,0,0]
count2 = [0,0,0]
count3 = [0,0,0]
count4 = [0,0,0]



   
def torque_encode(w1,w2,w3,state,count):
    '''
    w1,w2,w3 = target pwm(-255,255)
    state = list of states of motors(0 = stopped, 1 = motors started)
    count = list of number of frames that max pwm has been given
    cnt = number of frames for max pwm before target pwm is sent
    thresh = pwm threshold for detecting change
    '''
    thresh = 10
    cnt = 20
    [state1,state2,state3] = state
    [count1, count2, count3] = count
    if abs(w1) > thresh:
        if state1 == 0 or count1<cnt:
            state1 = 1
            if w1 > 0:
                w1 = 255
            else :
                w1 = -255
            count1 += 1
    else:
        state1 = 0
        count1 = 0
    
    if abs(w2) > thresh:
        if state2 == 0 or count2<cnt:
            state2 = 1
            if w2 > 0:
                w2 = 255
            else :
                w2 = -255
            count2 += 1
    else:
        state2 = 0
        count2 = 0
   

    if abs(w3) > thresh:
        if state3 == 0 or count3<cnt:
            state3 = 1
            if w3 > 0:
                w3 = 255
            else :
                w3 = -255
            count3 += 1
    else:
        state3 = 0
        count3 = 0
   
    state = [state1,state2,state3]
    count = [count1, count2, count3]
    return w1,w2,w3,state,count

def encode(w1,w2,w3):
    '''
    remaps from (-255,255) to (0,255)
    '''
    w1 = (w1+255)/2
    w2 = (w2+255)/2
    w3 = (w3+255)/2
    w1 = int(w1)
    w2 = int(w2)
    w3 = int(w3)
    return w1,w2,w3

def invk(tw):
    '''
    applies ik given vx,vy,omega
    Returns w1,w1 w3
    '''
    sl = 19.0
    intercept = 160.0
    vx = tw.linear.x
    vy = tw.linear.y
    wz = tw.angular.z
    w1 = ((vx/1.732)/r) - ((vy/3)/r) + ((wz*R)/r)
    w2 = ((vy/1.5)/r) + ((R*wz)/r)
    w3 = ((wz*R)/r) - ((vx/1.732)/r) - ((vy/3)/r)
        
    w1 = int(127*w1)
    w2 = int(127*w2)
    w3 = int(127*w3)
    w1 *= 255.0/100.0
    w2 *= 255.0/100.0
    w3 *= 255.0/100.0

    if w1 >255:
    	w1 = 255
    if w2 > 255:
        w2 = 255
    if w3 >255:
        w3 = 255

    if w1 <-255:
        w1 = -255
    if w2 < -255:
        w2 < -255
    if w3 < -255:
        w3 = -255
    if w1 > 0:	
        w1 = w1*sl/51.0 + intercept
    if w2 > 0:	
        w2 = w2*sl/51.0 + intercept
    if w3 > 0:	
        w3 = w3*sl/51.0 + intercept
    if w1 < 0:	
    	w1 = w1*sl/51.0 - intercept
    if w2 < 0:	
    	w2 = w2*sl/51.0 - intercept
    if w3 < 0:	
        w3 = w3*sl/51.0 - intercept
    w1 = int(w1)
    w2 = int(w2)
    w3 = int(w3)

    if w1 >255:
    	w1 = 255
    if w2 > 255:
    	w2 = 255
    if w3 >255:
     	w3 = 255

    if w1 <-255:
    	w1 = -255
    if w2 < -255:
    	w2 < -255
    if w3 < -255:
    	w3 = -255
    return w1,w2,w3

def b1t(msg):
    global w1b1
    global w2b1
    global w3b1
    global state1
    global count1
    w1b1,w2b1,w3b1 = invk(msg)
    #w1b1,w2b1,w3b1,state1,count1 = torque_encode(w1b1,w2b1,w3b1,state1,count1)
    w1b1,w2b1,w3b1 = encode(w1b1,w2b1,w3b1)
    return 0

def b2t(msg):
    global w1b2
    global w2b2
    global w3b2
    global state2
    global count2
    w1b2,w2b2,w3b2 = invk(msg)
    #w1b2,w2b2,w3b2,state2,count2 = torque_encode(w1b2,w2b2,w3b2, state2,count2)
    w1b2,w2b2,w3b2 = encode(w1b2,w2b2,w3b2)
    return 0

def b3t(msg):
    global w1b3
    global w2b3
    global w3b3
    global state3
    global count3
    w1b3,w2b3,w3b3 = invk(msg)
    #w1b3,w2b3,w3b3,state3,count3 = torque_encode(w1b3,w2b3,w3b3,state3,count3)
    w1b3,w2b3,w3b3 = encode(w1b3,w2b3,w3b3)
    return 0

def b4t(msg):
    global w1b4
    global w2b4
    global w3b4
    global state4
    global count4
    state4
    w1b4,w2b4,w3b4 = invk(msg)
    #w1b4,w2b4,w3b4,state4,count4 = torque_encode(w1b4,w2b4,w3b4,state4,count4)
    w1b4,w2b4,w3b4 = encode(w1b4,w2b4,w3b4)
    return 0

def b1d(msg):
    global d1
    d1 = msg.data
    return 0

def b2d(msg):
    global d2
    d2 = msg.data
    return 0

def b3d(msg):
    global d3
    d3 = msg.data
    return 0

def b4d(msg):
    global d4
    d4 = msg.data
    return 0

def b1k(msg):
    global k1
    k1 = msg.data
    return 0

def b2k(msg):
    global k2
    k2 = msg.data
    return 0

def b3k(msg):
    global k3
    k3 = msg.data
    return 0

def b4k(msg):
    global k4
    k4 = msg.data
    return 0

def run():
    global w1b1
    global w2b1
    global w3b1
    global w1b2
    global w2b2
    global w3b2
    global w1b3
    global w2b3
    global w3b3
    global w1b4
    global w2b4
    global w3b4
    global d1
    global d2
    global d3
    global d4
    global k1
    global k2
    global k3
    global k4
    rospy.init_node('listener', anonymous=True)
    rate = rospy.Rate(10)
    rospy.Subscriber("bot1twist", Twist, b1t)
    rospy.Subscriber("bot2twist", Twist, b2t)
    rospy.Subscriber("bot3twist", Twist, b3t)
    rospy.Subscriber("bot4twist", Twist, b4t)
    rospy.Subscriber("bot1d", Int32, b1d)
    rospy.Subscriber("bot2d", Int32, b2d)
    rospy.Subscriber("bot3d", Int32, b3d)
    rospy.Subscriber("bot4d", Int32, b4d)
    rospy.Subscriber("bot1k", Int32, b1k)
    rospy.Subscriber("bot2k", Int32, b2k)
    rospy.Subscriber("bot3k", Int32, b3k)
    rospy.Subscriber("bot4k", Int32, b4k)
    while(True):
        '''
        Creates packet for sending commands to bot
        '''
        s1= str(w1b1) + ':' + str(w2b1) + ':' + str(w3b1) +':'+str(d1) +':'+str(k1) +':'
        s2= str(w1b2) + ':' + str(w2b2) + ':' + str(w3b2) +':'+str(d2) +':'+str(k2) +':'
        s3= str(w1b3) + ':' + str(w2b3) + ':' + str(w3b3) +':'+str(d3) +':'+str(k3) +':'
        s4= str(w1b4) + ':' + str(w2b4) + ':' + str(w3b4) +':'+str(d4) +':'+str(k4) +':'
        print 's1',s1
        s = s1+s2+s3+s4
        print 's2',s2
        print 's3',s3
        print 's4',s4
        sent = xbee.SendStr(s.encode())    
        rate.sleep()


if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException:
        pass