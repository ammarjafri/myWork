import cv2, datetime, time, gpiozero, pysftp, threading
import numpy as np
import utlis
buzz = gpiozero.LED(17)
tic=time.time()
home_path = "/home/pi/"
hubid = 0
f = open(home_path+'DVR/config.txt')
data_value = f.readlines()
f.close()

for x in data_value:
    if "hubid=" in x:
        hubid = x.split('=')[1][:-1]

dims = {
    "480":(640,480),
    "600":(800,600),
    "768":(1024,768),
    "720":(1280,720),
    "960":(1280,960),
    "1600":(1920,1600),
    "1080":(1920,1080),
    }

save_path = home_path+"imgs/"
cap = cv2.VideoCapture(0)
widthImg,heightImg = dims["1600"] 
cap.set(3,widthImg)
cap.set(4,heightImg)
i=0

def upload_file(filename,file_to_send):
    while True:
        try:
            FTP_HOST, FTP_USER, FTP_PASS = ["52.214.240.108","sftp","P)O(I*U&A!S@D#F$@123"] 
            filename_where_send = '/motion_box/'+filename
            with pysftp.Connection(host=FTP_HOST, username=FTP_USER, password=FTP_PASS) as sftp:
                print("connected")
                sftp.put(file_to_send,filename_where_send)
            break
        except:
            pass

def my_thread(tar,arg=[]):
    threads = threading.Thread(target=tar,args=arg)
    threads.start()

while True:
    success, img = cap.read()
    imgGray = cv2.resize(img, dims["480"]) # RESIZE IMAGE
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # CONVERT IMAGE TO GRAY SCALE
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1) # ADD GAUSSIAN BLUR
    img_bf = cv2.bilateralFilter(imgGray,9,75,75)
    imgThreshold = utlis.thresf(imgBlur)
    imgThreshold2 = utlis.thresf(img_bf)
    img_1 = utlis.is_cont(imgThreshold)
    img_2 = utlis.is_cont(imgThreshold2)
    toc=time.time()
    fps=1/toc-tic
    print(fps)
    if img_1 or img_2:
        differ = toc-tic
        if differ >= 2.2:
            tic=toc
            time_now = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
            filename = hubid+'_'+time_now+'.jpeg'
            file_save = save_path+filename
            # print(save)
            i=0
            # cv2.imwrite(save,img)
            # buzz.on()
            # my_thread(upload_file,[filename,file_save])
            # time.sleep(2)
            # buzz.off()
    # tic=toc
    key = cv2.waitKey(1)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()