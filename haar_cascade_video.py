'''Testing Haar Cascade detection through OpenCV using the OpenCV documentation. 
By Angel Rodriguez 2023'''

import cv2 as cv
import os
from haar_cascade_images import findTurbine

CWD = os.getcwd()
cascade_folder = "cascade"
# cascade_path = os.path.join(CWD, cascade_folder)

if __name__ == "__main__":

    # video_path = os.path.join(CWD, "DJI_0556.mp4")
    video_cap = cv.VideoCapture("video.avi")

    while True:
        # Capture frame-by-frame
        ret, img = video_cap.read()
        # img = cv.resize(img, None, fx=0.25, fy=0.25, interpolation=cv.INTER_AREA)
        img, info = findTurbine(img, cascade_folder, largest_only=False)
        if info[0][0]: # Turbine detected
            # (Focal length of camera lense * Real-world width of object)/Width of object in pixels
            # About 22 cm correctly calculates the distance of my face, feel free to revise to work with you
            print(f'turbine detected')
        else: # Turbine not detected
            print(f'turbine NOT detected')
        # Display the resulting frame
        cv.imshow('Turbine Detection on Video', img)
        #wait for 'c' to close the application
        if cv.waitKey(1) & 0xFF == ord('c'):
            break

        x, y = info[0]  # The x and y location of the center of the bounding box in the frame
        area = info[1]  # The area of the bounding box
        width = info[2] # The width of the bounding box
    
    video_cap.release()

