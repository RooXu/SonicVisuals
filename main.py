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
s.setBufferSize(3640)
s.setVerbosity(True)
s.boot()
s.start()
s.amp = 0.2





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
#pat4 = Pattern(function=vidstuff,time = 0.25).play()
    
def pixChange(): 
    #Reading Two Frames 
    ret1,img1 = cap.read() 
    ret2,img2 = cap.read()

    #Blur the Frames
    imgGry1 = cv2.GaussianBlur(cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY), ksize=(5,5), sigmaX=0)
    imgGry2 = cv2.GaussianBlur(cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY), ksize=(5,5), sigmaX=0)

    #Calculate the difference
    imgDiff = cv2.absdiff(imgGry2,imgGry1)

    #Sum all the pixel intensities
    pxValSum = np.sum(imgDiff)
    print("PixValue Sum"+str(pxValSum))
    imgWidth = int(cap.get(3))
    imgHeight = int(cap.get(4))

    #Calculate the percent change with respect to the theoretical maximum change (if all pixels changed from 0 to 255)
    pixFrac = pxValSum/(imgWidth*imgHeight*255)
    print("Pixel Fraction"+ str(pixFrac))

    #Rescale the fraction to realistic pitches
    pxFreq = rescale(pixFrac,0,1,0,2000)

    #Generate a group of notes to play
    pxFreqs = [pxFreq/3,pxFreq/2,pxFreq,pxFreq*3,pxFreq*5,pxFreq*6,pxFreq*5,pxFreq*3,pxFreq,pxFreq/2]
    print("FreqList:" + str(pxFreqs))
    return EventSeq(pxFreqs)

def update(): 
    pixChangeEvent.play()

#The first argument that reaches the end of its sequence triggers the end of the Events’s playback
pixChangeEvent = Events(freq = EventCall(pixChange), beat = EventSeq([2/3.,1/3.])).play()

# Calls the update which calls on pixChangeEvent to obtain a new set of frequencies to play through.
pat = Pattern(function = update, time = 5).play()

#distort = Disto(pixChangeEvent, drive = 0.1, slope = 0.5, mul = 1, add = 0)
s.gui(locals())