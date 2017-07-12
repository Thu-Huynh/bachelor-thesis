from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import Tkinter as tki
import threading
import datetime
import imutils
import cv2
import os
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27,1)
class PhotoBoothApp:
        def ON(self):
                GPIO.output(27,0)
                os.system("aplay /home/pi/bash/moi.wav")
        def OFF(self):
                GPIO.output(27,1)
        def NOTICE(self):
                os.system("aplay /home/pi/bash/khong.wav")
	def __init__(self, vs, outputPath):
		self.vs = vs
		self.outputPath = outputPath
		self.frame = None
		self.thread = None
		self.stopEvent = None
		self.root = tki.Tk()
		self.panel = None
		
		btn = tki.Button(self.root, width=25, text="SNAPSHOT", command=self.takeSnapshot)
		on = tki.Button(self.root, width=25, text ="UNLOCK", command = self.ON)
                off = tki.Button(self.root, width=25, text="LOCK", command=self.OFF)
                notice= tki.Button(self.root, width=25, text="NOTICE", command=self.NOTICE)
		btn.pack(side="bottom",expand="yes", padx=10, pady=10)
                notice.pack(side="bottom",expand="yes",padx=10,pady=10)
                off.pack(side="bottom",expand="yes", padx=10, pady=10)
                on.pack(side="bottom",expand="yes", padx=10, pady=10)
               	self.stopEvent = threading.Event()
		self.thread = threading.Thread(target=self.videoLoop, args=())
		self.thread.start()

		self.root.wm_title("Giao dien quan sat va dieu khien")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

	def videoLoop(self):
		try:
			while not self.stopEvent.is_set():
				self.frame = self.vs.read()
				self.frame = imutils.resize(self.frame, width=200)
		
				image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
				image = Image.fromarray(image)
				image = ImageTk.PhotoImage(image)
		
				if self.panel is None:
					self.panel = tki.Label(image=image)
					self.panel.image = image
					self.panel.pack(fill="both",expand="yes")		
				else:
					self.panel.configure(image=image)
					self.panel.image = image

		except RuntimeError, e:
			print("[INFO] caught a RuntimeError")

	def takeSnapshot(self):
		ts = datetime.datetime.now()
		filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
		p = os.path.sep.join((self.outputPath, filename))
		cv2.imwrite(p, self.frame.copy())
		print("[INFO] saved {}".format(filename))

	def onClose(self):
		print("[INFO] closing...")
		self.stopEvent.set()
		self.vs.stop()
		self.root.quit()
