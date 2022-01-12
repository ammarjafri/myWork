import cv2
import numpy as np
import utlis

dims = {
    "480":(640,480),
    "600":(800,600),
    "768":(1024,768),
    "720":(1280,720),
    "960":(1280,960),
    "1600":(1920,1600),
    "1080":(1920,1080),
    }
pathImage = "/home/pi/Scanner/amm/final_scan.jpeg"
cap = cv2.VideoCapture(1)
widthImg,heightImg = dims["1600"] 
cap.set(3,widthImg)
cap.set(4,heightImg)
i=101
utlis.initializeTrackbars()

def thresf(imgBlur,int1,int2):
    imgThreshold = cv2.Canny(imgBlur,20,200) # APPLY CANNY BLUR
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgThreshold, kernel, iterations=int1) # APPLY DILATION
    imgThreshold = cv2.erode(imgDial, kernel, iterations=int2)  # APPLY EROSION
    return imgThreshold

def draw_cont(img_col,img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
    # cv2.drawContours(img_col, contours, -1, (0, 255, 0), 10) # DRAW ALL DETECTED CONTOURS
    biggest, maxArea = utlis.biggestContour(contours) # FIND THE BIGGEST CONTOUR
    if biggest.size != 0:
        biggest=utlis.reorder(biggest)
        cv2.drawContours(img_col, biggest, -1, (0, 255, 0), 20) # DRAW THE BIGGEST CONTOUR
        img_col = utlis.drawRectangle(img_col,biggest,2)
    return img_col

while True:
    save = "testing"+str(i)+".jpeg"
    success, img = cap.read()
#     img = cv2.imread(pathImage)
    img = cv2.resize(img, dims["480"]) # RESIZE IMAGE
#     imgBlank = np.zeros((heightImg,widthImg, 3), np.uint8) # CREATE A BLANK IMAGE FOR TESTING DEBUGING IF REQUIRED
    img_1 = img_2 = img.copy()
    thres=utlis.valTrackbars()
    ker , iter_dial, iter_erode = thres
    ker = ker+1 if ker%2==0 else ker 
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # CONVERT IMAGE TO GRAY SCALE
    imgBlur = cv2.GaussianBlur(imgGray, (ker, ker), 1) # ADD GAUSSIAN BLUR
    img_bf = cv2.bilateralFilter(imgGray,9,75,75)
    # thres=utlis.valTrackbars() # GET TRACK BAR VALUES FOR THRESHOLDS
#     imgThreshold = cv2.Canny(imgBlur,thres[0],thres[1]) # APPLY CANNY BLUR
    imgThreshold = thresf(imgBlur,iter_dial,iter_erode)
    imgThreshold2 = thresf(img_bf,iter_dial,iter_erode)
#     ## FIND ALL COUNTOURS
#     imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
#     imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    img_1 = draw_cont(img_1,imgThreshold)
    img_2 =draw_cont(img_2,imgThreshold2)
# 
# 
#     # FIND THE BIGGEST COUNTOUR
    # biggest, maxArea = utlis.biggestContour(contours) # FIND THE BIGGEST CONTOUR
    # if biggest.size != 0:
    #     biggest=utlis.reorder(biggest)
    #     cv2.drawContours(img_1, biggest, -1, (0, 255, 0), 20) # DRAW THE BIGGEST CONTOUR
    #     imgBigContour = utlis.drawRectangle(img_1,biggest,2)
#         pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
#         pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
#         matrix = cv2.getPerspectiveTransform(pts1, pts2)
#         imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
# 
#         #REMOVE 20 PIXELS FORM EACH SIDE
#         imgWarpColored=imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
#         imgWarpColored = cv2.resize(imgWarpColored,(widthImg,heightImg))
# 
#         # APPLY ADAPTIVE THRESHOLD
#         imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
#         imgAdaptiveThre= cv2.adaptiveThreshold(imgWarpGray, 255, 1, 1, 7, 2)
#         imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
#         imgAdaptiveThre=cv2.medianBlur(imgAdaptiveThre,3)
# 
#         # Image Array for Display
#         imageArray = ([img,imgContours,imgWarpColored,imgBlank],
#                       [imgBigContour,imgBlank, imgWarpGray,imgAdaptiveThre])
# 
#     else:
#         imageArray = ([img,imgContours,imgBlank,imgBlank],
#                       [imgBlank, imgBlank, imgBlank, imgBlank])
# 
#     # LABELS FOR DISPLAY
#     lables = [["Original","Gray","Threshold","Contours"],
#               ["Biggest Contour","Warp Prespective","Warp Gray","Adaptive Threshold"]]
# 
#     stackedImage = utlis.stackImages(imageArray,0.75,lables)
#     cv2.imshow("Result",stackedImage)
    # output2 = cv2.resize(imgThreshold, (640, 480))
    cv2.imshow("output1",imgThreshold)
    cv2.imshow("output2",imgThreshold2)
    # cv2.imshow("output2",output2)
    cv2.imshow("input",img_1)
    cv2.imshow("input2",img_2)
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
