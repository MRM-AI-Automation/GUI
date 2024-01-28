import threading
import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

bridge = CvBridge()
cv_image = None

class VideoCamera(object):
    def __init__(self):
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.callback)

    def callback(self, data):
        global cv_image
        try:
            cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
            cv2.imshow("Microscope", cv_image)
            cv2.waitKey(1)
        except CvBridgeError as e:
            print(e)

    def __del__(self):
        cv2.destroyAllWindows()

    def get_frame(self):
        global cv_image
        ret, jpeg = cv2.imencode('.jpg', cv_image)
        return jpeg.tobytes()

if __name__ == '__main__':
    cam = VideoCamera()
    rospy.init_node('microscope', disable_signals=True)
    rospy.spin()



# import cv2
# from cv_bridge import CvBridge, CvBridgeError
# import threading
# import rospy
# from sensor_msgs.msg import Image


# bridge = CvBridge()

# cv_image = 0

# class VideoCamera(object):
#     def __init__(self):
#       pass

#     def callback(data):
#         global cv_image
#         try:
#             cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
#             cv2.imshow("Microscope", cv_image)
#         except CvBridgeError as e:
#             print(e)

#     threading.Thread(target=lambda: rospy.init_node('microscope', disable_signals=True)).start()
#     image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, callback)

#     def __del__(self):
#       self.video.release()   

#     def get_frame(self):
#       global cv_image
#       ret, jpeg = cv2.imencode('.jpg', cv_image)
#       return jpeg.tobytes()
  
