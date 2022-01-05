#!/usr/bin/python3

import os, socket, subprocess, time

def isactive():
    msg = "connected"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect(("182.188.40.167",8080))
    except:
        msg = "nointernet"
    finally:
        s.close()
        if msg != "connected":
            return msg
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect(("10.8.0.1",555))
        except:
            try:
                msg = "restartvpn"
                subprocess.call(["systemctl", "restart", "openvpn"])
            except:
                msg = "failed"
        finally:
            s.close()
    return msg

if __name__ == "__main__":
   while True :
        time.sleep(60)
        #isactive()
        print('Result:', isactive())