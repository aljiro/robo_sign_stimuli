#!/usr/bin/python3

import numpy as np
import rospy
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import JointState
import time

class MiroActions(object):
    def __init__(self):
        rospy.init_node("actions")
        self.speed = 0.
        self.angular = 0.
        self.tilt = 0.
        self.lift = 0.
        self.yaw = 0.
        self.pitch = 0.
    
    def set_movement(self, speed, angular):
        self.speed = speed
        self.angular = angular
        self.make_movement()

    def make_movement(self):
        cmd_msg = TwistStamped()
        cmd_msg.twist.linear.x = self.speed
        cmd_msg.twist.angular.z = self.angular
        cmd_pub = rospy.Publisher('/miro/control/cmd_vel', TwistStamped, queue_size = 10)
        cmd_pub.publish(cmd_msg)

    def set_kinematic(self, tilt = None, lift = None, yaw = None, pitch = None):
        if not tilt is None:
            self.tilt = tilt
        if not lift is None:
            self.lift = lift
        if not yaw is None:
            self.yaw = yaw
        if not pitch is None:
            self.pitch = pitch
        self.make_kinematic()

    def make_kinematic(self):
        kinematic_msg = JointState()
        kinematic_msg.position = [self.tilt, self.lift, self.yaw, self.pitch]
        print(kinematic_msg.position)
        kinematic_pub = rospy.Publisher('/miro/control/kinematic_joints', JointState, queue_size = 10)
        kinematic_pub.publish(kinematic_msg)

class MiroAttack(MiroActions):

    def __init__(self):
        MiroActions.__init__(self)

    def action(self):
        end = time.time() + 2
        while time.time() < end:
            self.set_movement(1., 0.)
        end = time.time() + 1
        while time.time() < end:
            self.set_kinematic(1., 1.)
        self.set_movement(0., 0.)

class MiroAvoid(MiroActions):
    def __init__(self):
        MiroActions.__init__(self)

    def action(self):
        end = time.time() + 2
        while time.time() < end:
            self.set_movement(-1., 0.)
        end = time.time() + 1
        while time.time() < end:
            self.set_movement(0., 0.)
        self.set_kinematic(0., 0.)

miro = MiroAttack()
miro.action()
miro = MiroAvoid()
miro.action()