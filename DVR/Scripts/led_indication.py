from gpiozero import LED
import socket
main = LED(6)
cabin = LED(13)
front = LED(19)
right = LED(26)
main.on()
def isactive(ipaddress, port):
    connected = False
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((ipaddress,port))
        connected = True
    except:
        connected = False
    finally:
        s.close()
    return connected

if __name__ == "__main__":
    
    ipcabin = '192.168.15.90'
    ipfront = '192.168.15.95'
    ipright = '192.168.15.100'
    ipleft  = '192.168.15.105'
    while(True): 
        if isactive(ipcabin, 554):
            cabin.on()
        else:
            cabin.off()
        if isactive(ipfront, 554):
            front.on()
        else:
            front.off()
        if isactive(ipright, 554):
            right.on()
        else:
            right.off()
