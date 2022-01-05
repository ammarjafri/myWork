import datetime, os
home_path = '/home/pi/motioneye/Camera'
cam=0
f = open('/home/pi/DVR/config.txt')
data = f.read()
data = data.split('\n')
f.close()
for x in data:
    index = x.find('cams=')
    if(index != -1):
        value=x[len('cams='):len(x)]
        try:            
            cam=int(value)
        except:
            print('error in config.txt file')

def timecheck(check_time,filenamed):
    now_time = datetime.datetime.now()
    now_time = now_time.strftime("%Y%m%d-%H%M")
    check_days, check_times = check_time.split('-')
    now_days, now_times = now_time.split('-')
    dele = "sudo rm -rf " + filenamed
    if int(now_days) > int(check_days):
        if int(now_days) - int(check_days) > 1:
            os.system(dele)
        else:
            if int(now_times) > int(check_times):
                os.system(dele)

def remove_merge(cam):
    f_path = home_path+cam+'/'
    for folder in sorted(os.listdir(f_path)):
        for f in sorted(os.listdir(f_path+folder)):
            if f.endswith(".mp4"):
                if f[:3] == 'Req':
                    tts = f.split('.')[0]
                    tts = tts.split('_')[2]
                    timecheck(tts,f_path+folder+'/'+f)

if cam>=1:
    remove_merge('1')
if cam>=2:
    remove_merge('2')
if cam>=3:
    remove_merge('3')
if cam>=4:
    remove_merge('4')
