###This doesn't work yet but it does use
##sudo pip install git+https://github.com/dpallot/simple-websocket-server.git
import cv2
import numpy as np
import threading
import json
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket


server = None
clients = []


class SimpleWSServer(WebSocket):
    def handleConnected(self):
        clients.append(self)

    def handleClose(self):
        clients.remove(self)


def run_server():
    global server
    server = SimpleWebSocketServer('', 8081, SimpleWSServer,
                                   selectInterval=(1000.0 / 15) / 1000)
    server.serveforever()


t = threading.Thread(target=run_server)
t.start()

www
capture = cv2.VideoCapture(0)

t = 100
w = 640.0

last = 0
while True:
    ret, image = capture.read()

    for client in clients:
    msg = json.dumps({'x': x / w, 'y': y / h, 'radius': radius / w})
    client.sendMessage(unicode(msg))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


server.close()
