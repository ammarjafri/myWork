from gpiozero import Button #import button from the Pi GPIO library
import time # import time functions
import os #imports OS library for Shutdown control

stopButton = Button(21) # defines the button as an object and chooses GPIO 26

while True:
    if stopButton.is_pressed:
        time.sleep(1)
        if stopButton.is_pressed:
            print('Shutdown')
            os.system("shutdown now -h")
            
    time.sleep(1) # wait to loop again so we don’t use the processor too much.