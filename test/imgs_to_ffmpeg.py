# WHAMSTACK IT
# 'simple' script to convert directroy of imgs to video.
# By Conor Rogers
# 2019

import cv2
import argparse
import os
from multiprocessing import Pool

def isnum (num):
    try:
        int(num)
        return True
    except:
        return False

def image_sort (x,y):
    x = int(x.split(".")[0])
    y = int(y.split(".")[0])
    return x-y

# arg parser
argp = argparse.ArgumentParser()
argp.add_argument("-e","--extension", required=False,default='png',help="extension of photo, default will be 'png'.")
argp.add_argument("-o","--output",required=False,default='default_out.mp4',help="output video file name default will be 'default_out.mp4' (program will use ffmpeg, so *.mp4).")
args = vars(argp.parse_args())

# args
dir_path='.'
ext=args['extension']
out=args['output']

# collect images from current directory
images=[]

for f in os.listdir(dir_path):
    if f.endswith(ext):
        images.append(f)

int_name = images[0].split(".")[0]
if isnum(int_name):
    images = sorted(images, key=cmp_to_key(image_sort))
else:
    print("Failed to sort numerically, switching to alphabetic sort")
    images.sort()

print(images)
# get width/height from first image
img_path=os.path.join(dir_path,images[0])
frame=cv2.imread(img_path)
# cv2.imshow('video',frame)
height,width,channels=frame.shape

# codec def, change this here if mp4 doesn't work for you
# use lower case:
fourcc=cv2.VideoWriter_fourcc(*'mp4v')
# VideoWriter(str<ouput path>,<fourcc codec>,double<fps of video>,tuple<width,height>)
output_write=cv2.VideoWriter(out,fourcc,25.0,(width,height))

# loop for writing each image to a frame of video.
# if you were to parallelize this... run this loop on separate images and outputs then combine the outputs.
# def image_adding(img,output_str=''):
#      # image_path=os.path.join(dir_path,img)
#     # read frame
#     # frame=cv2.imread(image_path)
#     frame=cv2.imread(img[1])
#     # write frame to video
#     output_write=cv2.VideoWriter(out,fourcc,25.0,(width,height))

#     output_write.write(frame)
#     print("writing img {} to frame in video {}".format(img,output_str))


# pool=Pool()
# pool.map(image_adding,images,chunksize=1)

for n, img in enumerate(images):
    image_path=os.path.join(dir_path,img)
    # read frame
    frame=cv2.imread(image_path)
    # frame=cv2.imread(img)
    # write frame to video
    output_write.write(frame)
    if n%100==0:
        print("finished writing first to img {} to frame".format(img))

    # cv2.imshow('video',frame)
    # press q to exit
    if(cv2.waitKey(1) & 0xFF) == ord('q'):
        break

output_write.release()
cv2.destroyAllWindows()

print("video output is: {}".format(out))
