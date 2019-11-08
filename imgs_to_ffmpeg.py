# WHAMSTACK IT
# 'simple' script to convert directroy of imgs to video.
# By Conor Rogers
# 2019

import cv2
import argparse
import os
from concatinate_mp4 import combine_mp4
import multiprocessing
from multiprocessing import Pool, current_process
# from datetime import datetime
import datetime
# from skvideo.io import VideoWriter


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

#collects images in timerange then sorts them, returns sorted filename list
def collect_img(dir_path,ext,time_range,images=[]):
    for f in os.listdir(dir_path):
        if f.endswith(ext):
            t = os.path.getmtime(os.path.join(dir_path,f))
            #currently only adds images between specific times.. there are probably better ways to do this but it works OK for now.
            # will need a sophisticated technique eventually
            mod_time = datetime.datetime.fromtimestamp(t)
            if int(mod_time.hour) > time_range[0] and int(mod_time.hour) < time_range[1]:
                images.append(f)
    int_name = images[0].split(".")[0]
    if isnum(int_name):
        images = sorted(images, key=cmp_to_key(image_sort))
    else:
        print("Failed to sort numerically, switching to alphabetic sort")
        images.sort()

    return images

# parallelization function
def image_adding(args):
    image_batch = args[0]
    dir_path,out,fourcc,fps,vid_width,vid_height,batch_quantity = args[1]
    batch_out=cv2.VideoWriter(str(image_batch[0])+out,fourcc,fps,(vid_width,vid_height),True)
    print("writing img {} + next {} to video object".format(image_batch[0],batch_quantity))

    for img in image_batch:
        image_path=os.path.join(dir_path,img)
        # read frame
        frame=cv2.imread(image_path)
        # resize=cv2.resize(oriimg,(1920,1080))
        batch_out.write(cv2.resize(frame,(vid_width,vid_height)))
        # cv2.waitKey(1)

    batch_out.release()

# converts images dir_path directory to specified video format
def directory_conversion_video(dir_path,ext,out,fourcc,fps,vid_width,vid_height,time_range):
     # collect and sort image files from current directory
    images=collect_img(dir_path,ext,time_range)
    # Parallelizaiton
    # Here we run multiple processes to resize each frame and output a separate video (we then combine the videos into a master one)
    #    
    #we determine the number of videos to produce based on how many cpu cores at our disposal (by making a list of a set amount of lists)
    batch_quantity = int(len(images)/multiprocessing.cpu_count())+1 #we want this distributed over the cores
    # pass all the necessary arguments in this pythonic list [[list of image files],(tuple of const values)]
    images_batches = [(images[x:x+batch_quantity],(dir_path,out,fourcc,fps,vid_width,vid_height,batch_quantity)) for x in range(0, len(images), batch_quantity)]
    pool=Pool()
    pool.map(image_adding,images_batches)

    #populate array with tempfilenames to be erased later...
    videofiles=[]
    for image_batch in images_batches:    
        videofiles.append(str(image_batch[0][0])+out)

    output_write=cv2.VideoWriter(out,fourcc,fps,(vid_width,vid_height),True)

    #concatinates all the videos (see concatinate_mp4.py)
    #populates frames=[] with frame objects to be written to master video
    combine_mp4(videofiles,output_write)

    #writing frames to output
    # print("writing batched frames to final...")
    # for frame in frames:
    #     output_write.write(frame)
    # output_write.release()

    #erase temp files...
    for fname in videofiles:
        os.remove(os.path.join('.', fname))


def main():

    dir_path='.'
    # arg parser
    argp = argparse.ArgumentParser()
    argp.add_argument("-e","--extension", required=False,default='png',help="extension of photo, default will be 'png'.")
    argp.add_argument("-d","--directory",required=False,default='.',help="select directory of images, default is current directory.")
    argp.add_argument("-o","--output",required=False,default='default_out.mp4',help="output video file name default will be 'default_out.mp4' (program will use ffmpeg, so *.mp4).")
    argp.add_argument("-wi","--width",required=False,default=1920,help="enter width value, default is 1920.")
    argp.add_argument("-hi","--height",required=False,default=1080,help="enter height value, default is 1080.")
    argp.add_argument("-ow","--overwrite_out",action='store_true',help="name output after directory with .mp4 extension")
    argp.add_argument("-m","--mothership_deploy",action='store_true',help="convert all directories in given directory to video, then concatinate")
    # argp.add_argument("-st","--start-time",requied=False,default=7,help="Filter images based on time taken, range is ")
    args = vars(argp.parse_args())
    dir_path=args['directory']
    ext=args['extension']
    output_overwrite_flag=args['overwrite_out']
    out=args['output']
    vid_width=args['width']
    vid_height=args['height']
    mothership_deploy_flag=args['mothership_deploy']

    if output_overwrite_flag:
        out =dir_path.split('/')[-2]+'.mp4'

    # time range to collect images (will be replaced eventually)
    time_range=(7,19)
   
    # codec def, change this here if mp4 doesn't work for you
    # use lower case:
    fourcc=cv2.VideoWriter_fourcc(*'mp4v')
    # video FPS
    fps=25.0

    directory_conversion_video(dir_path,ext,out,fourcc,fps,vid_width,vid_height,time_range)

    #bandaid for creating an h264 encoding video.
    os.system("ffmpeg -i {} -f mp4 -vcodec libx264 -preset fast -profile:v main -acodec aac {} -hide_banner".format(out,'h264_'+out))

    print("video output is: {}".format(out))


if __name__ == '__main__':
    main()

