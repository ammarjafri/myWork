#!/usr/bin/python

import requests
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth
import datetime


def TimeOverlay(ipaddress):
    url= 'http://'+ipaddress+'/cgi-bin/global.cgi?action=setCurrentTime&time='
    url_enable = 'http://'+ipaddress+'/cgi-bin/configManager.cgi?action=setConfig&VideoWidget[0].CustomTitle[1].EncodeBlend=true'
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    url = url + date + '%20'    
    time = datetime.datetime.now().strftime('%H:%M:%S')
    url = url + time
    try:
        #print(url)
        response = requests.get(url, auth=HTTPDigestAuth('admin', 'camosg123'),timeout = 2)
        print(response.status_code)
        response = requests.get(url_enable, auth=HTTPDigestAuth('admin', 'camosg123'),timeout = 2)
        print(response.status_code)
    except:
        print('Please check Camera Connection', ipaddress)
        
    
def TotalCams(cams):
    if(cams==0):        
        print('Please setup config.txt file')
    if(cams==1):
        TimeOverlay('192.168.15.90')
    elif(cams==2):
        TimeOverlay('192.168.15.90')
        TimeOverlay('192.168.15.95')
        
    elif(cams==3):
        TimeOverlay('192.168.15.90')
        TimeOverlay('192.168.15.95')
        TimeOverlay('192.168.15.100')
    elif(cams==4):
        TimeOverlay('192.168.15.90')
        TimeOverlay('192.168.15.95')
        TimeOverlay('192.168.15.100')
        TimeOverlay('192.168.15.105')

f = open('/home/pi/DVR/config.txt')
data = f.read()
data = data.split('\n')
totalCams = 0
f.close()
for x in data:
    index = x.find('cams=')
    if(index != -1):
        #print(x[len('cams='):len(x)])
        value=x[len('cams='):len(x)]
        try:            
            value=int(value)
            totalCam=value
            #print(value)
        except:
            print('error in config.txt file')
        


TotalCams(totalCam)

    

