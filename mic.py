#!/usr/bin/env python3
import numpy as np
import sounddevice as sd
import datetime

duration = 24 * 60 * 60 #in seconds

def now():
   return datetime.datetime.now()

start = now()

def audio_callback(indata, frames, time, status):
   volume_norm = np.linalg.norm(indata) * 10
   global start
   end = now()
   delta = end - start
   if(0 < delta.seconds) :
      start = end
      # print(delta.seconds)
      print("|" * int(volume_norm), int(volume_norm))

stream = sd.InputStream(callback=audio_callback)
with stream:
   sd.sleep(duration * 1000)