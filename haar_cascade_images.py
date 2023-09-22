'''Testing Haar Cascade detection through OpenCV using the OpenCV documentation. 
By Angel Rodriguez 2023'''

import cv2 as cv
import os

CWD = os.getcwd()
image_folder = 'positive'

# Check if the "positive" folder exists in the first directory
if not os.path.exists(os.path.join(image_folder)):
    # If not, create a symlink to the shared folder
    positive_folder = r'C:\Users\10801309\OneDrive - Utah Valley University\23-07-31-Mini3ProSmallWtb\positive'
    os.symlink(positive_folder, os.path.join(CWD, image_folder))

def findTurbine(img, cascade_path, largest_only=False):
    '''Take an input image and searches for the target object using an xml file. 
    Returns the inupt image with boundaries drawn around the detected object and the x and y values of the center of the target in the image
    as well as the area of the detection boundary.'''
    # Use Haar Cascades to detect objects using the built-in clasifier tool
    cascade = cv.CascadeClassifier(cascade_path + '\cascade.xml')
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    turbines = cascade.detectMultiScale(gray, 1.2, 8)

    turbineListC = []
    turbineListArea = []
    # turbineListW = []
    turbine_annotations = {}

    cv.putText(img, cascade_path, (0, len(img)-5), cv.FONT_HERSHEY_PLAIN, 2, (255,255,255))
    for (x,y,w,h) in turbines:
        # draw a rectangle around the detected object
        # code for creating a rectangle to see dectection boundaries --
        if not largest_only:
            cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # determine the center of the detection boundaries and the area
        centerX = x + w // 2
        centerY = y + h // 2
        area = w * h
        turbineListC.append([centerX, centerY])
        turbineListArea.append(area)
        turbine_annotations[area] = [x, y, w, h]
    
    if turbine_annotations and largest_only: # If there are detected turbines and we want to only draw the largest
        # print(turbine_annotations)
        max_key = max(list(turbine_annotations.keys()))
        max_values = turbine_annotations[max_key]
        cv.rectangle(img, (max_values[0], max_values[1]), (max_values[0] + max_values[2], max_values[1] + max_values[3]), (0, 0, 255), 2)

    if len(turbineListArea) != 0:
        # if there is items in the area list, find the maximum value and return
        i = turbineListArea.index(max(turbineListArea))
        return img, [turbineListC[i], turbineListArea[i], w]
    else:
        return img, [[0, 0], 0, 0]


if __name__ == "__main__":
    
    # cascade_path = os.path.join(CWD, cascade_folder)
    cascade_folder = "cascade"
    test_images_path = os.path.join(CWD, image_folder)
    image_paths = []
    for subdir, dirs, files in os.walk(test_images_path):
        for file in files:
            if file.endswith((".png",".jpg")):
                file = os.path.join(test_images_path,file)
                image_paths.append(file)
     
    for file in image_paths:
        img = cv.imread(file)
        # img = cv.resize(img, (w, h))
        img, info = findTurbine(img, cascade_folder, largest_only=True)
        if info[0][0]: # Turbine detected
            # (Focal length of camera lense * Real-world width of object)/Width of object in pixels
            # About 22 cm correctly calculates the distance of my face, feel free to revise to work with you
            print(f'turbine detected')
        else: # Turbine not detected
            print(f'turbine NOT detected')
        # Display output window showing the drone's camera frames
        cv.imshow("Output", img)
        cv.waitKey(0)

        x, y = info[0]  # The x and y location of the center of the bounding box in the frame
        area = info[1]  # The area of the bounding box
        width = info[2] # The width of the bounding box

