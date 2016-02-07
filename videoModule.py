from SimpleCV import Camera, VideoStream, Display
from multiprocessing import Process
import subprocess
import time
import datetime
import sys
from sys import argv
import os
import getopt

def saveFilmToDisk(bufferName, outname):
    params = " -i {0} -c:v mpeg4 -b:v 700k -r 24 {1}".format(bufferName, outname)
    subprocess.call('ffmpeg'+params, shell=True)
    os.remove('buffer.avi')

class VideoModule:
    videoTitle =  time.strftime("%Y_%m_%d_%H_%M_%S_")

    continueRecord = True

    width = 300
    height = 300

    makefilmProcess = Process()

    disp = 0

    def getVideoTitle(self):
        return self.videoTitle

    def getVideoDisplay(self):
        return self.disp

    def recordVideo(self, length=5):
        BUFFER_NAME = 'buffer.avi'
        vs = VideoStream(fps=24, filename=BUFFER_NAME, framefill=True)
        self.disp = Display((self.width, self.height))
        cam = Camera(prop_set={"width":self.width,"height":self.height})

        while self.continueRecord:
            gen = (i for i in range(0, 30 * length) if self.continueRecord)
            for i in gen:
                img = cam.getImage()
                vs.writeFrame(img)
                img.save(self.disp)
            self.continueRecord = False
        print "Broke capture loop"
        self.disp.quit()

        print "Saving video"

        # This is to run this process asynchronously - we will skip that
        # self.makefilmProcess = Process(target=saveFilmToDisk, args=(BUFFER_NAME, self.videoTitle))
        # self.makefilmProcess.start()

    def endCapture(self):
        self.continueRecord = False
        print "Set variable to false"

    def __init__(self, appendTitle):
        self.videoTitle += appendTitle + ".mp4"
