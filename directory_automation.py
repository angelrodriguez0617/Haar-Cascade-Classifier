from os.path import join
from os import listdir, rmdir
from shutil import move
import os
import cv2 as cv
import shutil

def extract_from_folders(root, recusrive=False):
    '''Takes all of the files out of all folders in CWD and places those files in the CWD
    and removes the folders which are empty afterwards'''
    # root = os.getcwd()

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
        for subdir, dirs, files in os.walk(root):
            for file in files:
                file_path = os.path.abspath(os.path.join(subdir, file))
                move(file_path, join(root, file))
            for dir in dirs:
                dir_path = os.path.abspath(os.path.join(subdir, dir))
                if not os.listdir(dir_path): # If directory is empty which it should be since we moved all the files
                    rmdir(dir_path)
                else: # If the directory is NOT empty as expected because there are still subdirectories in it
                    for subfile in os.listdir(dir_path):
                        subfile_path = os.path.abspath(os.path.join(dir_path, subfile))
                        move(subfile_path, join(root, subfile))
                    rmdir(dir_path)

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

def move_files(source_dir, dest_dir):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, file)
            shutil.move(src_file, dest_file)
        for dir in dirs:
            dir_path = os.path.abspath(os.path.join(root, dir))
            if not os.listdir(dir_path): # If directory is empty which it should be since we moved all the files
                os.rmdir(dir_path)
    os.rmdir(source_dir)

def replace_in_file(file_path, old_string, new_string):
    with open(file_path, 'r') as f:
        file_content = f.read()
        replaced_content = file_content.replace(old_string, new_string)
    with open(file_path, 'w') as f:
        f.write(replaced_content)

# root = r'C:\Users\10801309\OneDrive - Utah Valley University\23-07-31-Mini3ProSmallWtb\23-09-02 Photos from desktop software Mixed'
# extract_from_folders(root, recusrive=True)
# create_video()
# move_files(r'Sat-Sept-9th', 'uncategorized_images')
# replace_in_file('Sat-Sept-9th pos.txt', 'Sat-Sept-9th', 'positive')
