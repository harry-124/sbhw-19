#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
import math as m
from geometry_msgs.msg import Pose
b1sin = 0
b1cos = 1
b2sin = 0
b2cos = 1
b3sin = 0
b3cos = 1
b4sin = 0
b4cos = 1
b1lt = Twist()
b2lt = Twist()
b3lt = Twist()
b4lt = Twist() 

def b1t(msg):
    global b1sin
    global b1cos
    global b1lt
    vx = -msg.linear.x
    vy = -msg.linear.y
    b1lt.linear.x = vx*b1cos + vy*b1sin
    b1lt.linear.y = -vx*b1sin + vy*b1cos
    b1lt.angular.z = msg.angular.z
    return 0

def b2t(msg):
    global b2sin
    global b2cos
    global b1lt
    vx = -msg.linear.x
    vy = -msg.linear.y
    b2lt.linear.x = vx*b2cos + vy*b2sin
    b2lt.linear.y = -vx*b2sin + vy*b2cos
    b2lt.angular.z = msg.angular.z
    return 0

def b3t(msg):
    global b3sin
    global b3cos
    global b1lt
    vx = -msg.linear.x
    vy = -msg.linear.y
    b3lt.linear.x = vx*b3cos + vy*b3sin
    b3lt.linear.y = -vx*b3sin + vy*b3cos
    b3lt.angular.z = msg.angular.z
    return 0

def b4t(msg):
    global b4sin
    global b4cos
    global b1lt
    vx = -msg.linear.x
    vy = -msg.linear.y
    b4lt.linear.x = vx*b4cos + vy*b4sin
    b4lt.linear.y = -vx*b4sin + vy*b4cos
    b4lt.angular.z = msg.angular.z
    return 0

def b1p(msg):
    global b1sin
    global b1cos
    qz = msg.orientation.z
    yaw = 2*m.atan(qz)
    print('bot1',yaw)
    b1sin = m.sin(yaw)
    b1cos = m.cos(yaw)
    return 0

def b2p(msg):
    global b2sin
    global b2cos
    qz = msg.orientation.z
    yaw = 2*m.atan(qz)
    print('bot2',yaw)
    b2sin = m.sin(yaw)
    b2cos = m.cos(yaw)
    return 0

def b3p(msg):
    global b3sin
    global b3cos
    qz = msg.orientation.z
    yaw = 2*m.atan(qz)
    print('bot3',yaw)
    b3sin = m.sin(yaw)
    b3cos = m.cos(yaw)
    return 0

def b4p(msg):
    global b4sin
    global b4cos
    qz = msg.orientation.z
    yaw = 2*m.atan(qz)
    print('bot4',yaw)
    b4sin = m.sin(yaw)
    b4cos = m.cos(yaw)
    return 0

def run():
    global b1lt
    global b2lt
    global b3lt
    global b4lt
    rospy.init_node('listener', anonymous=True)
    rate = rospy.Rate(60)
    rospy.Subscriber("bot1twistglobal", Twist, b1t)
    rospy.Subscriber("bot2twistglobal", Twist, b2t)
    rospy.Subscriber("bot3twistglobal", Twist, b3t)
    rospy.Subscriber("bot4twistglobal", Twist, b4t)
    rospy.Subscriber("bot1pose", Pose, b1p)
    rospy.Subscriber("bot2pose", Pose, b2p)
    rospy.Subscriber("bot3pose", Pose, b3p)
    rospy.Subscriber("bot4pose", Pose, b4p)
    b1tpub = rospy.Publisher("bot1twist",Twist,queue_size = 10)
    b2tpub = rospy.Publisher("bot2twist",Twist,queue_size = 10)
    b3tpub = rospy.Publisher("bot3twist",Twist,queue_size = 10)
    b4tpub = rospy.Publisher("bot4twist",Twist,queue_size = 10)
    while(True):
        b1tpub.publish(b1lt)
        b2tpub.publish(b2lt)
        b3tpub.publish(b3lt)
        b4tpub.publish(b4lt)
        rate.sleep()


if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException:
        pass
