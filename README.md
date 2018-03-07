# Solar Eclipse MegaMovie
This projected was funded by grant No. AGS-14612277 and conducted under PI 
Juan Carlos Martinez Oliveroz and co-PI Laura Peticolas
at UC Berkeley Space Sciences Lab

# Required Hardware 

![setup1](https://user-images.githubusercontent.com/8731829/37075790-1dd0c070-2199-11e8-943d-86da87dd7944.png)

**Figure 1:** The basic required components for the raspberry pi powered solar eclipse camera set-up consists of an Uptronics GPS Expansion Board, Raspberry Pi 3, Picamera v2.1 module, 3D printed adapter for camera lense, hdmi + monitor + keyboard + mouse, tripod, and mounting platform.  In this instance, we used a set-up that mounted the raspberry pi and GPS hat between two pieces of wood.

# GUI Flowchart

![gui fixed](https://user-images.githubusercontent.com/8731829/37075358-191913b8-2197-11e8-9bd4-fb16ce68e972.png)



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
