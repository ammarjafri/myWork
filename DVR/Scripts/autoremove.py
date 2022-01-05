import subprocess, os, datetime, logging
home = '/home/pi/'
f = open(home+'DVR/config.txt')
data = f.read()
data = data.split('\n')
totalCam = 0
f.close()
logging.basicConfig(level=logging.INFO,filename="/home/pi/DVR/ELogs/autoremove.log", format='%(asctime)s - %(message)s',datefmt='%y-%b-%d %H:%M:%S')

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

root_size = subprocess.check_output("df -h | grep /dev/root | head -1 | awk -F' ' '{ print $5/1 }' | tr ['%'] ['0']",shell=True)
root_size = root_size.decode()
print(root_size)

if int(root_size) >= 96:
    os.system("sudo systemctl stop motioneye")
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

    if int(root_size) >= 92:
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
    logging.error('error = ' +str(e))
