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
# utlis.initializeTrackbars()

while True:
    save = "testing"+str(i)+".jpeg"
    success, img = cap.read()
    print(img.shape)
#     img = cv2.imread(pathImage)
    img = cv2.resize(img, dims["720"]) # RESIZE IMAGE
#     imgBlank = np.zeros((heightImg,widthImg, 3), np.uint8) # CREATE A BLANK IMAGE FOR TESTING DEBUGING IF REQUIRED
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # CONVERT IMAGE TO GRAY SCALE
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1) # ADD GAUSSIAN BLUR
    
#     thres=utlis.valTrackbars() # GET TRACK BAR VALUES FOR THRESHOLDS
#     imgThreshold = cv2.Canny(imgBlur,thres[0],thres[1]) # APPLY CANNY BLUR
    # imgThreshold = cv2.Canny(imgBlur,20,200) # APPLY CANNY BLUR
    # kernel = np.ones((5, 5))
    # imgDial = cv2.dilate(imgThreshold, kernel, iterations=2) # APPLY DILATION
    # imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # APPLY EROSION
# 
#     ## FIND ALL COUNTOURS
#     imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
#     imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
#     contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
#     cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10) # DRAW ALL DETECTED CONTOURS
# 
# 
#     # FIND THE BIGGEST COUNTOUR
#     biggest, maxArea = utlis.biggestContour(contours) # FIND THE BIGGEST CONTOUR
#     if biggest.size != 0:
#         print("true")
#         biggest=utlis.reorder(biggest)
#         cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 20) # DRAW THE BIGGEST CONTOUR
#         imgBigContour = utlis.drawRectangle(imgBigContour,biggest,2)
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
    output1 = cv2.resize(imgBlur, (640, 480))
    # output2 = cv2.resize(imgThreshold, (640, 480))
    cv2.imshow("output1",output1)
    # cv2.imshow("output2",output2)
    cv2.imshow("input",img)
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
