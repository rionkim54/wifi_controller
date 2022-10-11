#!/usr/bin/env python3
from pickletools import read_stringnl_noescape
import socket
import time

import numpy as np
import sounddevice as sd
import datetime
import errno

duration = 24 * 60 * 60 #in seconds


host = "192.168.0.37"
# host = "127.0.0.1"
port = 8899
MaxBytes = 1024*1024

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(30)

client.connect((host, port))

index = 0
client.send(bytes(bytearray([0x55,0xaa,0x5a,0xa5,0x7e,index,0x80,0x00,0x80,0x08,0x68,0x00,0x00,0x01,0x00,0x0a,0x01,0x00,0x01,0x00,0x7e])))

def now():
   return datetime.datetime.now()

start = now()

def sendData(value):
    if(255 < value) :
        value = 255
    global index
    index += 1
    if(0x0f < index) :
        index = 1

    # client.send(bytes(bytearray([0x55,0xaa,0x5a,0xa5,0x7e,index,0x80,0x11,0x00,0x39,0xaf,0x00,0x00,0x01,0x00,0x07,0x02,0x00,0x00,value,0x00,0x7e])))        
    try : 
        client.send(bytes(bytearray([0x55,0xaa,0x5a,0xa5,0x7e,index,0x80,0x11,0x00,0x39,0xaf,0x00,0x00,0x01,0x00,0x07,0x02,0x00,0x00,value,0x00,0x7e])))
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise
        pass

dimmingValue = 0

def audio_callback(indata, frames, time, status):
   volume_norm = np.linalg.norm(indata) * 10
   global start
   end = now()
   delta = end - start
   print("|" * int(volume_norm), int(volume_norm))
   dimmingValue = int(volume_norm)
   print(dimmingValue)
   if(0 < delta.seconds) :
        start = end
        # print(delta.seconds)
        sendData(dimmingValue)

        # recvData = client.recv(MaxBytes)
        # if not recvData:
        #     print('      ，     ')
        # else:
        #     localTime = time.asctime( time.localtime(time.time()))
        #     print(localTime, '         :',len(recvData))
        #     print(recvData)      

stream = sd.InputStream(callback=audio_callback)
with stream:
   sd.sleep(duration * 1000)

client.close()