import cv2
import Image
from StringIO import StringIO
from flask import Flask,send_file, request, make_response, jsonify
import threading
import numpy as np
import time
app = Flask(__name__)

capture = None
captureThread = None
image = None

def auto_canny(img, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(img)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    return edged

def detect(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = auto_canny(blurred)
    return edges

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

def serve_outline_data():
    global image
    imgRGB = detect(image)
    return jsonify(imgRGB.tolist())


def serve_outline_image():
    global image
    img_io = StringIO()
    imgRGB=detect(image)

    njpg = Image.fromarray(imgRGB)
    njpg.save(img_io, 'JPEG', quality=50)
    img_io.seek(0)
    response=make_response(send_file(img_io,mimetype='image/jpeg'))
    response.headers['Content-Length'] = img_io.len
    return response


def loopingCamera():
    global capture
    global image
    while True:
        rc,img = capture.read()
        image = img
        time.sleep(0.3)


@app.route('/pressed')
def pressed():
    direct = request.args.get('dir')
    side = request.args.get('side')
    print(direct)
    print(side)

    #if direct == 'up':
    #    motors[side].forward()
    #elif direct == 'down':
    #    motors[side].backward()

    return 'pressed'



@app.route('/released')
def released():
    direct = request.args.get('dir')
    side = request.args.get('side')
    print(direct)
    print(side)

    #motors[side].stop()
    return 'released'


app.add_url_rule('/image.jpg','image',serve_image)
app.add_url_rule('/outline.jpg','outline',serve_outline_image)
app.add_url_rule('/data.json','data',serve_outline_data)

if __name__ == '__main__':
    global capture
    global captureThread
    try:
        capture = cv2.VideoCapture(0)
        captureThread = threading.Thread(target=loopingCamera, args=())
        captureThread.start()
        app.run(host='0.0.0.0')
    except KeyboardInterrupt:
        captureThread.stop()
