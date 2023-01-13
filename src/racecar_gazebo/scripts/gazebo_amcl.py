#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Pose, Transform, TransformStamped,  PoseWithCovarianceStamped
from std_msgs.msg import Header
import numpy as np
import math
import tf2_ros

class AmclPoseNode:
    # Set publishers
    pub_pose = rospy.Publisher('/car_pose',  PoseWithCovarianceStamped, queue_size=1)

    def __init__(self):
        # init internals
        self.last_received_pose = Pose()
        self.last_recieved_stamp = None

        # Set the update rate
        rospy.Timer(rospy.Duration(.05), self.timer_callback) # 20hz

        self.tf_pub = tf2_ros.TransformBroadcaster()

        # Set subscribers
        rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.sub_robot_pose_update)

    def sub_robot_pose_update(self, msg):

        try:
            pass
            # arrayIndex = msg.name.index('racecar::base_link')
        except ValueError as e:
            # Wait for Gazebo to startup
            pass
        else:
            self.last_received_pose = msg.pose
        self.last_recieved_stamp = rospy.Time.now()

    def timer_callback(self, event):
        if self.last_recieved_stamp is None:
            return

        cmd = PoseWithCovarianceStamped()
        cmd.header.stamp = self.last_recieved_stamp
        cmd.header.frame_id = 'map'
        cmd.pose.pose = self.last_received_pose

        self.pub_pose.publish(cmd)
 
        tf = TransformStamped(
            header=Header(
                frame_id='map',
                stamp=cmd.header.stamp
            ),
            child_frame_id='base_link',
            transform=Transform(
                translation=cmd.pose.pose.pose.position,
                rotation=cmd.pose.pose.pose.orientation
            )
        )

        self.tf_pub.sendTransform(tf)


# Start the node
if __name__ == '__main__':
    rospy.init_node("gazebo_amcl_node")
    node = AmclPoseNode()
    rospy.spin()
