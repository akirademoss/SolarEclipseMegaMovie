#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Eclipse megamovie

This code is in interactive GUI used for
eclipse photography automization

author: Akira DeMoss, Siuling Pau, and Juan Carlos Martinez Oliveros
last edited: August 2017
"""

#imports
import os
import pynmea2	
import sys
from time import sleep
import datetime as dt
from subprocess import Popen
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
from datetime import timedelta
import subprocess
import signal
import Queue as queue


class MyWindow(QWidget): 
	def __init__(self,*args): 
		QWidget.__init__(self,*args)
		QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 9))
		self.te = QtGui.QTextEdit()
		self.te2 = QtGui.QTextEdit()
		self.te.setReadOnly(True)
		self.te2.setReadOnly(True)
		#inserts GUI megamovie logo
		pixmap = QtGui.QPixmap('mega_logo.png')
		pixmap2 = pixmap.scaledToWidth(135)
		label = QtGui.QLabel(self)
		label.setPixmap(pixmap2)
		label.move(1,1)
		#Take GPS button
		self.btn = QtGui.QPushButton('Take GPS', self)
		self.btn.setToolTip('Acquires GPS position')
		self.btn.clicked.connect(self.btn_clicked)
		self.btn.resize(110, 30)
		self.btn.move(140, 0)
		#Start Timeserver button
		self.btn1 = QtGui.QPushButton('Contact Times', self)
		self.btn1.setToolTip('First click \'Take GPS\' to enable button')
		self.btn1.setEnabled(False)
		self.btn1.clicked.connect(self.btn1_clicked)
		self.btn1.resize(110, 30)
		self.btn1.move(140, 30)      
		#Start Timeserver button
		self.btn2 = QtGui.QPushButton('Time Precision', self)
		self.btn2.setToolTip('First click \'Get Contact Times\' to enable button')
		self.btn2.setEnabled(False)
		self.btn2.setCheckable(True)
		self.btn2.clicked.connect(lambda:self.btn2_clicked)
		self.btn2.clicked.connect(self.btn2_clicked)
		self.btn2.resize(110,30)
		self.btn2.move(140, 60) 
		#Take Eclipse button
		self.btn3 = QtGui.QPushButton('Take Eclipse', self)
		self.btn3.setToolTip('First click \'Compute Contact Times\' to enable button.\nMake sure sun is in focus.\'Camera Preview\' and \'Time Precision\' must be toggled off to capture eclipse')
		self.btn3.setEnabled(False)
		self.btn3.clicked.connect(self.btn3_clicked)
		self.btn3.resize(110, 30)
		self.btn3.move(140, 90) 
		#Camera Preview button
		self.btn4 = QtGui.QPushButton('Camera\nPreview', self)
		self.btn4.setToolTip('Displays preview window for camera')
		self.btn4.setCheckable(True)
		self.btn4.clicked.connect(lambda:self.btn4_clicked)
		self.btn4.clicked.connect(self.btn4_clicked)
		self.btn4.resize(60,60)
		self.btn4.move(255, 45) 
		#Quit button
		self.qbtn = QtGui.QPushButton('Quit', self)
		self.qbtn.setToolTip('Kill program')
		self.qbtn.clicked.connect(self.qbtn_clicked)
		self.qbtn.resize(110,30)
		self.qbtn.move(140, 120)  		      
		#GUI settings
		self.setGeometry(0, 0, 320, 370)
		self.setWindowTitle('Eclipse Megamovie')   
		self.show()
		#Layout
		layout = QGridLayout(self)
		layout.addWidget(label)
		layout.addWidget(self.te)
		layout.addWidget(self.te2)
		self.setLayout(layout) 
			
	#btn Handler (Take GPS)
	def btn_clicked(self):
		self.btn4_switch()
		self.btn1.setToolTip('Waiting for GPS calibration...')
		self.te.append('Taking 1 minute GPS Calibration data... Please wait while calibrating\n')
		self.write_gps()
		self.format_position()
		self.btn1.setEnabled(True)
		self.btn1.setToolTip('Displays eclipse contact times based off of calibrated GPS coordinates')
		self.btn4_switch()
		
	#btn1 Handler (Get Contact Times)
	def btn1_clicked(self):	
		self.te.append('\nFinding contact times... ')
		self.compute_contacts()
		self.btn2.setEnabled(True)
		self.btn2.setToolTip('Displays the GPS jitter, updates value every minute')
		
	#btn2 Handler (Start Time Server)	
	def btn2_clicked(self):
		import os
		self.btn2.toggle()
		global thread
		if self.btn2.isChecked(): 
			thread.terminate()
			self.btn2.toggle()
			self.btn3_switch()
		else:
			self.btn2.toggle()
			self.btn3_switch()
			self.te2.append('Finding Time Precision Data... Wait 1 minute\n')
			self.queue = queue.Queue()
			thread = GpsJitterThread(self.queue, self.append_jitter)
			thread.start()
			for arg in range(240):
				self.queue.put(arg)
			
	#btn3 Handler (Take Eclipse)
	def btn3_clicked(self):
		self.btn4.setEnabled(False)
		self.btn4.setToolTip('Waiting for eclipse photography...')
		self.photo_automatize()
		self.btn4.setEnabled(True)
		self.btn1.setToolTip('Displays eclipse contact times based off of calibrated GPS coordinates')
		self.btn4.setToolTip('Displays preview window for camera')
		
	#btn4 Handler (Camera Preview)
	def btn4_clicked(self): 
		self.btn4.toggle()
		global pidb4_
		if self.btn4.isChecked() and pidb4_ > 0:
			self.btn4.toggle()
			os.kill(pidb4_, signal.SIGKILL)
			self.btn3_switch()
		else:
			self.btn4.toggle()
			self.btn3_switch()
			cam_prev = subprocess.Popen([sys.executable,'/home/pi/eclipse/GUI/cameraPreview_320_240_prev.py'])
			pidb4_ = int(cam_prev.pid)
			
	#btn4 Handler (Quit)	
	def qbtn_clicked(self):
		pid = QtCore.QCoreApplication.applicationPid()
		os.kill(pid, signal.SIGKILL)
		
	#Enable/Disable switch for btn3
	def btn3_switch(self):
		if self.btn3.isEnabled() == True and self.btn4.isChecked():
			self.btn3.setEnabled(False)
			self.btn3.setToolTip('First click \'Compute Contact Times\' to enable button.\nMake sure sun is in focus.\'Camera Preview\' and \'Time Precision\' must be toggled off to capture eclipse')
		else:
			self.btn3.setEnabled(True)
			self.btn3.setToolTip('Take eclipse photography burst and bracket mode.\nMake sure sun is in focus.')
			
	#Enable/Disable switch for btn4	
	def btn4_switch(self):
			if self.btn4.isEnabled() == True:
				self.btn4.setEnabled(False)
				self.btn4.setToolTip('Waiting for GPS calibration...')
			else:
				self.btn4.setEnabled(True)
				self.btn4.setToolTip('Displays preview window for camera')
				
	#creates file with GPS position and timestamp collected for 1 minute calibration
	def write_gps(self):
		import pynmea2
		import datetime as dt
		import time
		import serial	
		import subprocess
		#kills gpsd and ntpd proccesses running in background (if any) to enable new data acquisition
		subprocess.call("sudo killall gpsd", shell=True)
		subprocess.call("sudo killall ntpd", shell=True)
		serialPort = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)
		today = dt.datetime.utcnow()
		timeout = time.time() + 1*60 #minutes
		self.position_data = '/home/pi/eclipse/gps_data_%d%02d%02d_%02d%02d.dat'%(today.year,today.month,today.day,today.hour,today.minute)
		f = open('/home/pi/eclipse/gps_data_%d%02d%02d_%02d%02d.dat'%(today.year,today.month,today.day,today.hour,today.minute),'w')
		while True:
			QtCore.QCoreApplication.processEvents()
			strng = serialPort.readline()
			self.parseGPS(strng,f)
			if time.time() > timeout:
				break
		f.close()
		
		
	#formats strings for GPS calibration
	def parseGPS(self, strng,f):
		if strng.find('GGA') > 0:
			msg = pynmea2.parse(strng)
			latitude = msg.latitude + msg.latitude_minutes *1.0/60 + msg.latitude_seconds * 1.0/3600
			longitude = msg.longitude + msg.longitude_minutes * 1.0/60 + msg.longitude_seconds * 1.0/3600
			f.write("%s,%07.4f,%07.4f,%s,\n" % (msg.timestamp,latitude,longitude,msg.altitude))
	
	#computes average of last 20 recorded GPS positions and formats output
	def format_position(self):
		from lat_lon import LatLon
		f = open(self.position_data)
		#create arrays of times, latitudes and longitudes
		times=[];lats=[];lons=[];alts=[]
		for line in f:
			col = line.split(',')
			time = col[0]
			times.append(time)
			lat = col[1]
			lats.append(float(lat))
			lon = col[2]
			lons.append(float(lon))
			alt = col[3]
			alts.append(float(alt))
		#create new arrays for last 20 elements	
		new_lats=[]; new_lons=[]; new_alts=[]
		end = len(lats)-1
		#store elements to be averaged in new arrays
		i = 0
		while i < 20:
			QtCore.QCoreApplication.processEvents()
			new_lats.append(lats[end-i])
			new_lons.append(lons[end-i])
			new_alts.append(alts[end-i])
			i+=1
		f.close()
		#formatting for GUI
		self.latitude = round(sum(new_lats)/20,4)
		self.longitude = round(sum(new_lons)/20,4)
		altitude = str(round(sum(new_alts)/20,4))
		time = str(times[end])
		lat_lon = LatLon(self.latitude, self.longitude)
		lat_lon = lat_lon.to_string('d% %m% %S% %H')
		lat_lon = str(lat_lon)
		lat_lon = lat_lon.strip('(\'\')')
		col = lat_lon.split(',')
		lat = col[0].strip('\'')
		lon = col[1].strip(' \'')
		strout = "GPS location stored\n\nTimestamp: %s\n Lat: %s \n Lon: %s \n Altitude: %s M"%(time,lat,lon,altitude)
		self.te.append(strout)
		
	#helper function for compute_contacts()
	def check_non_zero(self, x):
		return x > 0
		
	#computes contact times
	def compute_contacts(self):
		import ephem
		import math 					   
		from operator import itemgetter 
		observer = ephem.Observer() 
		observer.lat = str(self.latitude)
		observer.lon = str(self.longitude)
		time = (2017, 8, 21, 15, 40, 00)
		observer.date = time 
		sun = ephem.Sun()
		moon = ephem.Moon()
		results = []
		#5 hs = 18000
		for x in range (0,18000): 
			QtCore.QCoreApplication.processEvents()
			observer.date = (ephem.date(ephem.date(time) + x * ephem.second))
			sun.compute(observer)
			moon.compute(observer)
			r_sun = sun.size/2
			r_moon = moon.size/2
			s = math.degrees(ephem.separation((sun.az, sun.alt), (moon.az, moon.alt)))*60*60
			#Calculate the size of the lune
			if s <= (r_moon+r_sun):
				#only under totality. NO lune
				if r_moon >= (s+r_sun):    
					lunedelta = 'small' 
				else:
					lunedelta = 0.25 * math.sqrt((r_sun+r_moon+s)*(r_moon+s-r_sun)*(s+r_sun-r_moon)*(r_sun+r_moon-s))
			#If s>r_moon+r_sun there is no eclipse taking place
			else: 
				lunedelta = None
			if lunedelta:
				#Only under totality. NO lune
				if r_moon >= (s + r_sun):	
					lune_area = 0
					percent_eclipse = 100
				else:
					lune_area = 2*lunedelta + (r_sun*r_sun * math.acos((
						(r_moon*r_moon) - (r_sun*r_sun) - (s*s)) / (2*r_sun*s)
					)) - (r_moon*r_moon * math.acos((
						(r_moon*r_moon) + (s*s) - (r_sun*r_sun)) / (2*r_moon*s)))
					percent_eclipse = (1-(lune_area/(math.pi*r_sun*r_sun)))*100
			else:
						lune_area = None
						percent_eclipse = 0
			# Append to list of lists:
			results.append([observer.date.datetime(), s, sun.size,moon.size, lune_area, percent_eclipse])
		gen=(x for x in results)
		#Find Max percentage of eclipse...
		max_eclipse = max(gen, key=itemgetter(5)) 
		gen=(x for x in results)
		tc1 = next(x for x in gen if self.check_non_zero(x[5]))[0]
		self.tc2 =  next(x for x in gen if x[5] >= (max_eclipse[5] - 0.0001*max_eclipse[5]))[0]
		self.tc3 = next(x for x in gen if x[5] < (max_eclipse[5] - 0.0001*max_eclipse[5]))[0]
		tc4 = next(x for x in gen if x[5] == 0)[0]
		totality = self.tc3 - self.tc2
		mid_eclipse = self.tc2 + (totality)/2
		gen=(x for x in results)
		max_part_eclipse = next(x for x in gen if x[5] == (max_eclipse[5]))[0]
		if __name__ == '__main__':
			output = []
			gen=(x for x in results)
			if max_eclipse[5] == 100:
				output = str("\nMax percent: " + '%.2f' % max_eclipse[5]) + \
				str("\nMax eclipse at: " + str(mid_eclipse)) + str("\nDuration of totality: " + str(self.tc3-self.tc2)) + \
				str("\n\nFirst contact: " + str(next(x for x in gen if self.check_non_zero(x[5]))[0])) + \
				str("\nSecond contact: " + str(self.tc2)) + str("\nThird contact: " + str(self.tc3)) + \
				str("\nLast contact: " + str(next(x for x in gen if x[5] == 0)[0]) + "\n")
			else:
				output = "\nMax percent: " + '%.2f' % max_eclipse[5] + \
				str("\nMax eclipse at: " + str(max_part_eclipse)) + str("\nNo totality\n")
		self.te.append(output)

	#automate photography	
	def photo_automatize(self):		
		#camera imports
		from imutils.video import FPS
		import numpy as np
		from picamera import PiCamera
		from fractions import Fraction
		#Times for contacts
		start_first_burst = self.tc2 - dt.timedelta(seconds=20)
		end_first_burst = self.tc2 + dt.timedelta(seconds=2)
		start_second_burst = self.tc3 + dt.timedelta(seconds=2)
		end_second_burst = self.tc3 + dt.timedelta(seconds=20)
		#Camera setup
		shs = np.array([125,60,30,1,2]) 
		camera = PiCamera()
		camera.preview_fullscreen = False
		camera.resolution = (3280,2460)
		camera.preview_window=(47, 457, 320, 240)
		camera.start_preview()
		camera.iso = 50
		camera.color_effects=(128,128)
		#Before Camera Takes Shots
		while dt.datetime.now() < start_first_burst:
			QtCore.QCoreApplication.processEvents()
			self.te.append('sleeping... %s'%dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f'))
			sleep(1)
		#First Burst Mode Camera Settings
		#set i = 0 for control (see if statement)
		i = 0
		self.te.setTextColor(QtGui.QColor(255,0,0))
		self.te.append('\nUse filter\n')
		self.te.setTextColor(QtGui.QColor(0,0,0))
		fps = FPS().start()
		while start_first_burst <= dt.datetime.now() < end_first_burst :
			QtCore.QCoreApplication.processEvents()
			#Text for GUI
			#g.append('\nUse filter')
			camera.framerate = 24
			camera.shutter_speed = int(1000000*Fraction(1, int(1000)))
			# Give the camera time to set gains 
			sleep(0.01)
			camera.exposure_mode = 'off'
			#Burst mode capture
			camera.capture('/media/pi/U/images/Burst_Mode/img_%s_%d.jpg'%(dt.datetime.now().strftime('%Y%m%d_%H%M%S_%f'), 1000))
			fps.update()
			self.te.append('Exposure:\t   1/%ds\nDate:\t    %.22s'%(1000, dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')))
			#if statement, we add 1 to i so that '\nTake out filter in 5 seconds' only prints once.
			#this prints 5 seconds before the second contact time
			if dt.datetime.now() >= start_first_burst + dt.timedelta(seconds=15) and i <= 0:
				i += 1
				self.te.setTextColor(QtGui.QColor(255,0,0))
				self.te.append('\nTake out filter in 5 seconds\n')
				self.te.setTextColor(QtGui.QColor(0,0,0))
		#Bracket Mode Camera Settings	
		#set i = 0 for control (see if statement)
		i = 0
		while end_first_burst <= dt.datetime.now() < start_second_burst:
			QtCore.QCoreApplication.processEvents()
			if dt.datetime.now() >= start_second_burst - dt.timedelta(seconds=7) and i <= 0:
				i += 1
				self.te.setTextColor(QtGui.QColor(255,0,0))
				self.te.append('\nPut on filter in 5 seconds\n')
				self.te.setTextColor(QtGui.QColor(0,0,0))
			for spds in shs:
				QtCore.QCoreApplication.processEvents()
				camera.framerate = 30
				camera.shutter_speed = int(1000000*Fraction(1, int(spds)))
				#Set Gains
				sleep(0.01)
				camera.exposure_mode = 'off'
				#Capture Image
				camera.capture('/media/pi/U/images/Bracket_Mode/img_%s_%d.jpg'%(dt.datetime.now().strftime('%Y%m%d_%H%M%S_%f'), spds)) #,format='bgr',bayer='True')
				fps.update()
				self.te.append('Exposure:\t   1/%ds\nDate:\t    %.22s'%(spds, dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')))
		#Second Burst Mode Camera Settings	
		while start_second_burst <= dt.datetime.now() < end_second_burst:
			QtCore.QCoreApplication.processEvents()
			camera.framerate = 30
			camera.shutter_speed = int(1000000*Fraction(1, int(1000)))
			# Give the camera time to set gains 
			sleep(0.01)
			camera.exposure_mode = 'off'
			#Burst mode capture
			camera.capture('/media/pi/U/images/Burst_Mode/img_%s_%d.jpg'%(dt.datetime.now().strftime('%Y%m%d_%H%M%S_%f'), 1000))
			fps.update()
			self.te.append('Exposure:\t   1/%ds\nDate:\t    %.22s'%(1000, dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')))
		fps.stop()
		camera.stop_preview()	
		camera.close()
		self.te.append("\n[INFO] elasped time: {:.2f}".format(fps.elapsed()))
		self.te.append("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
		
	#Input to GUI from GPSJitterThread	
	def append_jitter(self, result):
		self.te2.append(result)
			
	
"""
Thread object class that emits signal to display jitter in GUI
"""			
class GpsJitterThread(QThread):
	finished=QtCore.pyqtSignal(object)
	#queue initializer, with two constructor input parameters 
	def __init__(self,queue,callback,parent=None):
		QThread.__init__(self,parent)
		self.queue=queue
		self.finished.connect(callback)
	
	#pulls numeric placeholders from queue list and passes them into jitter_out
	#executed when GpsJitterThread is created in main thread and function .start() is called
	def run(self):
		while True:
			arg=self.queue.get()
			if arg is None:
				return
			self.str_sigout(arg)
	
	#aquires jitter reading and em	
	def str_sigout(self, arg):
		period = timedelta(minutes=0.1)
		end_time = dt.datetime.now() + period
		while end_time >= dt.datetime.now():
			QtCore.QCoreApplication.processEvents()
			subprocess.call("sudo service timeservice restart", shell=True)
			subprocess.call("sudo ~/ntpd_startup", shell=True)
			p = subprocess.Popen(['ntpq', '-pn'], stdout=subprocess.PIPE)
			std_out = p.communicate()
			std_out = str(std_out)
			std_out.split(" ")
			str0 = 'jitter: '
			str1 = std_out[237]
			str2 = std_out[238]
			str3 = std_out[239]
			str4 = std_out[240]
			str5 = std_out[241]
			str6 = std_out[242]
			arg = str0 + str1 + str2 + str3 + str4 + str5 + str6    
			self.sleep(60)
		self.finished.emit(arg)

"""
"""	

def main():
	app = QtGui.QApplication(sys.argv)
	myapp = MyWindow()
	myapp.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()



