'''Testing Haar Cascade detection through OpenCV using the OpenCV documentation. 
By Angel Rodriguez 2023'''

import cv2 as cv
import os
import numpy
from haar_cascade_images import findTurbine

CWD = os.getcwd()
left_cascade = "cascade"
right_cascade = "all_cascade"
# cascade_path = os.path.join(CWD, cascade_folder)

if __name__ == "__main__":

    # video_path = os.path.join(CWD, "DJI_0556.mp4")
    video_cap = cv.VideoCapture("video.avi")

    while True:
        # Capture frame-by-frame
        ret, img = video_cap.read()
        img = cv.resize(img, None, fx=0.75, fy=0.75, interpolation=cv.INTER_AREA)
        img1, info1 = findTurbine(img.copy(), left_cascade, largest_only=True)
        img2, info2 = findTurbine(img, right_cascade, largest_only=True)
        img = numpy.hstack((img1, img2))
        # Display the resulting frame
        cv.imshow(f'Turbine Detection Comparison: {left_cascade} (left) vs {right_cascade} (right)', img)
        #wait for 'c' to close the application
        if cv.waitKey(1) & 0xFF == ord('c'):
            break

        x, y = info1[0]  # The x and y location of the center of the bounding box in the frame
        area = info1[1]  # The area of the bounding box
        width = info1[2] # The width of the bounding box
    
    video_cap.release()

