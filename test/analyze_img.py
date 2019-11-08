# WHAMSTACK IT 
# To remove images with certain timestamps (ideally night photography) from directory.
# By Conor Rogers
# 2019

import os.path
from os import path
from PIL import Image
from PIL import ExifTags
from datetime import datetime
import time

# temp messy paths
BASEPATH = '../../../Wolff_Contacting_Media/Dennis/'
TIME_FORMAT='%Y:%m:%d %H:%M:%S'

# perhaps the EXIF metadata holds the key...
# could use Luma for a precise measure, but the complexity of searching each photo!
# I would rather keep it O(n) if I could, (thousands of images), will use the date.

# we will want to figure out the time difference between the first 2 photos, 
# this will enable us to guess the time of day based on photo number.
# Due to application, any photo around the time before 7am and after 6pm wouldn't be used anyways. 
# Date discrepencies happen between battery changes, but we will just compile each folder into a video then combine all videos.


#debug information
def print_img(img,txt='img'):
    # f=open(txt,'w')
    # f.write(str(img._getexif()))
    # f.close()
    exif_data = img._getexif()
    print(txt,
        '\n format: ',img.format, 
        '\n mode: ', img.mode,
        '\n date: ', exif_data[36867])

def unix_time(dt):
    epoch = datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds()

#looks at first 2 photos, returns list of time delta in seconds, start time in seconds since unix epoch and datetime object start time
# start time is seconds since unix epoch for simplicity.
def determine_pattern(directory_path,time_format=TIME_FORMAT):
    if(path.exists(directory_path+'STC_0001.JPG') and path.exists(directory_path+'STC_0002.JPG')):
        img1=Image.open(directory_path+'STC_0001.JPG')
        img2=Image.open(directory_path+'STC_0002.JPG')

        date_img1=img1._getexif()[36867]
        start_time = datetime.strptime(date_img1, time_format)

        date_img2=img2._getexif()[36867]
        second_time = datetime.strptime(date_img2, time_format)

        epoch_seconds_start = unix_time(start_time)

       

        return[unix_time(second_time)-epoch_seconds_start,epoch_seconds_start,start_time]

        # delta=datetime.strptime(date_img2, time_format) - start_time
        # ftr = [3600,60,1]
        # delta_s=sum([a*b for a,b in zip(ftr, map(int,delta.split(':')))])
        # return (delta,datetime.strptime(date_img1, time_format))
    else:
        print('\nNO PATH FOUND \n')
        return -1

# def get_time(time_diff_pattern,img_name):
#     return int(img_name.split(r'[._]')[1])*



def main():
    # images always named "STC_<number>.JPG"
    # day_img = Image.open(BASEPATH + 
    #     'Dennis_Ln_9-3--9-5/STC_0001.JPG')
    # night_img = Image.open(BASEPATH + 
    #     'Dennis_Ln_9-3--9-5/STC_0177.JPG')

    # print_img(day_img,'day_img')
    # print_img(night_img,'night_img')
    time_diff_pattern=determine_pattern(BASEPATH+'Dennis_Ln_9-3--9-5/')
    print(time_diff_pattern)





if __name__ == '__main__':
    main()