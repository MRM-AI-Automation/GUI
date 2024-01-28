#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

class CameraSubscriber:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.image_callback)

    def image_callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
            return

        # Display the image using OpenCV
        cv2.imshow("USB Camera", cv_image)
        cv2.waitKey(1)  # Adjust the waitKey delay as needed

def main():
    rospy.init_node("usb_camera_display_node", anonymous=True)
    camera_subscriber = CameraSubscriber()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
