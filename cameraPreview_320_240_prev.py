#from multiprocessing import Process
from picamera import PiCamera
from fractions import Fraction
from time import sleep
	
#btn3 Handler
def btn4_CtoF_clicked():
	with PiCamera() as camera:
		camera.preview_fullscreen=False
		camera.resolution = (3280,2460)
		#mini monitor
		camera.preview_window=(47, 457, 320, 240)
		#(higher resolution monitor)
		#camera.preview_window=(47, 552, 640, 480)
		camera.start_preview()
		camera.vflip=False
		camera.hflip=False
		camera.color_effects=(128,128)
		camera.exposure_mode = 'night'
		camera.shutter_speed = int(1000000*Fraction(1,100))
		camera.iso = 200
		sleep(240)
		camera.stop_preview()	
		camera.close()



if __name__ == '__main__':
	btn4_CtoF_clicked()

