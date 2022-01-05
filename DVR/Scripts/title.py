#!/usr/bin/python

import requests
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth


def NameOverlay(ipaddress):
    url = 'http://'+ipaddress+'/cgi-bin/configManager.cgi?action=setConfig&VideoWidget[0].ChannelTitle[1].EncodeBlend=true&ChannelTitle[0].Name='+namePlate
    try:
        response = requests.get(url, auth=HTTPDigestAuth('admin', 'camosg123'),timeout=2)
        print(ipaddress,response)
    except:
        print('Please check Camera Connection', ipaddress)
        

def TotalCams(cams):
    if(cams==1):
        NameOverlay('192.168.15.90')
    elif(cams==2):
        NameOverlay('192.168.15.90')
        NameOverlay('192.168.15.95')
        
    elif(cams==3):
        NameOverlay('192.168.15.90')
        NameOverlay('192.168.15.95')
        NameOverlay('192.168.15.100')
    elif(cams==4):
        NameOverlay('192.168.15.90')
        NameOverlay('192.168.15.95')
        NameOverlay('192.168.15.100')
        NameOverlay('192.168.15.105')


namePlate = input("please enter the truck number:    ")

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
    
