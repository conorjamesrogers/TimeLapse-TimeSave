# WHAMSTACK IT
# 'simple' script to convert directroy of imgs to video.
# By Conor Rogers
# 2019

import cv2
import argparse
import os
from multiprocessing import Pool, current_process
from operator import itemgetter
from moviepy.editor import VideoFileClip, concatenate_videoclips
import glob
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


# def concatenate():
#     stringa = "ffmpeg -i \"concat:"
#     elenco_video = glob.glob("*.mp4")
#     elenco_file_temp = []
#     for f in elenco_video:
#         file = "temp" + str(elenco_video.index(f) + 1) + ".ts"
#         os.system("ffmpeg -i " + f + " -c copy -f mpegts " + file)
#         elenco_file_temp.append(file)
#     print(elenco_file_temp)
#     for f in elenco_file_temp:
#         stringa += f
#         if elenco_file_temp.index(f) != len(elenco_file_temp)-1:
#             stringa += "|"
#         else:
#             stringa += "\" -c copy  -bsf:a aac_adtstoasc " + out
#     print(stringa)
#     os.system(stringa)
 


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

# print(images)
# get width/height from first image
img_path=os.path.join(dir_path,images[0])
frame=cv2.imread(img_path)
# cv2.imshow('video',frame)
height,width,channels=frame.shape

# codec def, change this here if mp4 doesn't work for you
# use lower case:
fourcc=cv2.VideoWriter_fourcc(*'mp4v')
# fourcc=cv2.VideoWriter_fourcc(*'xvid')
# fourcc = 0x34363248
fps=25.0
# VideoWriter(str<ouput path>,<fourcc codec>,double<fps of video>,tuple<width,height>)

# loop for writing each image to a frame of video.
# if you were to parallelize this... run this loop on separate images and outputs then combine the outputs.
images_batches = [images[x:x+100] for x in range(0, len(images), 100)]
videofiles=[]
def image_adding(image_batch,output_str=''):
    batch_out=cv2.VideoWriter(str(image_batch[0])+out,fourcc,fps,(1920,1080),True)
    print("writing img {} + next 100 to video object".format(image_batch[0]))

    for img in image_batch:
        image_path=os.path.join(dir_path,img)
        # read frame
        frame=cv2.imread(image_path)
        # resize=cv2.resize(oriimg,(1920,1080))
        batch_out.write(cv2.resize(frame,(1920,1080)))
        cv2.waitKey(1)

        # frame=cv2.imread(img[1])
        # write frame to video
        # output_write=cv2.VideoWriter(out,fourcc,25.0,(width,height))


    batch_out.release()
    # output_write.write(frame)

# video_write=[]
pool=Pool()
pool.map(image_adding,images_batches)

# concatenate()

# now to combine the videos...
# videofiles = [n for n in os.listdir('.') if n[0]=='S' and n[-13:]=='.mp4']
# videofiles = sorted(videofiles, key=lambda item: int( item.partition('.')[0][3:]))
for image_batch in images_batches:    
#     videofiles.append(VideoFileClip(str(image_batch[0])+out))
    videofiles.append(str(image_batch[0])+out)
# print("concatenating...")
# final_clip = concatenate_videoclips(videofiles)
# final_clip.write_videofile(out)
output_write=cv2.VideoWriter(out,fourcc,fps,(1920,1080),True)

capture= cv2.VideoCapture(videofiles[0])
video_index=0

frames=[]

while(capture.isOpened()):
    ret, frame = capture.read()
    if frame is None:
        print("end of video " + str(video_index) + " .. next one now")
        video_index += 1
        if video_index >= len(videofiles):
            break
        capture.release()
        capture = cv2.VideoCapture(videofiles[ video_index ])
        ret, frame = capture.read()
        # if not  ret:
        #     break
    frames.append(frame)

    # cv2.imshow('frame',frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
print("...")

capture.release()

for frame in frames:
    output_write.write(frame)
    cv2.waitKey(1)

output_write.release()




# print(video_write)
# sorted(video_write,key=itemgetter(1))
# print(video_write)
# for n, frame, img in enumerate(video_write):
#     output_write.write(frame)
#     if n%100==0:
#         print("finished writing first to img {} to frame".format(img))

# for n, img in enumerate(images):
#     image_path=os.path.join(dir_path,img)
#     # read frame
#     frame=cv2.imread(image_path)
#     # frame=cv2.imread(img)
#     # write frame to video
#     output_write.write(frame)
#     if n%100==0:
#         print("finished writing first to img {} to frame".format(img))

    # cv2.imshow('video',frame)
    # press q to exit
    # if(cv2.waitKey(1) & 0xFF) == ord('q'):
    #     break


for fname in videofiles:
    os.remove(os.path.join(dir_path, fname))

print("video output is: {}".format(out))