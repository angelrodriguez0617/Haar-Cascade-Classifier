from os.path import join
from os import listdir, rmdir
from shutil import move
import os
import cv2 as cv

def extract_from_folders(recusrive=False):
    '''Takes all of the files out of all folders in CWD and places those files in the CWD
    and removes the folders which are empty afterwards'''
    root = os.getcwd()
    root = r'C:\Users\10801309\OneDrive - Utah Valley University\23-07-31-Mini3ProSmallWtb\negative'

    if not recusrive : # Take all files in immediate subdirectories of root (not recursively) and place them so root is the parent directory of those files
        for directory in listdir(root):
            for filename in listdir(join(root, directory)):
                move(join(root, directory, filename), join(root, filename))
            dir_path = os.path.abspath(directory)
            if not os.listdir(dir_path): # If directory is empty which it should be since we moved all the files
                rmdir(dir_path)
            else: # If the directory is NOT empry as expected
                print(f'DIRECTORY {dir_path} IS NOT EMPTY AS EXPECTED')
    
    else: # Recursively take all files in root (including subdirectories of subdirectory and so on) and place them so root is the parent directory of all files
        for root, dirs, files in os.walk(root):
            for file in files:
                move(os.path.abspath(file)), join(root, file)
            for dir in dirs:
                dir_path = os.path.abspath(dir)
                if not os.listdir(dir_path): # If directory is empty which it should be since we moved all the files
                    rmdir(dir_path)
                else: # If the directory is NOT empry as expected
                    print(f'DIRECTORY {dir_path} IS NOT EMPTY AS EXPECTED')

def create_video():
    image_folder = 'positive'
    video_name = 'video.avi'

    images = [img for img in os.listdir(image_folder) if img.endswith(".png") or img.endswith(".jpg")]
    frame = cv.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv.VideoWriter(video_name, 0, 1, (width,height))

    for image in images:
        video.write(cv.imread(os.path.join(image_folder, image)))

    cv.destroyAllWindows()
    video.release()

# extract_from_folders(recusrive=True)
# create_video()