'''Testing Haar Cascade detection through OpenCV using the OpenCV documentation. 
By Angel Rodriguez 2023'''

import cv2 as cv
import os
import numpy as np

CWD = os.getcwd()
left_file = 'outdoor_pos.txt'
right_file = 'mason_pos.txt'
# cascade_path = os.path.join(CWD, cascade_folder)

def draw_annotation(img, x, y, w, h, filename):
    '''Draw rectangle over image using .txt annotations from opencv_annotations.exe to see how annotaiton looks'''
    cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv.putText(img, filename, (0, len(img)-5), cv.FONT_HERSHEY_PLAIN, 2, (255,255,255))
    return img

if __name__ == "__main__":

    file1 = {}
    file2 = {}
    with open(left_file) as file:
        for line in file:
            file1[line.split()[0]] = [int(line.split()[2]), int(line.split()[3]), int(line.split()[4]), int(line.split()[5])]

    with open(right_file) as file:
        for line in file:
            file2[line.split()[0]] = [int(line.split()[2]), int(line.split()[3]), int(line.split()[4]), int(line.split()[5])]
    
    common_images = []
    for img_name in file1:
        if img_name in file2:
            common_images.append(img_name)

    for img_path in common_images:
        img1 = cv.imread(img_path)
        img1 = draw_annotation(img1, file1[img_path][0], file1[img_path][1], file1[img_path][2], file1[img_path][3], left_file)
        img2 = cv.imread(img_path)
        img2 = draw_annotation(img2, file2[img_path][0], file2[img_path][1], file2[img_path][2], file2[img_path][3], right_file)
        img = np.hstack((img1, img2))
        cv.imshow(f'Annotation Comparison of {img_path}: {left_file} (left) vs {right_file} (right)', img)
        print(f'Coordinates from {left_file}: {file1[img_path][0]}, {file1[img_path][1]}, {file1[img_path][2]}, {file1[img_path][3]}')
        print(f'Coordinates from {right_file}: {file2[img_path][0]}, {file2[img_path][1]}, {file2[img_path][2]}, {file2[img_path][3]}')
        cv.waitKey(0)
        cv.destroyAllWindows()




