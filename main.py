import time, datetime, cv2, imutils,os
from utils import Main
# from saver import saver
my_main = Main()
# file_type = 'mp4'
# frames_per_second = 24.0
# my_res = '720p'

dims =  {
    "360": (640, 360),
    "480": (640, 480),
    "448": (800, 448),
    "600": (800, 600),
    "576": (1024, 576),
    "720_2": (960, 720),
    "768": (1024, 768),
    "720": (1280, 720),
    "960": (1280, 960),
    "896": (1600, 896),
    "960_2": (1712, 960),
    "1008": (1792, 1008),
    "1600": (1920, 1600),
    "1080": (1920, 1080),
    "4k": (3840, 2160),
}

# Types of Codes: http://www.fopiurcc.org/codecs.php
# # VIDEO_TYPE = {
# #     'avi': cv2.VideoWriter_fourcc(*'MJPG'),
# #     'mp4': cv2.VideoWriter_fourcc(*'mp4v'),
# # }

cap = cv2.VideoCapture(1)
widthImg, heightImg = dims["720"]
# print(widthImg,heightImg)
cap.set(3,widthImg)
cap.set(4,heightImg)
tic = time.time()

while True:
    _, img = cap.read()
    # print(img.shape)
    # img = imutils.resize(img,height=480)
    # img = cv2.resize(img,(640,480))
    toc = time.time()
    fps = 1 / (toc - tic)
    tic = toc
    my_main.add_fps(img, fps)
    my_main.show_time(img)

    cv2.imshow("image", img)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
