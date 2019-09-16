#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64,Int32

def run():
    rospy.init_node('Clock', anonymous=True)
    
    time_pub = rospy.Publisher('Time',Float64,queue_size = 10)
    rate = rospy.Rate(200)
    start = rospy.get_rostime() 

    while(True):
        now = rospy.get_rostime() 
        '''
        gets time in milli seconds and publishes it for the robots to use
        measures time from start of this node
        '''
        m=Float64()
        millis=float(now.nsecs-start.nsecs)/(10.**6)+float(now.secs-start.secs)*(1000.)
        m.data=millis
        time_pub.publish(m)
        rate.sleep()

if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException:
        pass