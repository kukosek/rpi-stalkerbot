# rpi-stalkerbot
A web interface that allows you to control your raspberry pi robot

## Prerequisites
Working network connection
Raspberry pi camera (working and enabled)
Two continuos rotation motors that are controllable with PWM (I am recommending this https://www.pololu.com/product/2820)
### Camera tower
Camera tower (I 3d printed this: https://www.thingiverse.com/thing:1799905/remixes)
Two servos to control rotation of the camera tower


## Installation
On raspberry pi:
'''cd'''
'''git clone https://github.com/kukosek/rpi-stalkerbot.git''
'''cd rpi-stalkerbot'''

### Setting it up
Edit the file '''server.properties'''

## Running it
'''cd rpi-stalkerbot'''
'''python3 rpi_stalkerbot_server.py'''
Then type the IP adress of your rpi into a browser.
