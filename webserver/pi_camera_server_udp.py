import cv2
import Image
from StringIO import StringIO
from flask import Flask,send_file, request, make_response, jsonify
from socket import *
import threading
import numpy as np
import time
import base64
from picamera.array import PiRGBArray
from picamera import PiCamera

from gpiozero import Motor

#Need a config file for this part
motors = {
    'left':Motor(forward=17, backward=27),
    'right':Motor(forward=22, backward=23)
}


app = Flask(__name__)

captureThread = None
image = None

s = socket(AF_INET,SOCK_DGRAM)
host ="192.168.0.10"
port = 9999
buf =65536
addr = (host,port)

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
capture = PiRGBArray(camera, size=(640, 480))

def loopingCamera():
	global capture
	global camera
	for frame in camera.capture_continuous(capture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
		img = frame.array
		capture.truncate(0)
		serve_image(img)


def serve_image(image):
	
    img_io = StringIO()
    imgRGB=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    njpg = Image.fromarray(imgRGB)
    njpg.save(img_io, 'JPEG', quality=50)
    img_io.seek(0)
#    s.sendto(str(img_io.len),addr)
    data = img_io.read(buf)
    while (data):
        if(s.sendto(data,addr)):
            #print "sending ..."
            data = img_io.read(buf)

#    s.sendto('DONE',addr)
    img_io.close()


@app.route('/pressed')
def pressed():
    direct = request.args.get('dir')
    side = request.args.get('side')
    print(direct)
    print(side)

    if direct == 'up':
        motors[side].forward()
    elif direct == 'down':
        motors[side].backward()

    return 'pressed'


@app.route('/released')
def released():
    direct = request.args.get('dir')
    side = request.args.get('side')
    print(direct)
    print(side)

    motors[side].stop()
    return 'released'

if __name__ == '__main__':
    global capture
    global captureThread
    try:
        captureThread = threading.Thread(target=loopingCamera, args=())
        captureThread.start()
        app.run(host='0.0.0.0')
    except KeyboardInterrupt:

        captureThread.stop()
