# Solar Eclipse MegaMovie
This projected was funded by grant No. AGS-14612277 and conducted under PI 
Juan Carlos Martinez Oliveroz and co-PI Laura Peticolas
at UC Berkeley Space Sciences Lab

This software was developed for a raspberry pi 3, and picamera module v2.1 
to automatatize photography of the total solar eclipse of August 21, 2017.
The total solar eclipse 
of August 21, 2017 crossing 
The United States provided a unique scientific and educational 
opportunity to study the solar 
corona by solar physicists and 
citizen scientists.

Eclipse Megamovie project crowdsources scientifically valuable images 
of the solar corona from volunteers and amateur astronomers.

**Software objectives:**  
* Easy to use Graphical User Interface
* Real time GUI updates
* Calibrate GPS for coordinate precision
* Calculate eclipse contact times  
* Automatized “burst” images at fixed exposure 20 seconds before and after totality
* Iterate bracketed images: a “bracket” 
* Reminder message to remove filter 5 seconds before and after totality 
* Camera capture rate at least 1 FPS

# Required Hardware 

![setup1](https://user-images.githubusercontent.com/8731829/37075790-1dd0c070-2199-11e8-943d-86da87dd7944.png)

**Figure 1:** The basic required components for the raspberry pi powered solar eclipse camera set-up consists of an Uptronics GPS Expansion Board, Raspberry Pi 3, Picamera v2.1 module, 3D printed adapter for camera lense, hdmi + monitor + keyboard + mouse, tripod, and mounting platform.  In this instance, we used a set-up that mounted the raspberry pi and GPS hat between two pieces of wood.

# GUI Flowchart

![gui fixed](https://user-images.githubusercontent.com/8731829/37075358-191913b8-2197-11e8-9bd4-fb16ce68e972.png)

**Figure 2:** Event sequence necessary to successfully operate the solar eclipse camera.  Note that we purposely disable buttons in order to ensure that the user operates the camera in proper sequence.  The camera preview and quit buttons are both executable at any time, however Take GPS, Compute Contact Times, and Time Preciscion must be executed sequentially.  Additionally, the user will want to use the camera preview feature within 5 to 10 minutes of capturing the eclipse to ensure that the sun is in the frame of view of the camera. 

# Take GPS 

![gps_calibration1](https://user-images.githubusercontent.com/8731829/37075128-e4ed8b38-2195-11e8-96dc-8ac75d14aa69.JPG)

**Figure 3:** This is the screen displayed while the GPS module is performing a calibration.  During the calibration, the program is saving the output collected from the GPS module to a .dat file.  By default in Qt, events generated by the window system while the application is saving a file to disk will not be processed until the file is saved.  During this project substantive effort was put into resolving the issue of program crashes and inability to update the text view in real time.  The fix I will explain is simple.  In line 197 of megamovie_Akira_Simulate_Eclipse.py, the line reads QtCore.QCoreApplication.processEvents(). This function tells Qt to process any pending events, and then returns control to the caller.[1]

![gps_calibration2](https://user-images.githubusercontent.com/8731829/37075215-625be93e-2196-11e8-9b6a-83c22b7b86ad.JPG)
**Figure 4:**

![jitter format2](https://user-images.githubusercontent.com/8731829/37075221-6ab57f00-2196-11e8-8a54-be2d6ba191fd.JPG)
**Figure 5:**

![sleeping](https://user-images.githubusercontent.com/8731829/37075272-a948524c-2196-11e8-9ee1-b6b89bd03309.JPG)
**Figure 6:**

# Understanding the Qt framework





[1] http://www.informit.com/articles/article.aspx?p=1405544&seqNum=3

