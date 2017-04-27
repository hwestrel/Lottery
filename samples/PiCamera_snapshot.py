
import datetime
from gpiozero import Button
from picamera import PiCamera
from time import sleep

button = Button(2)
camera = PiCamera()

#-----------------
# camera.iso = 100
# camera.shutter_speed = microsec
camera.video_stabilization = True
camera.resolution = 'XGA'
# VGA, XGA,HD
#-----------------
print ("ISO:" + str(camera.iso))
print ("Shutter Speed:" + str(camera.shutter_speed))
print ("Video Stab:" + str(camera.video_stabilization))
print ("Resolution:" + str(camera.resolution))

button.wait_for_press()
sleep(1)

#camera.start_preview()

while True:
    #camera.start_preview() 
    button.wait_for_press()
    button.wait_for_release()
    timestamp = str( datetime.datetime.today())
    camera.annotate_text = timestamp
    sleep(1)
    camera.capture('/home/pi/Lottery/face.jpg')
    print ("Picture taken - " + timestamp)
    sleep(2)
    # camera.stop_preview()
 

