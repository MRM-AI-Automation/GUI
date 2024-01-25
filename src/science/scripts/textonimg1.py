import cv2
import numpy as np

def add_overlay(image, angle, lat, long, elevation):
    color = (0, 0, 255)
    h,w,=image.shape[:2]
    image = cv2.putText(image, 'N', (70, 30), cv2.FONT_HERSHEY_TRIPLEX,
                        0.5, color, 1, cv2.LINE_AA)
    image = cv2.putText(image, 'W', (20, 75), cv2.FONT_HERSHEY_TRIPLEX,
                        0.5, color, 1, cv2.LINE_AA)
    image = cv2.putText(image, 'E', (120, 75), cv2.FONT_HERSHEY_TRIPLEX,
                        0.5, color, 1, cv2.LINE_AA)
    image = cv2.putText(image, 'S', (70, 120), cv2.FONT_HERSHEY_TRIPLEX,
                        0.5, color, 1, cv2.LINE_AA)

    image = cv2.putText(image, f'GPS: Latitude: {lat}', (200, 95), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 1, cv2.LINE_AA)
    image = cv2.putText(image, f'GPS: Longitude: {long}', (200, 75), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 1, cv2.LINE_AA)
    image = cv2.putText(image, f'Elevation: {elevation}', (200, 55), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 1, cv2.LINE_AA)
    image = cv2.putText(image, f'Accuracy: 1.5 meters', (200, 35), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 1, cv2.LINE_AA)    

    overlay_image = cv2.imread('/home/nikhilesh/GUII/src/science/scripts/needle2.png', cv2.IMREAD_UNCHANGED)
    overlay_image = cv2.resize(overlay_image, (70, 70))
    row, col, _ = overlay_image.shape
    center = tuple(np.array([row, col]) / 2)
    rot_mat = cv2.getRotationMatrix2D(center, (-1.0) * angle, 1.0)
    overlay_image = cv2.warpAffine(overlay_image, rot_mat, (col, row))

    x_pos = 40
    y_pos = 38

    needle_image = image.copy()

    for y in range(overlay_image.shape[0]):
        for x in range(overlay_image.shape[1]):
            if overlay_image[y, x, 3] > 0:
                needle_image[y + y_pos, x + x_pos, 0] = overlay_image[y, x, 0]
                needle_image[y + y_pos, x + x_pos, 1] = overlay_image[y, x, 1]
                needle_image[y + y_pos, x + x_pos, 2] = overlay_image[y, x, 2]

    overlay_image1 = cv2.imread('/home/nikhilesh/GUII/src/science/scripts/MRM_logo.png', cv2.IMREAD_UNCHANGED)
    overlay_image1 = cv2.resize(overlay_image1, (50, 50))

    x_pos = (image.shape[1]) - overlay_image1.shape[1] - 20
    y_pos = 10

    mrm_image = needle_image.copy()

    for y in range(overlay_image1.shape[0]):
        for x in range(overlay_image1.shape[1]):
            if overlay_image1[y, x, 3] > 0:
                mrm_image[y + y_pos, x + x_pos, 0] = overlay_image1[y, x, 0]
                mrm_image[y + y_pos, x + x_pos, 1] = overlay_image1[y, x, 1]
                mrm_image[y + y_pos, x + x_pos, 2] = overlay_image1[y, x, 2]

    return mrm_image

# Example usage:
input_image = cv2.imread('/home/nikhilesh/GUII/src/science/scripts/panorama_site1/final_12.jpg')  
h,w,=input_image.shape[:2]
output_image = add_overlay(input_image, angle=174.21, lat=11.0243795, long=77.0246601, elevation=413.228)

cv2.imshow('Output Image', output_image)
cv2.imwrite('site1_img1.png', output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
