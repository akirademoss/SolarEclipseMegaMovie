# Solar Eclipse MegaMovie
Research for this project was funded by grant No. AGS-14612277 and conducted under co-PIs 
Juan Carlos Martinez Oliveroz and Laura Peticolas
at UC Berkeley Space Sciences Lab.

This software was developed for raspberry pi 3, and picamera module v2.1 
to automatize photography for the total solar eclipse of August 21, 2017
which traversed accross the United States. This event provided a unique 
scientific and educational opportunity to study the solar corona by solar 
physicists, and citizen scientists alike.

To view the images and access the database [please click this link](https://eclipsemega.movie/)
Additionally, the academic poster can be viewed [here](https://drive.google.com/file/d/0B9rIxN9MNchmRWRrSXo2bHJRWjQ/view)

**Software objectives:**  
* Easy to use Graphical User Interface
* Real time GUI updates
* Calibrate GPS for coordinate precision
* Calculate eclipse contact times  
* Automatize “burst” images at fixed exposure 20 seconds before and after totality
* Iterate bracketed images to capture full dynamic range of solar corona during totality 
* Reminder message to remove filter 5 seconds before and after totality 
* Camera capture rate at least 1 FPS

## Documentation Overview
This documentation was created for the purpose of demonstrating the capabilities of the system.  Images displayed in this document are from the original source code produced, and therefor when using this software screens may differ slightly in appearance.  Upgrades include a second text display window that allows you to view the time precision and take eclipse status symultaneously.  Additionally formatting of datetime and exposure times during the Take Eclipse execution is improved to produce clarity for the user. [1] 

## Test Screen Demonstration

![gui cam preview example](https://user-images.githubusercontent.com/8731829/37075741-d854f49e-2198-11e8-944d-91428cc92fed.png)

###### **Figure 1:**  Example solar eclipse camera setup. [2]
 
## Required Hardware 
![setup1](https://user-images.githubusercontent.com/8731829/37075790-1dd0c070-2199-11e8-943d-86da87dd7944.png)

###### **Figure 2:** Basic hardware setup : Raspberry Pi 3, Uptronics GPS Expansion Board, Picamera v2.1 module, 3D printed adapter for camera lense, hdmi + monitor + keyboard + mouse, tripod, and mounting platform.  

## GUI Flowchart

![gui fixed](https://user-images.githubusercontent.com/8731829/37075358-191913b8-2197-11e8-9bd4-fb16ce68e972.png)

###### **Figure 3:** Simplified sequence diagram for GUI.
This includes sequence of events to be completed to successfully operate the solar eclipse camera.  The program purposely disables buttons to ensure users operate the camera correctly.  The camera preview and quit buttons are both executable at any time.  Take GPS, Compute Contact Times, and Time Preciscion must be executed sequentially.  




## Take GPS 

**Saving Position Data**

![gps_calibration1](https://user-images.githubusercontent.com/8731829/37075128-e4ed8b38-2195-11e8-96dc-8ac75d14aa69.JPG)

###### **Figure 4:** GPS Data Acquisition 
During the calibration, the GPS module acquires signal and stores locations to a .dat file.  Multithreading was implemented to resolve the to enable real time text updates to the GUI, and event handling was implemented to resolve prevent the program from crashing.  See line 197 of megamovie_Akira_Simulate_Eclipse.py for an example of Event Handling in Qt.  The line reads QtCore.QCoreApplication.processEvents(). This function tells Qt to process any pending events, and then returns control to the caller.[3]


**Performing the Calibration Calculation**

![gps_calibration2](https://user-images.githubusercontent.com/8731829/37075215-625be93e-2196-11e8-9b6a-83c22b7b86ad.JPG)

###### **Figure 5:** GPS Calibration
After collecting GPS positions and storing to .dat files for 1 minute, the program then computes the average of the last 20 saved positions to complete the calibration.  


## Contact Times

![times precision data](https://user-images.githubusercontent.com/8731829/37077481-cf12c020-21a0-11e8-9a83-197f9d1699d0.JPG)

###### **Figure 6:** Computation
We use the calibrated postion to compute the contact times of the total solar eclipse.  Values from this example indicate that totality did not occur in California.  To test the behavior of the camera, we simulated totality by using a GPS position of a location on the path of totality.  

## Time Precision

![jitter format2](https://user-images.githubusercontent.com/8731829/37075221-6ab57f00-2196-11e8-8a54-be2d6ba191fd.JPG)

###### **Figure 7:**  Jitter

Jitter is displayed for the purpose of encouraging the user to set-up early the camera early. This value gradualy progresses toward zero. 

## Take Eclipse

![sleeping](https://user-images.githubusercontent.com/8731829/37075272-a948524c-2196-11e8-9ee1-b6b89bd03309.JPG)

###### **Figure 8:**  Set Up

The user will want to use the camera preview feature within 5 to 10 minutes of capturing the eclipse to ensure that the sun is in the frame of view of the camera. Program will check every second to see if the clock indicates the time (2nd contact - 20 seconds) computed in the Contact Times phase of the program.  Until time (2nd contact - 20 seconds) is reached, the program indicates it is sleeping. 

**Burst Capture Sequence**

![take-out-filter](https://user-images.githubusercontent.com/8731829/37075310-e4f65a50-2196-11e8-81f2-34fe3f09744e.jpg)

###### **Figure 9:** Fixed burst exposure times
Once the indicated time is reached, the program automates the camera to take photographs in a burst capture sequence at fixed exposure times of 1/1000 seconds.  The program saves the image as the datetime value, and prints to the screen for each image captured.  Additionally, 5 seconds before totality a notification to remove the filter will appear on the screen.

![burst movie reel](https://user-images.githubusercontent.com/8731829/37075425-5de2974e-2197-11e8-8cc4-d9dabd74d475.png)

###### **Figure 10:**  Rapid fixed exposure burst.  
Sample of images captured during a test at Charbot Space Center in Oakland, California.  Note that actual exposure times in this photo may be different, this is simply for demonstration purposes.  Actual images are saved in RAW format.

**Bracketed Capture Sequence**

![aeb](https://user-images.githubusercontent.com/8731829/37075338-02ffb406-2197-11e8-9e3b-e85340b110a7.JPG)

###### **Figure 11:**  Bracketed exposure times
Once the 2nd contact time is reached, the program automates the camera to take photographs in a bracketed capture sequence at iterated exposure rates.  In the GUI image, the print out indicates images being taken at exposure times of 1/125, 1/60, 1/30, 1, and 1/2 seconds.[4]  The program saves the image as the datetime value, and prints to the screen for each image captured.  Additionally, 5 seconds before totality a notification to remove the filter will appear on the screen.  The screen will also send a notification 5 before the 3rd conact time to notify the user to put the filter back on, as it will finally take photographs in the burst capture sequence for 20 more seconds.

![bracketing movie reel](https://user-images.githubusercontent.com/8731829/37075440-68ff1df0-2197-11e8-9987-70d1f52f7e7e.png)

###### **Figure 12:**  Bracketed Photo Reel
Demonstration of the Bracketed image sequence.  Bracketing exposure times enables the photographs to be recompiled into a composite image that will accurately to capture the full dynamic range and results in an image that looks similar to one would see in person.



## Footnotes

[1] In the Bracketed Image Capture Sequence subsection of Take Eclipse the expose time above the image file captured is displaying only the denominator of the exposure time.  Dividing 1 by the value printed is what the program is actually doing. 

[2] The actual screenshot in the monitor background is taken using VNC viewer.  Because the camera preview is displayed using the raspberry pi's GPU, you will not be able to view the the camera preview in VNC viewer.  This is just to demonstrate how the camera preview would look on the raspberry pi.

[3] References information found on this page: http://www.informit.com/articles/article.aspx?p=1405544&seqNum=3

[4] Regaurding the first footnote, the intended image capture sequence would be 1/125, 1/60, 1/30, 1/2, 1.  This will produce images that gradually become brighter.


## Credits 

- [Akira Demoss](https://github.com/akirademoss)
- Juan Carlos Martínez Oliveros
- Siuling Pau






