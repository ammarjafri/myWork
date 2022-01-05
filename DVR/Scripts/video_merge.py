import os, re, requests, time, datetime, logging
logging.basicConfig(level=logging.INFO,filename="/home/pi/DVR/ELogs/merge.log", format='%(asctime)s - %(message)s',datefmt='%y-%b-%d %H:%M:%S')
f = open('/home/pi/DVR/config.txt')
data = f.readlines()
f.close()
hubid=-1
for x in data:
    if "hubid" in x:
        hubid = x.split('=')[1][:-1]

home_path = '/home/pi/motioneye/Camera'
my_https = "connect-srvc.monit.tech"

def converter(timings):
    timing = timings.split('"')[3]
    date, times = timing.split('T')
    hour, mint, sec = times.split(':')
    times = hour+'-'+mint
    return date, times, int(hour), int(mint)


def merger(vn,fp):
    saving="sudo mkvmerge -o "+vn
    isVideo = False
    for i in range(0,timing+1):
        video=start_timess+datetime.timedelta(minutes=i)
        video=str(video.strftime("%H-%M"))
        for files in os.listdir(fp):
            if re.match(video,files) and files.endswith(".mp4"):
                saving+= ' '+fp+files+' \+'
                isVideo = True
    saving=saving[:-2]
    return  isVideo, saving

def api_hit(req_id,hubid,f_name,status_id):
    link='http://'+my_https+'/api/UpdateVideoRequestStatus/?id='+req_id+'&&hubid='+hubid+\
        '&&filename='+f_name+'&&Statusid='+status_id
#     print(link)
    res = requests.get(link)
    logging.error(f_name+' '+status_id+' '+res.status_code)


while(True):
    try:
        success = False
        url_link='http://'+my_https+'/api/Getvideorequest/?hubid='+hubid
        n = requests.get(url=url_link, timeout=5)
        n.encoding='utf-8'
        tex=n.text
        if tex != '0':
            print(tex)
            a = tex[2:-2]
            req_id, camera, froms, tos = a.split(',')
            req_id = req_id.split(':')[1]
            camera = camera.split(':')[1]
            date,start_time,hour_start,mint_start = converter(froms)
            date,end_time,hour_end,mint_end = converter(tos)
            final_path=home_path+camera+'/'+date+'/'
            start_timess=datetime.datetime.strptime(start_time,"%H-%M")
            hours_of_video=hour_end-hour_start
            if hours_of_video>=1:    
                first_half=60-mint_start
                timing=mint_end+first_half
            else:
                timing=mint_end-mint_start
            now_timings = datetime.datetime.now().strftime("%Y%m%d-%H%M")
            f_name="Req"+"_"+start_time+"-"+end_time+"_"+now_timings+".mp4"
            video_name=final_path+f_name
            if os.path.isfile(video_name):
                api_hit(req_id,hubid,f_name,"1")
                success = True
            else:
                if os.path.exists(final_path):
                    success, merge_command = merger(video_name,final_path)
                    if success:
                        os.system(merge_command)
                        api_hit(req_id,hubid,f_name,"1")
            if not success:
                api_hit(req_id,hubid,f_name,"2")
        time.sleep(1)
    except Exception as e:
        logging.error('error = ' +str(e))