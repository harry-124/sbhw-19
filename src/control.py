#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
import math as m
from geometry_msgs.msg import Pose
from sbhw.msg import mov

bmov1 = mov()
bmov2 = mov()
bmov3 = mov()
bmov4 = mov()
bp1 = Pose()
bp2 = Pose()
bp3 = Pose()
bp4 = Pose()
reached = [0,0,0,0]

def b1p(msg):
    global bp1
    bp1 = msg
    return 0

def b2p(msg):
    global bp2
    bp2 = msg
    return 0

def b3p(msg):
    global bp3
    bp3 = msg
    return 0

def b4p(msg):
    global bp4
    bp4 = msg
    return 0

def mb1(msg):
    global bmov1
    global reached
    reached[0] = 0
    bmov1 = msg
    return 0

def mb2(msg):
    global bmov2
    global reached
    reached[1] = 0
    bmov2 = msg
    return 0

def mb3(msg):
    global bmov3
    global reached
    reached[2] = 0
    bmov3 = msg
    return 0

def mb4(msg):
    global bmov4
    global reached
    reached[3] = 0
    bmov4 = msg
    return 0

def pid(bp,bmov,bn):
    global reached
    tw = Twist()
    xtg = bmov.x
    ytg = bmov.y
    kpr = 0.1
    thetap = bmov.thetap
    x = bp.position.x
    y = bp.position.y
    z = bp.orientation.z
    theta = 2*m.atan(z)
    print 'togo',xtg,ytg,'at',x,y
    if x == xtg and y == ytg:
        tw.linear.x = 0
        tw.linear.y = 0
        reached[bn] = 1
    else:
        ex = xtg - x
        ey = ytg - y
        if (abs(bmov.thetap-theta)>0.1 and bmov.thetap <= 6.28 and bmov.thetap >= 0):
            if(abs(bmov.thetap-theta)<(6.28-abs(bmov.thetap-theta))):
                f = (bmov.thetap-theta)/abs(bmov.thetap-theta)
                e = abs(bmov.thetap-theta)
                thetad = (e*kpr)*(f)
            else:
                f = (bmov.thetap-theta)/abs(bmov.thetap-theta)
                e = 6.28 - abs(bmov.thetap-theta)
                thetad = -((e*kpr))*(f)        
        else:
            thetad = 0
        vx = ex
        vy = ey
        norm = vx**2 + vy**2
        norm = m.sqrt(norm)
        vx = vx/norm
        vy = vy/norm
        norm = m.sqrt(norm)/10
        if norm > 1:
            norm = 1
        vx = 0.06*vx*norm
        vy = 0.06*vy*norm
        tw.linear.x = vx
        tw.linear.y = vy
        tw.angular.z = thetad
    return tw

def velcmd(bp,bmov):
    kpr = 0.1
    tw = Twist()
    tw.linear.x = bmov.mag*m.cos(bmov.thetav)/0.06
    tw.linear.y = bmov.mag*m.sin(bmov.thetav)/0.06
    print tw.linear.x,tw.linear.y
    x = bp.position.x
    y = bp.position.y
    z = bp.orientation.z
    theta = 2*m.atan(z)
    if (abs(bmov.thetap-theta)>0.1 and bmov.thetap <= 6.28 and bmov.thetap >= 0):
        if(abs(bmov.thetap-theta)<(6.28-abs(bmov.thetap-theta))):
            f = (bmov.thetap-theta)/abs(bmov.thetap-theta)
            e = abs(bmov.thetap-theta)
            thetad = (e*kpr)*(f)
        else:
            f = (bmov.thetap-theta)/abs(bmov.thetap-theta)
            e = 6.28 - abs(bmov.thetap-theta)
            thetad = -((e*kpr))*(f)        
    else:
        thetad = 0
        print tw.linear.x , tw.linear.y
    tw.angular.z = thetad
    return tw
        

def run():
    global reached
    global bmov1
    global bmov2
    global bmov3
    global bmov4
    global bp1
    global bp2
    global bp3
    global bp4

    rospy.init_node('controller', anonymous=True)
    rate = rospy.Rate(60)
    rospy.Subscriber("bot1pose", Pose, b1p)
    rospy.Subscriber("bot2pose", Pose, b2p)
    rospy.Subscriber("bot3pose", Pose, b3p)
    rospy.Subscriber("bot4pose", Pose, b4p)
    rospy.Subscriber("bot1mov",mov,mb1)
    #rospy.Subscriber("bot2mov",mov,mb2)
    rospy.Subscriber("bot3mov",mov,mb3)
    rospy.Subscriber("bot4mov",mov,mb4)
    pubv1 = rospy.Publisher('bot1twistglobal',Twist,queue_size = 10)
    #pubv2 = rospy.Publisher('bot2twistglobal',Twist,queue_size = 10)
    pubv3 = rospy.Publisher('bot3twistglobal',Twist,queue_size = 10)
    pubv4= rospy.Publisher('bot4twistglobal',Twist,queue_size = 10)
    while(True):
        if reached[0]==0 and bmov1.mode == 1:
            tw1 = pid(bp1,bmov1,0)
            bmov1.mode = 0
            pubv1.publish(tw1)
        """if reached[1]==0 and bmov2.mode == 1:
            tw2 = pid(bp2,bmov2,1)
            bmov2.mode = 0
            pubv2.publish(tw2)
        elif bmov2.mode == 2:
            print 'nadakkudhu'
            twc = velcmd(bp2,bmov2)
            bmov2.mode = 0
            pubv2.publish(twc)"""
        if reached[2]==0 and bmov3.mode == 1:
            tw3 = pid(bp3,bmov3,2)
            bmov3.mode = 0
            pubv3.publish(tw3)
        if reached[3]==0 and bmov4.mode == 1:
            tw4 = pid(bp4,bmov4,3)
            bmov4.mode = 0
            pubv4.publish(tw4)
        rate.sleep()
        

if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException:
        pass