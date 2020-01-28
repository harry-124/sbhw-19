#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
import math as m
from geometry_msgs.msg import Pose
from sbhw.msg import mov
import pygame

pos1 = mov()
pos2 = mov()
pos3 = mov()
pos4 = mov()

pos1.mode = 1
pos2.mode = 1
pos3.mode = 1
pos4.mode = 1

pos1.x = 200
pos1.y = 150

pos2.x = 200
pos2.y = -150

pos3.x = -200
pos3.y = -150

pos4.x = -200
pos4.y = 150

pos = [pos1,pos2,pos3,pos4]

def run():
    b1mov = mov()
    rate = rospy.Rate(60)
    pygame.init()
    pygame.joystick.init()
    b1tpub = rospy.Publisher("bot1mov",mov,queue_size = 10)
    i = 0
    bn = 0
    while(True):
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                done=True
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            name = joystick.get_name()
            axes = joystick.get_numaxes()
            hats = joystick.get_numhats()
            for i in range( hats ):
                hat = joystick.get_hat( i )
            a,b = hat
            buttons = joystick.get_numbuttons()
            k = joystick.get_button(0) ## 0 or 1 -> kick
        if a == 1:
            bn = 1
        if b == 1:
            bn = 0
        if b ==-1:
            bn = 2
        if a ==-1:
            bn = 3
        b1mov = pos[bn]
        print b1mov.x,b1mov.y,bn
        b1tpub.publish(b1mov)
        rate.sleep()

if __name__ == '__main__':
    try:
        rospy.init_node('squaretest', anonymous=True)
        run()
    except rospy.ROSInterruptException:
        pass