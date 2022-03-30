#!/usr/bin/env python

import time
from math import sin

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry

import cv2
from cv_bridge import CvBridge, CvBridgeError

import numpy as np

import math


def euler_from_quaternion(x, y, z, w):
    """
    Convert a quaternion into euler angles (roll, pitch, yaw)
    roll is rotation around x in radians (counterclockwise)
    pitch is rotation around y in radians (counterclockwise)
    yaw is rotation around z in radians (counterclockwise)
    """
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)

    return roll_x, pitch_y, yaw_z  # in radians


def nothing(x):
    pass


kernel = np.ones((5, 5), np.uint8)


# cv2.namedWindow("track", cv2.WINDOW_NORMAL)

# cv2.createTrackbar("H","track", 33, 180, nothing)
# cv2.createTrackbar("S","track", 245, 255, nothing)
# cv2.createTrackbar("V","track", 255, 255, nothing)

# cv2.createTrackbar("HL","track", 0, 180, nothing)
# cv2.createTrackbar("SL","track", 236, 255, nothing)
# cv2.createTrackbar("VL","track", 201, 255, nothing)
class SimpleCV():

    def __init__(self):
        rospy.init_node('simple_mover', anonymous=True)
        rospy.on_shutdown(self.shutdown)

        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        rospy.Subscriber("diff_drive_robot/camera1/image_raw", Image, self.camera_cb)
        rospy.Subscriber("odom", Odometry, self.odometry)
        self.rate = rospy.Rate(30)

        self.cv_bridge = CvBridge()

    def odometry(self, msg):
        pose1 = msg.pose.pose.orientation
        _, _, self.orientation_z = euler_from_quaternion(pose1.x, pose1.y, pose1.z, pose1.w)
        print(self.orientation_z)

    def camera_cb(self, msg):

        try:
            cv_image = self.cv_bridge.imgmsg_to_cv2(msg, "bgr8")

        except CvBridgeError, e:
            rospy.logerr("CvBridge Error: {0}".format(e))

        self.show_image(cv_image)

    def show_image(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_blue_dots = cv2.inRange(hsv, np.array([96, 0, 0]), np.array([118, 255, 255]))
        _, contours, _ = cv2.findContours(mask_blue_dots, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for x in range(len(contours)):
            area = cv2.contourArea(contours[x])
            if area > 5:
                x, y, w, h = cv2.boundingRect(contours[x])
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        mask_green = cv2.inRange(hsv, np.array([52, 0, 0]), np.array([89, 255, 243]))
        _, contours, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for x in range(len(contours)):
            area = cv2.contourArea(contours[x])
            if area > 5:
                x, y, w, h = cv2.boundingRect(contours[x])
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        mask_yellow = cv2.inRange(hsv, np.array([0, 125, 201]), np.array([35, 255, 255]))
        _, contours, _ = cv2.findContours(mask_yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for x in range(len(contours)):
            area = cv2.contourArea(contours[x])
            if area > 5:
                x, y, w, h = cv2.boundingRect(contours[x])
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        mask = cv2.inRange(hsv, np.array([0, 0, 77]), np.array([0, 0, 255]))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

        cv2.imshow("yellow", mask_yellow)
        cv2.imshow("blue_dots", mask_blue_dots)
        cv2.imshow("green", mask_green)
        cv2.imshow("walls", closing)
        cv2.imshow("frame", frame)
        cv2.waitKey(3)

    def spin(self):
        start_time = time.time()
        while not rospy.is_shutdown():
            twist_msg = Twist()
            t = time.time() - start_time
            twist_msg.angular.z = 0.4
            self.cmd_vel_pub.publish(twist_msg)
            self.rate.sleep()

    def shutdown(self):
        self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)


simple_mover = SimpleCV()
simple_mover.spin()
