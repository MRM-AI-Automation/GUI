# import cv2

# # Open the camera (0 is usually the default for the first connected camera)
# cap = cv2.VideoCapture(2)

# # Check if the camera is opened successfully
# if not cap.isOpened():
#     print("Error: Could not open camera.")
#     exit()

# while True:
#     # Capture frame-by-frame
#     ret, frame = cap.read()

#     # Check if the frame was captured successfully
#     if not ret:
#         print("Error: Failed to capture frame.")
#         break

#     # Display the resulting frame
#     cv2.imshow('USB Camera', frame)

#     # Break the loop if 'q' key is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the camera and close the window
# cap.release()
# cv2.destroyAllWindows()

import cv2

# Print the number of available cameras
num_cameras = 5  # You can adjust the range based on your system
for i in range(num_cameras):
    cap = cv2.VideoCapture(i)
    if not cap.read()[0]:
        continue
    cap.release()
    print(f"Camera {i} is available")
