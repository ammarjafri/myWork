import socket, subprocess, os, re, requests, urllib.request, getpass, threading, datetime, pysftp, logging, time
from datetime import date;
import constants as Const
home_path = "/home/pi/"
logging.basicConfig(level=logging.INFO, filename=home_path+"DVR/ELogs/heartbeat.log", format='%(asctime)s - %(message)s', datefmt='%y-%b-%d %H:%M:%S')
my_https = "connect-srvc.monit.tech"
host = ""
port = 5555
port2 = 5556
port3 = 5558
auth_user = 'admin'
auth_passwd = 'camosg123'
cornerCountL = cornerCountR = totalCam = hubid = motionBox = camSwitch = gpsLog = isSeatBelt = isIgnition = 0
nodeData = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
eventState = lastEvent = lat = long = speed = '0'
sbOld = igOld = sbData = igData = '1'
eventUrl = data = ''
eventName = '.'
eFlag = False
totalCam = 0

f = open(home_path+'DVR/config.txt')
data_value = f.readlines()
f.close()

def get_value(val):
    val = val + "="
    for x in data_value:
        if val in x:
            final = x.split('=')[1][:-1]
    return int(final)


totalCam = get_value("cams")
hubid = str(get_value("hubid"))
motionBox = get_value("motion")
camSwitch = get_value("camswitch")
gpsLog = get_value("gpslog")
isSeatBelt = get_value("seatbelt")
isIgnition = get_value("ignition")

def isactive(ipaddress, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((ipaddress, port))
        connected = True
    except:
        connected = False
    finally:
        s.close()
    return connected

def api_hit(val,DeviceDT,lat,long,speed):
    newURL = "http://"+my_https+"/api/SetDeviceHeartBeat?hubid=" + \
        hubid + "&&servertime=" + DeviceDT + "&&lat=" + lat + "&&long=" +\
             long + "&&alt=0.0&&speed=" + str(speed) + "&&eventtypeid=" + val
    requests.get(newURL)

def eventCheck(sb, ig, DeviceDT, lat, long, speed):
    global igOld, sbOld
    if isIgnition == 1:
        if igOld != ig:
            if int(ig) == 1:
                api_hit('9',DeviceDT,lat,long,speed)
            if int(ig) == 0:
                api_hit('8',DeviceDT,lat,long,speed)
    if isSeatBelt == 1:
        if sbOld != sb:
            if int(sb) == 1:
                api_hit('11',DeviceDT,lat,long,speed)
            if int(sb) == 0:
                api_hit('10',DeviceDT,lat,long,speed)
    sbOld = sb
    igOld = ig

def GPSRequest():
    global  lat, long, speed, sbData, igData
    try:
        DeviceDT = date.today().strftime("%Y-%m-%d") + 'T' + time.strftime("%H:%M:%S")
        ipcabin, ipfront, ipright, ipleft = '192.168.15.90','192.168.15.95','192.168.15.100','192.168.15.105'
    
        cabin = "true" if isactive(ipcabin, 554) else "false"
        front = "true" if isactive(ipfront, 554) else "false"
        right = "true" if isactive(ipright, 554) else "false"
        left = "true" if isactive(ipleft, 554) else "false"

        newURL = "http://"+my_https+"/api/SetDeviceHeartBeat?hubid=" + hubid + "&&servertime=" + \
            DeviceDT + "&&lat=" + lat + "&&long=" + long + "&&alt=0.0&&speed=" + \
            str(speed) + "&&cabin=" + cabin + "&&front=" + front + "&&left=" + left + "&&right=" + right
        # print(newURL)
        logging.error("speed = "+str(speed)+" , lat = "+str(lat)+" , long = "+str(long)+" , cabin = "+cabin+" , front = "+front)
        x = requests.get(newURL)
        eventCheck(sbData, igData,DeviceDT,lat,long,speed)
        if x.status_code != 200:
            ct = str(datetime.datetime.now())
            f = open(home_path+'DVR/ELogs/GPSRequestStatusCode.txt', 'w')
            f.write(ct + ' ' + x.status_code)
            f.close()
    except KeyboardInterrupt:
        pass
    except Exception as error:
        ct = str(datetime.datetime.now())
        f = open(home_path+'DVR/ELogs/GPSRequest.txt', 'w')
        f.write(ct + ' ' + str(error))
        f.close()

def GPSTask():
    threadingTask = threading.Thread(target=GPSRequest)
    threadingTask.start()


def getfilename(fol, vid):
    if len(os.listdir(fol)) > 0:
        for f in os.listdir(fol):
            if re.match(vid, f) and f.endswith(".mp4"):
                return f
        return 'null'
    else:
        return 'null'
def GetFileName(rawDate, rawTime, camera):
    pathName = home_path+'motioneye/Camera' + camera + '/'  ##To DO
    pathName = pathName + rawDate + '/'
    if not os.path.exists(pathName):
        return 'null'
    rawTimes = rawTime.split(':')
    rawTime = rawTimes[0] + "-" + rawTimes[1]
    try:
        video_name = getfilename(pathName, rawTime)
        if video_name == 'null':
            return 'null'
        sec = os.path.splitext(video_name)[0]
        sec = sec.split('-')[2]
        if int(rawTimes[2]) > int(sec):
            return pathName + video_name
        else:
            ntime = datetime.datetime.strptime(rawTime, "%H-%M")
            ntime = ntime - datetime.timedelta(minutes=1)
            ntime = ntime.strftime('%H-%M')
            new_video_name = getfilename(pathName, ntime)
            if new_video_name == 'null':
                return 'null'
            return pathName + new_video_name
    except Exception as error:
        ct = str(datetime.datetime.now())
        f = open(home_path+'DVR/ELogs/GetFileName.txt', 'w')
        f.write(ct + ' ' + str(error))
        f.close()
        return 'null'

def UploadFileThread(fileNameToSend, fileNameToFetch):
    try:
        FTP_HOST = "52.214.240.108"
        FTP_USER = "sftp"
        FTP_PASS = "P)O(I*U&A!S@D#F$@123"
        fileNameSent = "/motion_box/" + fileNameToSend
        with pysftp.Connection(host=FTP_HOST, username=FTP_USER, password=FTP_PASS) as sftp:
            print("connected")
            sftp.put(fileNameToFetch,fileNameSent)
    except KeyboardInterrupt:
        pass
    except Exception as error:
        ct = str(datetime.datetime.now())
        f = open(home_path+'DVR/ELogs/UploadFileThread.txt', 'w')
        f.write(ct + ' ' + str(error))
        f.close()
def UploadFile(fileName, event_id, camera, date, times):
    try:
        times = times.split(':')
        times = times[0] + "-" + times[1]
        sendFileName = hubid + "_" + str(event_id) + "_" + str(camera) + "_" + date + "_" + times + ".mp4"
        fileToFetch = fileName
        uploadThread = threading.Thread(target=UploadFileThread, args=[sendFileName, fileToFetch])
        uploadThread.start()
        return sendFileName
    except KeyboardInterrupt:
        pass
    except Exception as error:
        ct = str(datetime.datetime.now())
        f = open(home_path+'DVR/ELogs/UploadFile.txt', 'w')
        f.write(ct + ' ' + str(error))
        f.close()

def delayedService(datess, times, event, speed):
    global  lat, long
    DeviceDT = datess + 'T' + times
    fileName1 = GetFileName(datess, times, '1')
    fileName2 = GetFileName(datess, times, '2')
    fileName3 = GetFileName(datess, times, '3')
    fileName4 = GetFileName(datess, times, '4')
    print(fileName1, fileName2)
    try:
        if (fileName1 != 'null') or (fileName2 != 'null') or (fileName3 != 'null') or (fileName4 != 'null'):
            if fileName1 != 'null':
                sendFileName1 = UploadFile(fileName1, event, '1', datess, times)
            else:
                sendFileName1 = 'null'
            if fileName2 != 'null':
                sendFileName2 = UploadFile(fileName2, event, '2', datess, times)
            else:
                sendFileName2 = 'null'
            if fileName3 != 'null':
                sendFileName3 = UploadFile(fileName3, event, '3', datess, times)
            else:
                sendFileName3 = 'null'
            if fileName4 != 'null':
                sendFileName4 = UploadFile(fileName4, event, '4', datess, times)
            else:
                sendFileName4 = 'null'

            eventUrL = "http://"+my_https+"/api/SetDeviceHeartBeat?hubid=" +hubid +\
                "&&servertime=" + DeviceDT + "&&lat=" + lat + "&&long=" + long +\
                "&&alt=0.0&&speed=" + str(speed) + "&&eventtypeid=" + event + "&&filefront=" +\
                sendFileName1 + "&&filecabin=" + sendFileName2 + "&&fileleft=" + sendFileName3 + "&&fileright=" + sendFileName4
            print(eventUrL)
            r = requests.get(eventUrL)
    except KeyboardInterrupt:
        pass
    except Exception as error:
        ct = str(datetime.datetime.now())
        f = open(home_path+'DVR/ELogs/delayedService.txt', 'w')
        f.write(ct + ' ' + str(error))
        f.close()

def GetDateTime():
    readable = datetime.datetime.now()
    date = readable.strftime("%Y-%m-%d")
    times = readable.strftime("%H:%M:%S")
    return date, times

def runTask(event, speed):
    try:
        print('event occur')
        print(event)
        date, times = GetDateTime()
        start_time = threading.Timer(120, delayedService, args=[date, times, event, speed])
        start_time.start()
    except KeyboardInterrupt:
        pass
    except Exception as error:
        ct = str(datetime.datetime.now())
        f = open(home_path+'DVR/ELogs/runTask.txt', 'w')
        f.write(ct + ' ' + str(error))
        f.close()

def MotionEvent():
    global eventState, speed
    while True:
        try:
            time.sleep(0.1)
            if eventState != '0':
                runTask(eventState, speed)
                time.sleep(30)
            else:
                pass
        except KeyboardInterrupt:
            break
        except Exception as error:
            print(error)
            ct = str(datetime.datetime.now())
            f = open(home_path+'DVR/ELogs/MotionEvent.txt', 'w')
            f.write(ct + ' ' + str(error))
            f.close()


def MotionOverlay():
    global eventState, lastEvent, eventName
    while True:
        try:
            time.sleep(0.1)
            if eventState != lastEvent:
                lastEvent = eventState  # 0=no event, 1=Harsh Accel, 2=Harsh Brake, 3=Harsh Corner R, 4=Harsh Corner L
                if eventState == '1':
                    eventName = 'HARSH%20ACCELERATION'
                elif eventState == '2':
                    eventName = 'HARSH%20BRAKE'
                elif eventState == '3':
                    eventName = 'HARSH%20CORNER'
                elif eventState == '4':
                    eventName = 'HARSH%20CORNER'
                elif eventState == '5':
                    eventName = 'OVER%20SPEEDING'
                time.sleep(5)
                lastEvent = '0'
                eventName = '.'
        except KeyboardInterrupt:
            break
        except Exception as error:
            ct = str(datetime.datetime.now())
            f = open(home_path+'DVR/ELogs/MotionOverlay.txt', 'w')
            f.write(ct + ' ' + str(error))
            f.close()


def CheckEvent():
    global cornerCountR, cornerCountL
    try:
        event = '0'
        if float(nodeData[3]) > Const.MAX_SPEED:
            event = '5'
        elif float(nodeData[3]) - float(nodeData[2]) > Const.MAX_ACCEl_GPS:
            event = '1'
        elif float(nodeData[2]) - float(nodeData[3]) > Const.MAX_DECL_GPS:
            event = '2'
        elif float(nodeData[3]) > Const.MIN_SPEED:
            if (nodeData[5]) > Const.AYP:
                cornerCountR += 1
                if cornerCountR > 5:
                    event = '3'
                else:
                    event = '0'
            elif (nodeData[5]) < Const.AYN:
                cornerCountL += 1
                if cornerCountL > 5:
                    event = '3'
                else:
                    event = '0'
            else:
                cornerCountR = 0
                cornerCountL = 0

        return event
    except KeyboardInterrupt:
        pass
    except Exception as error:
        ct = str(datetime.datetime.now())
        f = open(home_path+'DVR/ELogs/CheckEvent.txt', 'w')
        f.write(ct + ' ' + str(error))
        f.close()
        return '0'

def rec_UDP():
    try:
        serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSock.bind((host, port))
        global lat, long, speed, nodeData, eventState, eFlag, sbData, igData
        yCount = 0
        yOffset = 0.0
        ay = 0.0
        aCal = 0
        a = time.time()
        while True:
            try:
                data, address = serverSock.recvfrom(1024)
                serverSock.sendto(data, (host, port2))
                serverSock.sendto(data, (host, port3))
                data = data.decode()
                rawData = data.split(',')
                if rawData[0] == 'I':
                    ay = float(rawData[2]) - float(yOffset)
                    ay = round(ay, 3)
                    yCount += 1
                    if (yCount < 230):
                        if (ay > 0.05 or ay < -0.05):
                            aCal += 1
                    else:
                        if (aCal > 150):
                            yOffset = yOffset + ay
                        yCount = 0
                        aCal = 0
                    if isSeatBelt == 1:
                        sbData = rawData[9]  # seatbelt
                    if isIgnition == 1:
                        igData = rawData[8]  # ignition

                if (rawData[0] == 'G'):
                    b = time.time() - a
                    a = time.time()
                    if (b > 3):
                        eFlag = False
                    else:
                        eFlag = True
                    lat = rawData[1]
                    long = rawData[2]
                    speed = rawData[3]
                    if (float(speed) < 3):
                        speed = 0.0
                    nodeData[0] = lat
                    nodeData[1] = long
                    nodeData[2] = nodeData[3]  # last Speed
                    nodeData[3] = speed  # current Speed

                elif (rawData[0] == 'I'):
                    nodeData[4] = rawData[1]  # Ax
                    nodeData[5] = ay  # AY

                if (eFlag == False):
                    eventState = '0'
                else:
                    eventState = CheckEvent()
            except KeyboardInterrupt:
                break
    except Exception as error:
        ct = str(datetime.datetime.now())
        f = open(home_path+'DVR/ELogs/rec_UDP.txt', 'w')
        f.write(ct + '  ' + str(error))
        f.close()


def camSwitchFunc():
    sUrl = 'http://"+my_https+"/camswitch?hub_id=' + hubid
    while True:
        try:
            x = requests.get(sUrl)
            if x.status_code == 200:
                if x.text[0] == '0':
                    print('MotionEye Should Off')
                    check = subprocess.run(["systemctl", "is-active", "motioneye"], stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                    status = check.stdout.decode()
                    status = status.strip()
                    if status == 'active':
                        check = subprocess.run(["systemctl", "stop", "motioneye"], stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE)
                    else:
                        pass
                elif x.text[0] == '1':
                    check = check = subprocess.run(["systemctl", "is-active", "motioneye"], stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE)
                    status = check.stdout.decode()
                    status = status.strip()
                    if status == 'inactive':
                        check = check = subprocess.run(["systemctl", "start", "motioneye"], stdout=subprocess.PIPE,
                                                       stderr=subprocess.PIPE)
                    else:
                        pass
            time.sleep(3)
        except KeyboardInterrupt:
            break
        except Exception as error:
            ct = str(datetime.datetime.now())
            f = open(home_path+'DVR/ELogs/camSwitchFuncI.txt', 'w')
            f.write(ct + ' ' + str(error))
            f.close()
            time.sleep(3)


def gpsLoggerFunc():
    global lat, long, speed
    count = 0
    logDataNew = ''
    while True:
        try:
            if count < 60:
                time.sleep(5)
                count += 1
                fileNew = open(home_path+'DVR/gpslogsNew.txt', 'w')
                ts = time.time()
                x = datetime.datetime.fromtimestamp(ts)
                tim1 = x.strftime("%Y-%m-%d")
                tim2 = (x.strftime("%H:%M:%S"))
                logDataNew = '{%20%22HubId%22:' + hubid + ',%20%22Latitude%22:%22' + lat +\
                '%22,%20%22Longitude%22:%22' + long + '%22,%20%22Altitude%22:%2225%22,%20%22Speed%22:' +\
                str(speed) + ',%20%22ServerDateTime%22:%22' + tim1 + '%20' + tim2 + '%22%20},%20'
                fileNew.write(logDataNew)

            else:
                fileNew.close()
                fileNew = open(home_path+'DVR/gpslogsNew.txt')
                dataNew = fileNew.read()
                dataNew = dataNew[:-4]
                url = 'http://"+my_https+"/api/gpslogger?data=[' + dataNew + '%20]'
                try:
                    x = requests.get(url)
                    if (x.status_code == 200):
                        file = open(home_path+'DVR/gpslogs.txt', 'w')
                        count = 0
                    else:
                        file = open(home_path+'DVR/gpslogs.txt', 'a')
                        count = 0
                except Exception as error:
                    file = open(home_path+'DVR/gpslogs.txt', 'a')
                    print(error)
                    ct = str(datetime.datetime.now())
                    f = open(home_path+'DVR/ELogs/camSwitchFuncI.txt', 'w')
                    f.write(ct + ' ' + str(error))
                    f.close()
                    time.sleep(3)
                    count = 0
        except KeyboardInterrupt:
            break


def SendOverlay(ipaddress):
    global lat, long, speed, eventName
    try:
        url = 'http://' + ipaddress + '/cgi-bin/configManager.cgi?action=setConfig&VideoWidget[0].CustomTitle[1].Text=' + str(
            speed) + '%20km%2Fh|' + lat + '%20%20' + long + '|' + eventName
        passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, auth_user, auth_passwd)
        authhandler = urllib.request.HTTPDigestAuthHandler(passman)
        opener = urllib.request.build_opener(authhandler)
        urllib.request.install_opener(opener)
        res = urllib.request.urlopen(url)
    except Exception as error:
        ct = str(datetime.datetime.now())
        f = open(home_path+'DVR/ELogs/Send_Overlay.txt', 'w')
        f.write(ct + ' ip = ' + ipaddress + '  ' + str(error))
        f.close()

def RunOverlay(ipaddress):
    threadingTask = threading.Thread(target=SendOverlay, args=[ipaddress])
    threadingTask.start()

def AllOverlay(cam):
    if cam >= 1:
        RunOverlay('192.168.15.90')
    if cam >= 2:
        RunOverlay('192.168.15.95')
    if cam >= 3:
        RunOverlay('192.168.15.100')
    if cam >= 4:
        RunOverlay('192.168.15.105')

listen_UDP = threading.Thread(target=rec_UDP)
listen_UDP.start()

if motionBox == 1:
    motionOverlayThread = threading.Thread(target=MotionOverlay)
    motionOverlayThread.start()
    motionEventThread = threading.Thread(target=MotionEvent)
    motionEventThread.start()

if camSwitch == 1:
    camSwitchThread = threading.Thread(target=camSwitchFunc)
    camSwitchThread.start()

if gpsLog == 1:
    gpsLoggingThread = threading.Thread(target=gpsLoggerFunc)
    gpsLoggingThread.start()



while True:
    try:
        time.sleep(1)
        GPSTask()
        AllOverlay(totalCam)
    except KeyboardInterrupt:
        break
