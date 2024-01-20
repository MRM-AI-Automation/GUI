#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
import rospy
from std_msgs.msg import Int64
import numpy as np
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import cv2

class GUI(QWidget):
    def __init__(self):
        self.count=0
        super(GUI, self).__init__()

        self.bridge = CvBridge()
        self.camera_number = 1

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('GUI')
        self.setGeometry(100, 100, 800, 600)

        self.label = QLabel(self)

        self.button_screenshot = QPushButton('Take Screenshot', self)
        self.button_screenshot.clicked.connect(self.screenshot)

        self.button_launch1 = QPushButton('Switch to Microscope', self)
        self.button_launch1.clicked.connect(lambda: self.switch_camera(1))

        self.button_launch2 = QPushButton('Switch to Camera', self)
        self.button_launch2.clicked.connect(lambda: self.switch_camera(2))

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.button_screenshot)
        layout.addWidget(self.button_launch1)
        layout.addWidget(self.button_launch2)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(100)  # Update every 100 milliseconds

    def update_image(self):
        try:
            camera_image = rospy.wait_for_message('/usb_cam/image_raw/compressed', CompressedImage, timeout=1)
            np_arr = np.frombuffer(camera_image.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            cv_image_bgr = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)  # Convert to BGR format

            height, width, channel = cv_image_bgr.shape
            bytes_per_line = 3 * width
            q_image = QImage(cv_image_bgr.data, width, height, bytes_per_line, QImage.Format_RGB888)

            self.label.setPixmap(QPixmap.fromImage(q_image))

        except rospy.exceptions.ROSException as e:
            print(f"Error: {e}")


    def screenshot(self):
        self.save_screenshot(self.label)

    def save_screenshot(self, label):
        pixmap = label.pixmap()
        if pixmap:
            pixmap.save(f"/home/nikhilesh/camera_ws/src/science/scripts/site1/screenshot_{self.count}.png")
            print(self.count)
            self.count+=1
            

    def switch_camera(self, camera_number):
        self.camera_number = camera_number
        rospy.loginfo(f'Switching to Camera {self.camera_number}')
        camera_switch_publisher.publish(self.camera_number)

if __name__ == '__main__':
    rospy.init_node('ros_image_subscriber', anonymous=True)
    camera_switch_publisher = rospy.Publisher('camera_switch_topic', Int64, queue_size=1)

    app = QApplication(sys.argv)
    camera_controller = GUI()
    camera_controller.show()
    sys.exit(app.exec_())