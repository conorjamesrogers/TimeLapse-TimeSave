import cv2
import os
# combines all mp4's specified in array of directory addresses, then returns an array of frame data.
def combine_mp4(video_file_array):

    capture= cv2.VideoCapture(video_file_array[0])
    video_index=0

    frames=[]

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
        frames.append(frame)

        # cv2.imshow('frame',frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
    print("...")

    capture.release()

    return frames

video_file_array = []
for f in os.listdir('.'):
    if f.endswith('mp4'):
        video_file_array.append(f)