import cv2
import Image
from StringIO import StringIO
from flask import Flask,send_file, make_response
import time
import threading
app = Flask(__name__)

capture = None
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
    global image
    while True:
        rc,img = capture.read()
        image = img
        time.sleep(0.05)


app.add_url_rule('/image.jpg','image',serve_image)
if __name__ == '__main__':
    global capture
    global captureThread
    try:
        capture = cv2.VideoCapture(0)
        captureThread = threading.Thread(target=loopingCamera, args=())
        captureThread.start()
        app.run()
    except KeyboardInterrupt:
		captureThread.stop()
