import cv2
class VideoCamera(object):
    def __init__(self):
      self.video = cv2.VideoCapture(2)



    def __del__(self):
      self.video.release()

    def get_frame(self):
      
      ret, frame = self.video.read()
    #   print("frame: ", frame)
    #   cv2.imshow('frame', frame)
      ret, jpeg = cv2.imencode('.jpg', frame)
      return jpeg.tobytes()

# import cv2

# # Print the number of available cameras
# num_cameras = 5  # You can adjust the range based on your system
# for i in range(num_cameras):
#     cap = cv2.VideoCapture(i)
#     if not cap.read()[0]:
#         continue
#     cap.release()
#     print(f"Camera {i} is available")
