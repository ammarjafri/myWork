import cv2, datetime, time, os, threading
class Main:
    def __init__(self):
        self.home = "videos/"
        self.today_folder = ""
        self.font1, self.line1, self.color1, self.color2 = cv2.FONT_HERSHEY_PLAIN, cv2.LINE_AA, (32, 32, 32), (240, 240, 240)
        self.folder_checker()

    def my_thread(self,tar,arg=[]):
        threads = threading.Thread(target=tar,args=arg,daemon=True)
        threads.start() 


    def overlay(self,img,texts,x,y):
        cv2.putText(img, texts, (x, y), self.font1, 1.0, self.color1, 4, self.line1)
        cv2.putText(img, texts, (x-1, y), self.font1, 1.0, self.color2, 1, self.line1)
        

    def add_fps(self,img, fps):
        fps_text = 'FPS: {:.2f}'.format(fps)
        self.overlay(img,fps_text,11,20)
        

    def show_time(self,img):
        _, img_w, _ = img.shape
        taxis1 = img_w - 180
        times1 = self.today_date()
        times2 = self.now_time()
        self.overlay(img,times1,taxis1,20)
        self.overlay(img,times2,taxis1,40)
        


    def now_time(self):
        ntime = datetime.datetime.now().strftime("%H-%M-%S")
        return ntime

    def today_date(self):
        ntime = datetime.datetime.now().strftime("%d-%b-%Y")
        return ntime

    def folder_checker(self):
        today_d = self.today_date()
        self.today_folder = self.home+today_d
        if not os.path.exists(self.today_folder):
            os.makedirs(self.today_folder)
