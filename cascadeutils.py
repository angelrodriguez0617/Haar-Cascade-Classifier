'''Used for training a Cascade Classifier, useful tutorial here:
https://learncodebygaming.com/blog/training-a-cascade-classifier'''

import os
from shutil import move

# reads all the files in the /negative folder and generates neg.txt from them.
# we'll run it manually like this:
# $ python
# Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:21:23) [MSC v.1916 32 bit (Intel)] on win32
# Type "help", "copyright", "credits" or "license" for more information.
# >>> from cascadeutils import generate_negative_description_file
# >>> generate_negative_description_file()
# >>> exit()
def generate_negative_description_file():
    # open the output file for writing. will overwrite all existing data in there
    with open('neg.txt', 'w') as f:
        # loop over all the filenames
        for filename in os.listdir('negative'):
            f.write('negative/' + filename + '\n')

def check_pos(filename, dir):
    img_list = []
    img_destination = 'uncategorized_images'
    with open(filename, 'r') as file1:
        for line in file1:
            img_name = line.split()[0].split('\\')[1]
            img_list.append(img_name)
            if not os.path.isfile(os.path.join(dir, img_name)): # Check if file exists within the directory
                print(f'{img_name} from {filename} is not found in {dir} directory')
    for file in os.listdir(dir):
        if file not in img_list:
            print(f'{file} from {dir} directory not found in {filename}, moving it to {img_destination}')
            move(os.path.join(dir, file), os.path.join(img_destination, file))


def delete_duplicate_files(source_dir, target_dir1, target_dir2):
    '''Delete file from source directory if it exists in target directory'''
    for filename in os.listdir(source_dir):
        if filename in os.listdir(target_dir1) or filename in os.listdir(target_dir2):
            os.remove(os.path.join(source_dir, filename))            


# generate_negative_description_file()
check_pos('all_pos.txt', 'positive')
delete_duplicate_files('uncategorized_images', 'negative', 'positive')
# the opencv_annotation executable can be found in opencv/build/x64/vc15/bin
# generate positive description file using:
# & "C:\Users\10801309\OneDrive - Utah Valley University\opencv\build\x64\vc15\bin\opencv_annotation.exe" --annotations=pos.txt --images=positive/

# You click once to set the upper left corner, then again to set the lower right corner.
# Press 'c' to confirm.
# Or 'd' to undo the previous confirmation.
# When done, click 'n' to move to the next image.
# Press 'esc' to exit.
# Will exit automatically when you've annotated all of the images

# generate positive samples from the annotations to get a vector file using:
# & "C:\Users\10801309\OneDrive - Utah Valley University\opencv\build\x64\vc15\bin\opencv_createsamples.exe" -info pos.txt -w 24 -h 24 -num 1000 -vec pos.vec
# There are a few arguments here to pay attention to. 
# Value for -num should be greater than or equal to the number of rectangles you drew, so that all of them get turned into vectors. 
# If you drew 100 rectangles and set this to 1000, it will still output only 100 vectors, so you can just make this any large number. 
# The -w and -h is the detection window size you want to use. 
# You won't be able to detect objects smaller than this size, and the larger you make this the longer it will take to train your model. 
# 20 or 24 are common.

# train the cascade classifier model using:
# & "C:\Users\10801309\OneDrive - Utah Valley University\opencv\build\x64\vc15\bin\opencv_traincascade.exe" -data cascade/ -vec pos.vec -bg neg.txt -numPos 200 -numNeg 100 -numStages 10 -w 24 -h 24
# There are many arguments here to talk about.
# The -numPos needs to be some amount lower than the number of samples created by createsamples.
# If you get errors that look like: Can not get new positive sample. Then you need to either lower your -numPos or lower the -minHitRate (default 0.995).
# A popular suggestion for -numNeg is to use half of -numPos. This is a good place to start, but you'll want to try many different values here. 
# Using twice the number of negative to positive, or even more, can sometimes yield better results.
# The -w and -h must match what was used for the createsamples step.
# The more -numStages the longer it will take to train. Too many and you might overtrain.
# If you run initially with 10 stages, you can later run it again with more stages, like 30, and it will pick up from where it left off. 
# As you get deeper into the stages, each one takes longer.

# When you run the training, you'll get some useful insights in the terminal output. 
# In the results table, HR means hit rate (the number of positive examples that were correctly identified), 
# FA is false alarm (the number of negative samples that were incorrectly identified),
# and N = weak layer number (which Haar cascade layer the rates are for). 
# A really small Neg acceptanceRatio can sometimes be an indication of overtraining, ie. if it has e-06. We'll talk more about overtraining in a little bit.

# You can get faster training by using the -precalcValBufSize and -precalcIdxBufSize parameters. 
# Keep in mind that these combined values should not exceed your available system memory.
# If you have too many false positives: add more -numNeg and train for more -numStages.
# If you valid objects are being missed: you overfit your data so try reducing the number of stages.
# Overtraining or overfitting means you trained your classifier to only recognize the exact images you have in your positive folder, 
# so it's not going to generalize well to any slightly different images. This is a common problem in machine learning. 
# Keep in mind that the best solution isn't always more or longer training. You may get improvements by actually reducing the number of training stages. 
# Your model will eventually hit the limit of what can be achieved with your dataset, and the only way to improve from there is with more and better training data.

# my final classifier training arguments:
# $ C:/Users/Ben/learncodebygaming/opencv/build/x64/vc15/bin/opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -precalcValBufSize 6000 -precalcIdxBufSize 6000 -numPos 200 -numNeg 1000 -numStages 12 -w 24 -h 24 -maxFalseAlarmRate 0.4 -minHitRate 0.999