#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

class ImageSubscriber:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/your/image/topic", Image, self.image_callback)
        self.window_name = "ROS Image Viewer"
        cv2.namedWindow(self.window_name)

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            cv2.imshow(self.window_name, cv_image)
            cv2.waitKey(1)
        except CvBridgeError as e:
            rospy.logerr("Error converting ROS Image to OpenCV image: {}".format(e))

def main():
    rospy.init_node('image_subscriber', anonymous=True)
    image_subscriber = ImageSubscriber()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down...")
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
