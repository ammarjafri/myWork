import cv2,threading
cap = cv2.VideoCapture(0)
dims = {
    "480":(640,480),
    "480_2":(800,480),
    "600":(800,600),
    "576":(1024,576),
    "600":(1024,600),
    "768":(1024,768),
    "720":(1280,720),
    "768_2":(1280,768),
    "800":(1280,800),
    "960":(1280,960),
    "1020":(1280,1020),
    "960_2":(1440,960),
    "1024":(1440,1024),
    "1200":(1600,1200),
    "1080":(1920,1080),
    }
global widthImg,heightImg
    
widthImg,heightImg=dims['480']
def set_sizes():
    while (True):
        global widthImg,heightImg
#         a = input("enter size: ")
        widthImg,heightImg=dims[a]
#         cap.set(3,widthImg)
#         cap.set(4,heightImg)
# asd = threading.Thread(target=set_sizes)
# asd.start()
cap.set(3,1920)
cap.set(4,1600)
i=1018

while True:
    save = "testing"+str(i)+".jpeg"
    _,img = cap.read()
#     img = cv2.resize(img, (widthImg, heightImg))
#     print(img.shape)
    cv2.imshow("img",img)
    cv2.imshow("roi",img[0:100,0:100])
    key = cv2.waitKey(1)
    if key == ord('s'):
        cv2.imwrite(save,img)
        print(save)
        print("save done!")
        i+=1
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
