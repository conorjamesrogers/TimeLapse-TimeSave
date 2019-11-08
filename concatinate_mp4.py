# WHAMSTACK IT
# script to concatinate directroy of videos to video.
# By Conor Rogers
# 2019

import cv2
import os
from functools import cmp_to_key
import argparse


def image_sort_datetime (x,y):
    x = os.path.getmtime(x)
    y = os.path.getmtime(y)
    return x - y

# combines all mp4's specified in array of directory addresses, then returns an array of frame data.
def combine_mp4(video_file_array,video_write_object):

    capture= cv2.VideoCapture(video_file_array[0])
    video_index=0

    # frames=[]

    while(capture.isOpened()):
        ret, frame = capture.read()
        if frame is None:
            print("end of video " + str(video_index) + " .. next one now")
            video_index += 1
            if video_index >= len(video_file_array):
                break
            capture.release()
            capture = cv2.VideoCapture(video_file_array[ video_index ])
            ret, frame = capture.read()
            # if not  ret:
            #     break
        # frames.append(frame)
        video_write_object.write(frame)

        # cv2.imshow('frame',frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
    print("...")

    capture.release()

    # return frames

argp = argparse.ArgumentParser()
argp.add_argument("-e","--extension", required=False,default='mp4',help="extension of video, default will be 'mp4'.")
argp.add_argument("-d","--directory",required=False,default='.',help="select directory of images, default is current directory.")
argp.add_argument("-o","--output",required=False,default='default_out.mp4',help="output video file name default will be 'default_out.mp4' (program will use ffmpeg, so *.mp4).")
argp.add_argument("-wi","--width",required=False,default=1920,help="enter width value, default is 1920.")
argp.add_argument("-hi","--height",required=False,default=1080,help="enter height value, default is 1080.")
argp.add_argument("-s","--start_with",required=False,default='h264',help="starting letters of video file")
argp.add_argument("-m","--mothership_deploy",action='store_true',help="convert all directories in given directory to video, then concatinate")
# argp.add_argument("-st","--start-time",requied=False,default=7,help="Filter images based on time taken, range is ")
args = vars(argp.parse_args())
dir_path=args['directory']
ext=args['extension']
strt=args['start_with']
out=args['output']
vid_width=args['width']
vid_height=args['height']
mothership_deploy_flag=args['mothership_deploy']

video_file_array = []
for f in os.listdir(dir_path):
    if f.startswith(strt) and f.endswith(ext):
        video_file_array.append(dir_path+'/'+f)

video_file_array = sorted(video_file_array,key=cmp_to_key(image_sort_datetime))

# codec def, change this here if mp4 doesn't work for you
# use lower case:
fourcc=cv2.VideoWriter_fourcc(*'mp4v')
# video FPS
fps=25.0

output_write=cv2.VideoWriter(out,fourcc,fps,(vid_width,vid_height),True)

if mothership_deploy_flag:
     for d in os.listdir(dir_path):
            print(dir)

print(video_file_array)
combine_mp4(video_file_array,output_write)

os.system("ffmpeg -i {} -f mp4 -vcodec libx264 -preset fast -profile:v main -acodec aac {} -hide_banner".format(out,'h264_'+out))

