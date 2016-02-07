import time
from userSettings import LENGTH
from videoModule import VideoModule as video
from audioModule import AudioModule as audio
from videoModule import saveFilmToDisk
from threading import Thread
from msvcrt import getch	# MICROSOFT WINDOWS MODULE
import os

def keypressKill(obj):
	getch()		# Essentially just wait for keypress
	print "Ending capture"
	for o in obj:
		o.endCapture()

def clickKill(vidObj, obj):
	while(vidObj.getVideoDisplay() == 0):
		pass;

	while(vidObj.getVideoDisplay().isNotDone()):
		if vidObj.getVideoDisplay().mouseLeft:
			print "Ending capture"
			for o in obj:
				o.endCapture()

videoTitle = "TheAmazingVisrut"		# No spaces allowed in the name

vCapture = video(videoTitle)
aCapture = audio(videoTitle)

threads = []

threads.append(Thread(target=aCapture.recordAudio, args=(LENGTH,)))
threads.append(Thread(target=vCapture.recordVideo, args=(LENGTH,)))
#threads.append(Thread(target=clickKill, args=(vCapture, [vCapture, aCapture],)))
threads.append(Thread(target=keypressKill, args=([vCapture, aCapture],)))

for t in threads:
	t.start()

threads[0].join()

print "Post thread statement"

print "Output file: " + vCapture.getVideoTitle()

saveFilmToDisk('buffer.avi', vCapture.getVideoTitle())
aCapture.saveToDisk();

os.system("ffmpeg -i " + vCapture.getVideoTitle() + " -i " + aCapture.getAudioTitle() + " -c:v copy -c:a copy awesomeMix.avi")