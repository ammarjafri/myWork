import time, datetime, cv2, imutils,os
# from saver import saver

file_type = 'mp4'
frames_per_second = 24.0
my_res = '720p'

dims =  {
    "480": (640, 480),
    "600": (800, 600),
    "768": (1024, 768),
    "720": (1280, 720),
    "960": (1280, 960),
    "1600": (1920, 1600),
    "1080": (1920, 1080),
    "4k": (3840, 2160),
}

# Types of Codes: http://www.fopiurcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'MJPG'),
    'mp4': cv2.VideoWriter_fourcc(*'mp4v'),
}

def add_fps(img, fps):
    font = cv2.FONT_HERSHEY_PLAIN
    line = cv2.LINE_AA
    fps_text = 'FPS: {:.2f}'.format(fps)
    cv2.putText(img, fps_text, (11, 20), font, 1.0, (32, 32, 32), 4, line)
    cv2.putText(img, fps_text, (10, 20), font, 1.0, (240, 240, 240), 1, line)
    return img

def show_time(img):
    img_h, img_w, _ = img.shape
    font = cv2.FONT_HERSHEY_PLAIN
    line = cv2.LINE_AA
    sizes = 1.4
    color1 = (32, 32, 32)
    color2 = (240, 240, 240)
    times = datetime.datetime.now()
    times1 = str(times.strftime("%Y-%m-%d"))
    times2 = str(times.strftime("%H:%M:%S"))
    taxis1 = img_w - 180
    taxis2 = img_w - 179
    cv2.putText(img, times1, (taxis1, 20), font, sizes, color1, 4, line)
    cv2.putText(img, times1, (taxis2, 20), font, sizes, color2, 1, line)
    cv2.putText(img, times2, (taxis1, 40), font, sizes, color1, 4, line)
    cv2.putText(img, times2, (taxis2, 40), font, sizes, color2, 1, line)
    return img

def get_sec():
    tim = datetime.datetime.now()
    tim = tim.strftime("%S")
    return tim

# def record():
#     file_name, writer = sav.get_writ(file_type)
#     video_writer = cv2.VideoWriter(file_name, fourcc, 25, dims)
#     return video_writer

# sav = saver()
cap = cv2.VideoCapture(0)
# dims = get_dims(cap,res=my_res)
# fourcc = get_video_type(file_type)
tic = time.time()
ptime = tic
start_sec = get_sec()
# vide = record()
while True:
    _, img = cap.read()
    # img = imutils.resize(img,height=480)
    # img = cv2.resize(img,(640,480))
    toc = time.time()
    fps = 1 / (toc - tic)
    # dif = tic - ptime
    tic = toc
    # sav.update(img)
    now_sec = get_sec()
    img = add_fps(img, fps)
    img = show_time(img)
    # if start_sec == "00":
    #     if now_sec == "00" and dif >= 58:
    #         ptime = toc
    #         vide = record()
    #     else:
    #         vide.write(img)
    #         # sav.Videorecord()
    # else:
    #     if now_sec == "00":
    #         start_sec = "00"
    #         ptime = toc
    #         vide = record()
    #     else:
    #         vide.write(img)
    #         # sav.Videorecord()
    #         # ptime = -60
    cv2.imshow("image", img)
    key = cv2.waitKey(1)
    if key == 27:  # ESC key: quit program
        break

cap.release()
cv2.destroyAllWindows()
