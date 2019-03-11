#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
import pygame

def talker():
    rospy.init_node('joystick', anonymous=True)
    pubd1 = rospy.Publisher('bot1d', Int32, queue_size = 10)
    pubd2 = rospy.Publisher('bot2d', Int32, queue_size = 10)
    pubd3 = rospy.Publisher('bot3d', Int32, queue_size = 10)
    pubd4 = rospy.Publisher('bot4d', Int32, queue_size = 10)
    pubk1 = rospy.Publisher('bot1k', Int32, queue_size = 10)
    pubk2 = rospy.Publisher('bot2k', Int32, queue_size = 10)
    pubk3 = rospy.Publisher('bot3k', Int32, queue_size = 10)
    pubk4 = rospy.Publisher('bot4k', Int32, queue_size = 10)
    pubv1 = rospy.Publisher('bot1twistglobal',Twist,queue_size = 10)
    pubv2 = rospy.Publisher('bot2twistglobal',Twist,queue_size = 10)
    pubv3 = rospy.Publisher('bot3twistglobal',Twist,queue_size = 10)
    pubv4= rospy.Publisher('bot4twistglobal',Twist,queue_size = 10)
    rate = rospy.Rate(60)
    while not rospy.is_shutdown():
    	pygame.init()

    	rate = rospy.Rate(60)

    	pygame.joystick.init()
        botn = 1
    	while True:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                	done=True 

            joystick_count = pygame.joystick.get_count()

            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                name = joystick.get_name()
    
                axes = joystick.get_numaxes()
        
                vx = joystick.get_axis(3)
                vx = vx*abs(vx)
                vy = joystick.get_axis(4)
                vy = vy*abs(vy)
                ds = joystick.get_axis(5)
                hats = joystick.get_numhats()
                for i in range( hats ):
                	hat = joystick.get_hat( i )
                a,b = hat
                print a,b
                buttons = joystick.get_numbuttons()

                k = joystick.get_button(0) ## 0 or 1 -> kick
                s = joystick.get_button(1) # Switch robot
                LB = joystick.get_button(4) ## 0 or 1 -> anti-clockwise rotation
                RB = joystick.get_button(5) ## 0 or 1 -> clockwise rotation
            if a == 1:
                botn = 2
            if b == 1:
                botn =1
            if b ==-1:
                botn = 3
            if a ==-1:
                botn = 4
            
            if(LB == 0 and RB ==1):
                wz = -0.1
            if(LB == 1 and RB ==0):
                wz = 0.1
            if( ( LB ==0 and RB == 0 ) or ( LB==1 and RB == 1 ) ):
                wz = 0
            vx = vx*0.06 
            vy = -vy*0.06 

            if ds < 0:
                ds = 0 ## value from 0 to 1
            ds = int(ds*255)
            tw = Twist()
            tw.linear.x = vx
            tw.linear.y = vy
            tw.angular.z = wz
            twelse = Twist()
            twelse.linear.x = 0
            twelse.linear.y = 0
            twelse.angular.z = 0
            if botn == 1:
                pubv1.publish(tw)
                pubv2.publish(twelse)
                pubv3.publish(twelse)
                pubv4.publish(twelse)
                pubd1.publish(ds)
                pubd2.publish(0)
                pubd3.publish(0)
                pubd4.publish(0)
                pubk1.publish(k)
                pubk2.publish(0)
                pubk3.publish(0)
                pubk4.publish(0)
            if botn == 2:
                pubv1.publish(twelse)
                pubv2.publish(tw)
                pubv3.publish(twelse)
                pubv4.publish(twelse)
                pubd1.publish(0)
                pubd2.publish(ds)
                pubd3.publish(0)
                pubd4.publish(0)
                pubk1.publish(0)
                pubk2.publish(k)
                pubk3.publish(0)
                pubk4.publish(0)
            if botn == 3:
                pubv1.publish(twelse)
                pubv2.publish(twelse)
                pubv3.publish(tw)
                pubv4.publish(twelse)
                pubd1.publish(0)
                pubd2.publish(0)
                pubd3.publish(ds)
                pubd4.publish(0)
                pubk1.publish(0)
                pubk2.publish(0)
                pubk3.publish(k)
                pubk4.publish(0)
            if botn == 4:
                pubv1.publish(twelse)
                pubv2.publish(twelse)
                pubv3.publish(twelse)
                pubv4.publish(tw)
                pubd1.publish(0)
                pubd2.publish(0)
                pubd3.publish(0)
                pubd4.publish(ds)
                pubk1.publish(0)
                pubk2.publish(0)
                pubk3.publish(0)
                pubk4.publish(k)
            rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass