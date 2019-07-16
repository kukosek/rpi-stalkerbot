# rpi-stalkerbot
A web interface that allows you to control your raspberry pi robot

## Prerequisites
  * Python3
  * [Pigpio](http://abyz.me.uk/rpi/pigpio/download.html) deamon and python library to controll hardware and software PWM
  * [picamera](https://pypi.org/project/picamera/) python module
  * Working network connection
  * Raspberry pi camera (working and enabled)
  * Two continuous rotation motors that are controllable with PWM (I am recommending [this](https://www.pololu.com/product/2820))
  * ### Camera tower
    * Camera tower (I 3d printed [this](https://www.thingiverse.com/thing:1799905/remixes))
    * Two servos to control rotation of the camera tower

## Installation
On raspberry pi:
```bash
cd
git clone https://github.com/kukosek/rpi-stalkerbot.git
cd rpi-stalkerbot
```

### Setting it up
Edit the file ```server.properties```

## Running it
```bash
cd rpi-stalkerbot
sudo python3 rpi_stalkerbot_server.py
```
Then type the IP adress of your rpi into a browser.
