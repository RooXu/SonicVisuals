#import numpy as np 
from pyo import *
import cv2
import numpy as np

print("Audio host APIS:")
#pa_list_host_apis()
#pa_list_devices()
#print("Default input device: %i" % pa_get_default_input())
#print("Default output device: %i" % pa_get_default_output())
#s=Server(audio="coreaudio")
s = Server(duplex = 0, nchnls = 2, audio="coreaudio")
s.setBufferSize(2056)
s.setVerbosity(True)
s.boot()
s.start()
s.amp = 0.2
# Creates a sine wave player.
# The out() method starts the processing
# and sends the signal to the output.
a = Sine(freq=200)
hr = Harmonizer(a).out()
hr1 = Harmonizer(hr).out()
hr2 = Harmonizer(hr1).out()
hr3 = Harmonizer(hr2).out()
# # Also through a chorus.
# ch = Chorus(a).out()

# # And through a frequency shifter.
# sh = FreqShift(a).out()




print("lmao3")
flipSwitch = False
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

def grabVid(): 
    #print("lmao")
    cap.grab()
    
def readVid():
    ret, frame = cap.retrieve()
    if ~ret: 
        a.freq = random.choice(midiToHz([60, 62, 63, 65, 67, 68, 71, 72]))
    else:
        average_color_row = np.average(frame, axis=0)
        average_color = np.average(average_color_row, axis=0)
        #print(average_color)
        a.freq = int(average_color[0])*10
def randoSine():
    a.freq = random.choice(midiToHz([60, 62, 63, 65, 67, 68, 71, 72]))

def vidstuff():
    ret, frame = cap.read()
    average_color_row = np.average(frame, axis=0)
    average_color = np.average(average_color_row, axis=0)
    #print(average_color)
    a.freq = int(average_color[0])*10
#Ca = CallAfter(function = grabVid, time = 5).out()
#pat2 = Pattern(function = readVid, time = 0.29).out()
#pat3 = Pattern(function= randoSine, time =0.3).play()
pat4 = Pattern(function=vidstuff,time = 0.25).play()
s.gui(locals())