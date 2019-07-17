# rpi-stalkerbot
A web interface that allows you to control your raspberry pi robot

## Features
 * Control your robot with buttons or keyboard arrow keys
 * Control rotation of your camera tower with 'W','A','S','D' keys
 * Center the camera tower with 'C' key
 * Change resolution, framerate and rotation of the camera
 * Turn the camera off/on
 * Run scripts saved on raspberry pi
 * Shutdown/reboot raspberry pi

## Installation

### Prerequisites
  * Python3
  * [Pigpio](http://abyz.me.uk/rpi/pigpio/download.html) deamon (must be running - ```sudo pigpiod```) and python library to controll hardware and software PWM
  * [picamera](https://pypi.org/project/picamera/) python module
  * Working network connection
  * Raspberry pi camera (working and enabled)
  * Two continuous rotation motors that are controllable with PWM (I am recommending [this](https://www.pololu.com/product/2820))
  * ### Camera tower
    * Camera tower (I 3d printed [this](https://www.thingiverse.com/thing:1799905/remixes))
    * Two servos to control rotation of the camera tower

On raspberry pi:
```bash
cd
git clone https://github.com/kukosek/rpi-stalkerbot.git
cd rpi-stalkerbot
```

### Setting it up
Edit the file ```server.properties```

### Running it
```bash
cd rpi-stalkerbot
sudo python3 rpi_stalkerbot_server.py
```
Then type the IP adress of your rpi into a browser.

## TODOs
 * telemetry of wifi signal
