#!/usr/bin/env python
import rospy
import math
from geometry_msgs.msg import Twist
import sys, select, os
import tty, termios

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

settings = termios.tcgetattr(sys.stdin)
rospy.init_node("tarea2.py")
pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
twist = Twist()
NumeroCuadros=0
while not rospy.is_shutdown():
    print("Ingrese el numero de cuadros a patrullar:")
    try:
        NumeroCuadros=int(getKey())
    except:
        continue
    print("Numero de cuadros a patrullar: "+str(NumeroCuadros))
    for contadorCuadros in range(4):
        twist.linear.x=0.5
        twist.angular.z=0
        pub.publish(twist)
        rospy.Rate(twist.linear.x/NumeroCuadros).sleep()
        
        twist.linear.x=0
        twist.angular.z=0.5
        pub.publish(twist)
        rospy.Rate(2*twist.angular.z/math.pi).sleep()
    twist.linear.x=0
    twist.angular.z=0
    pub.publish(twist)