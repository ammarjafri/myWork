import os, time, subprocess, datetime,threading
home = "/home/pi/"
cams = "motioneye/Camera"
mou = "null"
cam_fold_1 = home+cams+'1/'
cam_fold_2 = home+cams+'2/'
dels = "sudo rm -rf /media/pi/*"
os.system(dels)

def autoremove(usb):
    home = usb
    f = open('/home/pi/'+'DVR/config.txt')
    data = f.read()
    data = data.split('\n')
    totalCam = 0
    f.close()

    for x in data:
        index = x.find('cams=')
        if(index != -1):
            value=x[len('cams='):len(x)]
            try:            
                cam=int(value)
            except:
                print('error in config.txt file')

    cam1 = home+'motioneye/Camera1/'
    cam2 = home+'motioneye/Camera2/'
    cam3 = home+'motioneye/Camera3/'
    cam4 = home+'motioneye/Camera4/'

    def folder(fpath):
        for f in sorted(os.listdir(fpath)):
            break
        return f

    def splitss(timing,fold):
        try:
            tim = datetime.datetime.strptime(timing,"%Y-%m-%d")
            return tim
        except:
            deles = "sudo rm -rf "+fold+timing
            os.system(deles)

    root_size = subprocess.check_output("df -h | grep /dev/sda1 | head -1 | awk -F' ' '{ print $5/1 }' | tr ['%'] ['0']",shell=True)
    root_size = root_size.decode()
    print(root_size)
    try:
        if cam>=1:
            f_cam1 = folder(cam1)
            time1 = splitss(f_cam1,cam1)
            del1 = 'sudo rm -rf '+cam1+f_cam1
        if cam>=2:
            f_cam2 = folder(cam2)
            time2 = splitss(f_cam2,cam2)
            del2 = 'sudo rm -rf '+cam2+f_cam2
        if cam>=3:
            f_cam3 = folder(cam3)
            time3 = splitss(f_cam3,cam3)
            del3 = 'sudo rm -rf '+cam3+f_cam3
        if cam>=4:
            f_cam4 = folder(cam4)
            time4 = splitss(f_cam4,cam4)
            del4 = 'sudo rm -rf '+cam4+f_cam4

        if int(root_size) >= 98:
            if cam==1:
                os.system(del1)
            if cam==2:
                if time1 == time2:
                    os.system(del1)
                    os.system(del2)
                if time1 < time2:
                    os.system(del1)
                if time2 < time1:
                    os.system(del2)
            if cam==3:
                if time1 == time2 and time1 == time3:
                    os.system(del1)
                    os.system(del2)
                    os.system(del3)
                if time1 < time2 or time1 < time3:
                    os.system(del1)
                if time2 < time1 or time2 < time3:
                    os.system(del2)
                if time3 < time1 or time3 < time2:
                    os.system(del3)
            if cam==4:
                if time1 == time2 and time1 == time3 and time1 ==time4:
                    os.system(del1)
                    os.system(del2)
                    os.system(del3)
                    os.system(del4)
                if time1 < time2 or time1 < time3 or time1 < time4:
                    os.system(del1)
                if time2 < time1 or time2 < time3 or time2 < time4:
                    os.system(del2)
                if time3 < time1 or time3 < time2 or time3 < time4:
                    os.system(del3)
                if time4 < time1 or time4 < time2 or time4 < time3:
                    os.system(del4)
    except Exception as e:
        print(e)


def get_usb_location():
    fil = subprocess.check_output("df -h | grep /dev/sda1 | head -1 | awk -F' ' '{ print $6 }'",shell=True)
    fil = fil.decode()
    
    if fil !="":
        files = fil[:-1]+'/'
        return files
    else:
        return "null"


def get_today():
    today = datetime.datetime.now()
    day = today.strftime("%Y-%m-%d")
    return day


def mount_check(name,usb):
    path1 = "/dev/sda1"
    path2 = "/media/pi/"
    mou = subprocess.check_output("sudo blkid | grep /dev/sda1 | head -1 | awk -F' ' '{ print $2 }'",shell=True)
    mou = mou.decode()
    if name == "null":        
        if mou !="":
            moun = mou[:-1]
            moun = (moun.split('=')[1])[1:-1]
            nam = path2+moun+'/'
            if not os.path.exists(nam):
                os.makedirs(nam)
            com = "sudo mount "+path1+" "+nam
            os.system(com)
            return nam
            
        else:
            return "null"
    else:
        if mou=="":
            if usb!="null":
                uncom = "sudo umount "+path1
                os.system(uncom)
                dele = 'sudo rm -rf '+path2+'*'
                os.system(dele)
            return "null"
        else:
            return name


class done(Exception):
    pass


def copy_now(video_path,videos,usb_path):
    video = video_path+videos
    usb_video = usb_path+videos
    if videos.endswith(".mp4"):
        if not os.path.isfile(usb_video):
            copy_command = "sudo cp "+video +" "+usb_video
            print(copy_command)
            at= time.time()
            os.system(copy_command)
            bt =time.time()-at
            print(bt)
            return True
    return False

def verify(usb,home):
    try:
        for files in sorted(os.listdir(home)):
            usb_path = usb+files+'/'
            video_path = home+files+'/'
            today = get_today()
            
            if not os.path.exists(usb_path):
                os.makedirs(usb_path)
            if today != files:
                for videos in sorted(os.listdir(video_path)):
                    checks = copy_now(video_path,videos,usb_path)
                    if checks:
                        raise done
            else:
                for videos in sorted(os.listdir(video_path))[:-2]:
                    checks = copy_now(video_path,videos,usb_path)
                    if checks:
                        raise done
    except done:
        pass
while True:
    usb = get_usb_location()
    mou = mount_check(mou,usb)
    if usb != "null" and mou!="null":
        threadingTask = threading.Thread(target=autoremove,args=[usb])
        threadingTask.start()        
        usb_fold_1 = usb+cams+'1/'
        usb_fold_2 = usb+cams+'2/'
        verify(usb_fold_1,cam_fold_1)
        verify(usb_fold_2, cam_fold_2)
#         break
    time.sleep(2)