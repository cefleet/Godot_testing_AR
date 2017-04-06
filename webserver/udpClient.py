from socket import *
import sys
import select
import struct

host="localhost"
port = 9999
s = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))

addr = (host,port)
buf=65536

buft = ''
while len(buft)<4:
    buft += s.recv(4-len(buft))

size = struct.unpack('!i', buft)
print "receiving %s bytes" % size


with open('img.jpg', 'wb') as img:
    while True:
        data,addr = s.recvfrom(buf)
        print('gettingData')
        if not data:
            break
        img.write(data)
        if data == 'DONE':
            print('This one is done')
            break

img.close()
s.close()
