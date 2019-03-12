#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
import math as m
from geometry_msgs.msg import Pose
from sbhw.msg import mov

def run():
    pos1 = [150,150]
    pos2 = [-150,150]
    pos3 = [-150,-150]
    pos4 = [150,-150]
    b1mov = mov()
    b2mov = mov()
    b3mov = mov()
    b4mov = mov()
    b1mov.mode =1
    b2mov.mode =1
    b3mov.mode =1
    b4mov.mode =1
    b1mov.x = pos1[0]
    b1mov.y = pos1[1]
    b2mov.x = pos2[0]
    b2mov.y = pos2[1]
    b3mov.x = pos3[0]
    b3mov.y = pos3[1]
    b4mov.x = pos4[0]
    b4mov.y = pos4[1]
    rate = rospy.Rate(60)
    b1tpub = rospy.Publisher("bot1mov",mov,queue_size = 10)
    b2tpub = rospy.Publisher("bot2mov",mov,queue_size = 10)
    b3tpub = rospy.Publisher("bot3mov",mov,queue_size = 10)
    b4tpub = rospy.Publisher("bot4mov",mov,queue_size = 10)
    i = 0
    while(True):
        b1tpub.publish(b1mov)
        b2tpub.publish(b2mov)
        b3tpub.publish(b3mov)
        b4tpub.publish(b4mov)
        rate.sleep()

if __name__ == '__main__':
    try:
        rospy.init_node('lqwr', anonymous=True)
        run()
    except rospy.ROSInterruptException:
        pass
