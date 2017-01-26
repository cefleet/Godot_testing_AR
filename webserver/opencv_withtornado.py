##This doens't work ... yet but it does use:
## sudo pip install tornado
import cv2
import numpy as np
import threading
import json

import tornado.httpserver
import tornado.ioloop

def handle_request(request):
  message = "You requested %s\n" % request.uri
  request.write("HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s" % (len(message), message))
  request.finish()

http_server = tornado.httpserver.HTTPServer(handle_request)
http_server.listen(8081)
tornado.ioloop.IOLoop.instance().start()

print('this is tha t')
capture = cv2.VideoCapture(0)

t = 100
w = 640.0

last = 0
while True:
    ret, image = capture.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


server.close()
