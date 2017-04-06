import cv2
import Image
from StringIO import StringIO
from flask import Flask,send_file, request, make_response, jsonify
import threading
import numpy as np
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
app = Flask(__name__)

from gpiozero import Motor

#Need a config file for this part
motors = {
    'left':Motor(forward=17, backward=27),
    'right':Motor(forward=22, backward=23)
}


camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
capture = PiRGBArray(camera, size=(640, 480))


#capture = None
captureThread = None
image = None

def serve_image():
    global image
    img_io = StringIO()
    imgRGB=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    njpg = Image.fromarray(imgRGB)
    njpg.save(img_io, 'JPEG', quality=50)
    img_io.seek(0)
    response=make_response(send_file(img_io,mimetype='image/jpeg'))

    response.headers['Content-Length'] = img_io.len
    return response

def loopingCamera():
	global capture
	global camera
	global image
	for frame in camera.capture_continuous(capture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
		image = frame.array
		capture.truncate(0)

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


app.add_url_rule('/image.jpg','image',serve_image)

if __name__ == '__main__':
    global capture
    global captureThread
    try:
       # capture = cv2.VideoCapture(0)
        captureThread = threading.Thread(target=loopingCamera, args=())
        captureThread.start()
        app.run(host='0.0.0.0')
    except KeyboardInterrupt:
        captureThread.stop()
