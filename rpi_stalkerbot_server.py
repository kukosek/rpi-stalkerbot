import io
from os import listdir
from os.path import isfile, join
import os
import subprocess
from threading import Thread
from time import sleep
import picamera
import logging
import socketserver
from threading import Condition
import threading
from http import server
import pigpio
import urllib.parse
import time
import socket

pi = pigpio.pi()
c = threading.Condition()
secondThreadActive=False





#Second thread that is active when you are moving with the camera
def cam_rotation_handler_thread(direction,speed):
    x=pi.get_PWM_dutycycle(camTiltPin)
    y=pi.get_PWM_dutycycle(camPanPin)
    while secondThreadActive:
        if direction=="up":
            if camPanUpLIMIT>camPanDownLIMIT:
                y+=1
            else:
                y-=1
        elif direction=="down":
            if camPanUpLIMIT>camPanDownLIMIT:
                y-=1
            else:
                y+=1
        elif direction=="left":
            x+=1
        elif direction=="right":
            x-=1
        elif direction=="leftup":
            x+=1
            y-=1
        elif direction=="leftdown":
            x+=1
            y+=1
        elif direction=="rightup":
            x-=1
            y-=1
        elif direction=="leftdown":
            x-=1
            y+=1

        alrightX=False
        alrightY=False
        if camPanUpLIMIT<camPanDownLIMIT:
            if y>camPanUpLIMIT and y<camPanDownLIMIT:
                alrightY=True
        else:
            if y<camPanUpLIMIT and y>camPanDownLIMIT:
                alrightY=True
        if camTiltLeftLIMIT<camTiltRightLIMIT:
            if x>camTiltLeftLIMIT and x<camTiltLeftLIMIT:
                alrightX=True
        else:
            if x<camTiltLeftLIMIT and x>camTiltRightLIMIT:
                alrightX=True
        
        if alrightX:
            pi.set_PWM_dutycycle(camTiltPin,x)
        if alrightY:
            pi.set_PWM_dutycycle(camPanPin,y)

        sleep(speed)
if __name__ == "__main__":
    #Load variables from server properties
    serverDirPath=os.path.dirname(os.path.realpath(__file__))
    PAGE,JAVASCRIPTS,JQUERY,STYLES,FAVICON='','','','',''
    def loadProperties():
        try:
            with open(serverDirPath+'/server.properties', 'r') as file:
            	props = file.readlines()
        except IOError:
            print("ERROR - server.properties missing in the script folder")
            time.sleep(1)
            quit()
        for rawProperty in props:
            if '=' in rawProperty:
                keyAndValue=rawProperty.split('=',1)            
                propertyKey=keyAndValue[0].strip()
                propertyVal=keyAndValue[1].strip()
                if propertyKey=="serverAdress":
                    global serverAdress
                    if propertyVal=="default":
                        serverAdress=''
                    else:
                        serverAdress=propertyVal

                elif propertyKey=="serverPort":
                    global serverPort
                    serverPort=int(propertyVal)

                elif propertyKey=="leftMotorPin":
                    global leftMotorPin
                    leftMotorPin=int(propertyVal)

                elif propertyKey=="rightMotorPin":
                    global rightMotorPin
                    rightMotorPin=int(propertyVal)

                elif propertyKey=="camPanPin":
                    global camPanPin
                    camPanPin=int(propertyVal)

                elif propertyKey=="camTiltPin":
                    global camTiltPin
                    camTiltPin=int(propertyVal)

                elif propertyKey=="ledPin":
                    global ledPin
                    ledPin=int(propertyVal)

                elif propertyKey=="servoFreq":
                    global servoFreq
                    servoFreq=int(propertyVal)

                elif propertyKey=="camPanUpLIMIT":
                    global camPanUpLIMIT
                    camPanUpLIMIT=int(propertyVal)

                elif propertyKey=="camPanDownLIMIT":
                    global camPanDownLIMIT
                    camPanDownLIMIT=int(propertyVal)

                elif propertyKey=="camTiltLeftLIMIT":
                    global camTiltLeftLIMIT
                    camTiltLeftLIMIT=int(propertyVal)

                elif propertyKey=="camTiltRightLIMIT":
                    global camTiltRightLIMIT
                    camTiltRightLIMIT=int(propertyVal)

                elif propertyKey=="camPanCenter":
                    global camPanCenter
                    camPanCenter=int(propertyVal)

                elif propertyKey=="camTiltCenter":
                    global camTiltCenter
                    camTiltCenter=int(propertyVal)

                elif propertyKey=="camRotationSpeed":
                    global camRotationSpeed
                    camRotationSpeed=float(propertyVal)

                elif propertyKey=="userscriptPath":
                    global userscriptPath
                    userscriptPath=propertyVal
                
                elif propertyKey=="reloadFilesOnEveryRequest":
                    global reloadFilesOnEveryRequest
                    if propertyVal=="true" or propertyVal=="True":
                        reloadFilesOnEveryRequest=True
                    else:
                        reloadFilesOnEveryRequest=False

                else:
                    if '#' not in propertyKey and len(propertyKey)!=0:
                        print("Unknown key in properties:",propertyKey,"with value:",propertyVal)
        print("Properties loaded succesfully")
    loadProperties()
    def loadIndex():
        try:
            with open(serverDirPath+'/index.html', 'r') as file:
                PAGE = file.read()
        except IOError:
            print("WARNING - index.html missing in the script folder")
            PAGE="""<html><body><h2>404</h2>
                <p>Index.html is missing in the server folder.<p>"""
        return PAGE
    def loadScripts():
        try:
            with open(serverDirPath+'/scripts.js', 'r') as file:
                JAVASCRIPTS = file.read()
        except IOError:
            print("WARNING - scripts.js missing in the script folder")
            JAVASCRIPTS="//scripts.js missing in the server folder."
        return JAVASCRIPTS
    def loadJquery():
        try:
            with open(serverDirPath+'/jquery-3.4.1.min.js', 'r') as file:
                JQUERY = file.read()
        except IOError:
            print("WARNING - JQUERY missing in the script folder")
            JQUERY="//JQUERY missing in the server folder."
        return JQUERY
    def loadStyles():
        try:
            with open(serverDirPath+'/styles.css', 'r') as file:
                STYLES = file.read()
        except IOError:
            print("WARNING - styles.css missing in the script folder")
            STYLES="/*styles.css missing in the script folder.*/"
        return STYLES
    def loadFavicon():
        try:
            with open(serverDirPath+'/favicon.ico', 'r+b') as file:
                FAVICON = file.read()
                #faviconSize=os.stat('/favicon.ico').st_size
        except IOError:
            print("WARNING - favicon.ico missing in the script folder")
            FAVICON="/*favicon.ico missing in the script folder.*/"
        return FAVICON
    def loadFiles():   
        return(loadIndex(),loadScripts(),loadJquery(),loadStyles(),loadFavicon())

    if reloadFilesOnEveryRequest==False:
        PAGE,JAVASCRIPTS,JQUERY,STYLES,FAVICON=loadFiles()
        print("Server files loaded")
    else:
        print("Skipping server files loading into memory, will load it when a request comes") 
    #CENTER cam controll servos
    def centerCamServos():
        pi.set_PWM_frequency(camPanPin,servoFreq)
        pi.set_PWM_frequency(camTiltPin,servoFreq)
        pi.set_PWM_dutycycle(camPanPin, camPanCenter)
        pi.set_PWM_dutycycle(camTiltPin, camTiltCenter)
    centerCamServos()

    #String function that fetches wlan information
    def WlanInfo(index):
        wlanInfoList=subprocess.run(['/sbin/iw', 'wlan0', 'station','dump'], stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines()
        wlanInfoList.pop(0)
        return wlanInfoList[index]
    
    #Gets local IP of the server
    def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    class StreamingOutput(object):
        def __init__(self):
            self.frame = None
            self.buffer = io.BytesIO()
            self.condition = Condition()
        def write(self, buf):
            if buf.startswith(b'\xff\xd8'):
                # New frame, copy the existing buffer's responseContent and notify all clients it's available
                self.buffer.truncate()
                with self.condition:
                    self.frame = self.buffer.getvalue()
                    self.condition.notify_all()
                self.buffer.seek(0)
            return self.buffer.write(buf)
    class StreamingHandler(server.BaseHTTPRequestHandler):
        def do_GET(self):
            pi.write(ledPin,1)
            if self.path == '/':
                self.send_response(301)
                self.send_header('Location', '/index.html')
                self.end_headers()
            elif self.path == '/index.html':
                if reloadFilesOnEveryRequest:
                    global PAGE
                    PAGE=loadIndex()
                responseContent = PAGE.encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', len(responseContent))
                self.end_headers()
                self.wfile.write(responseContent)
            elif self.path == '/favicon.ico':
                if reloadFilesOnEveryRequest:
                    global FAVICON
                    FAVICON=loadFavicon()
                responseContent = FAVICON
                self.send_response(200)
                self.send_header('Content-Type', 'image/vnd.microsoft.icon')
                self.end_headers()
                self.wfile.write(responseContent)
            elif self.path == '/scripts.js':
                if reloadFilesOnEveryRequest:
                    global JAVASCRIPTS
                    JAVASCRIPTS=loadScripts()
                responseContent = JAVASCRIPTS.encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'text/javascript')
                self.send_header('Content-Length', len(responseContent))
                self.end_headers()
                self.wfile.write(responseContent)
            elif self.path == '/jquery-3.4.1.min.js':
                if reloadFilesOnEveryRequest:
                    global JQUERY
                    JQUERY=loadJquery()
                responseContent = JQUERY.encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'text/javascript')
                self.send_header('Content-Length', len(responseContent))
                self.end_headers()
                self.wfile.write(responseContent)
            elif self.path == '/styles.css':
                if reloadFilesOnEveryRequest:
                    global STYLES
                    STYLES=loadStyles()
                responseContent = STYLES.encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'text/css')
                self.send_header('Content-Length', len(responseContent))
                self.end_headers()
                self.wfile.write(responseContent)
            elif self.path == '/files.txt':
                onlyfiles = [f for f in listdir(userscriptPath) if isfile(join(userscriptPath, f))]
                onlyfilesTxt=""
                for f in onlyfiles:
                    onlyfilesTxt=onlyfilesTxt+f+";"
                responseContent = onlyfilesTxt.encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=UTF-8"')
                self.send_header('Content-Length', len(responseContent))
                self.end_headers()
                self.wfile.write(responseContent)
            elif self.path == '/stream.mjpg':
                self.send_response(200)
                self.send_header('Age', 0)
                self.send_header('Cache-Control', 'no-cache, private')
                self.send_header('Pragma', 'no-cache')
                self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
                self.end_headers()
                try:
                    while True:
                        with output.condition:
                            output.condition.wait()
                            frame = output.frame
                        self.wfile.write(b'--FRAME\r\n')
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', len(frame))
                        self.end_headers()
                        self.wfile.write(frame)
                        self.wfile.write(b'\r\n')
                except Exception as e:
                    logging.warning(
                        'Removed streaming client %s: %s',
                        self.client_address, str(e))
            else:
                self.send_error(404)
                self.end_headers()
            pi.write(ledPin,0)
        def do_POST(self):
                pi.write(ledPin,1)
                action=""
                param=""
                for key,value in dict(urllib.parse.parse_qs(self.rfile.read(int(self.headers['Content-Length'])))).items():
	                if str(key.decode("utf-8"))=="action":
	                    action=str(value[0].decode("utf-8"))
	                elif str(key.decode("utf-8"))=="param":
                    	    param=str(value[0].decode("utf-8"))
                print()
                print("REQUEST action: '"+action+"' Request parameter: '"+param+"'")
                responseContent="wifi-signal:"+WlanInfo(6)[14:]+""
                responseCode=200
                if action=="move":
                    if param=="forward":
                        pi.hardware_PWM(leftMotorPin, 50, 10000)
                        pi.hardware_PWM(rightMotorPin, 50, 100000)
                    elif param=="backwards":
                        pi.hardware_PWM(leftMotorPin, 50, 100000)
                        pi.hardware_PWM(rightMotorPin, 50, 10000)
                    elif param=="left":
                        pi.hardware_PWM(leftMotorPin, 50, 10000)
                        pi.hardware_PWM(rightMotorPin, 50, 10000)
                    elif param=="right":
                        pi.hardware_PWM(leftMotorPin, 50, 100000)
                        pi.hardware_PWM(rightMotorPin, 50, 100000)
                    elif param=="stop":
                        global secondThreadActive
                        c.acquire()
                        secondThreadActive=False
                        c.notify_all()
                        pi.hardware_PWM(leftMotorPin, 50, 1000000)
                        pi.hardware_PWM(rightMotorPin, 50, 1000000)
                    elif param=="forwardLeft":
                        pi.hardware_PWM(leftMotorPin, 50, 10000)
                        pi.hardware_PWM(rightMotorPin, 50, 78000)
                    elif param=="forwardRight":
                        pi.hardware_PWM(leftMotorPin, 50, 65000)
                        pi.hardware_PWM(rightMotorPin, 50, 100000)
                elif action=="cam":
                    if param=="true":
                        camera.start_recording(output, format='mjpeg')
                    elif param=="false":
                        camera.stop_recording()
                elif action=="camRotation":
                    angle=int(param)
                    if angle==0 or angle==90 or angle==180 or angle==270:
                        camera.rotation=angle
                elif action=="camResolution":
                    res=param.split("x")
                    camera.stop_recording()
                    camera.resolution=(int(res[0]),int(res[1]))
                    camera.start_recording(output, format='mjpeg')
                elif action=="camFramerate":
                    fps=int(param)
                    if fps>0 and fps<=60:
                        camera.stop_recording()
                        camera.framerate=fps
                        camera.start_recording(output, format='mjpeg')
                elif action=="shutdown":
                    reboot=int(param)
                    pi.write(ledPin,0)
                    camera.stop_recording()
                    if reboot==0:
                        os.system('sudo shutdown -r now')
                    elif reboot==1:
                        os.system('sudo reboot')
                elif action=="runScript":
                    script=param
                    pi.write(ledPin,0)
                    camera.stop_recording()
                    if ".py" in script:
                        subprocess.Popen(["python3",userscriptPath+script])
                    else:
                        responseCode=404
                        
                elif action=="camMove":
                    if param=="stop":
                        secondThreadActive=False
                    else:
                        secondThreadActive=True
                        thread = Thread(target = cam_rotation_handler_thread, args = (param, camRotationSpeed))
                        thread.start()
                elif action=="camSetPos":
                    xy=param.split(",")
                    x=int(xy[0])
                    y=int(xy[1])
                    if x==0 and y==0:
                        centerCamServos()
                    else:
                        alrightX=False
                        alrightY=False
                        if camPanUpLIMIT<camPanDownLIMIT:
                            if y>camPanUpLIMIT and y<camPanDownLIMIT:
                                alrightY=True
                        else:
                            if y<camPanUpLIMIT and y>camPanDownLIMIT:
                                alrightY=True
                        if camTiltLeftLIMIT<camTiltRightLIMIT:
                            if x>camTiltLeftLIMIT and x<camTiltLeftLIMIT:
                                alrightX=True
                        else:
                            if x<camTiltLeftLIMIT and x>camTiltRightLIMIT:
                                alrightX=True
                        if alrightX:
                            pi.set_PWM_dutycycle(camTiltPin,x)
                        else:
                            responseContent+="camSetPos:X-out-Of-Bounds-Error,"
                        if alrightY:
                            pi.set_PWM_dutycycle(camPanPin,y)
                        else:
                            responseContent+="camSetPos:Y-out-Of-Bounds-Error,"
                else:
                    response=400
                self.send_response(responseCode)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', len(responseContent))
                self.end_headers()
                self.wfile.write(responseContent.encode('utf-8'))
                pi.write(ledPin,0)
    class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
        allow_reuse_address = True
        daemon_threads = True
    with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
        output = StreamingOutput()
        print("Starting PiCamera recording...")
        camera.start_recording(output, format='mjpeg')
        print("Starting streaming server. Device ip:",get_ip()+":"+str(serverPort))
        print()
        try:
            address = (serverAdress, serverPort)          
            server = StreamingServer(address, StreamingHandler)
            server.serve_forever()
        finally:
            camera.stop_recording()
            print("Network error.. Exiting")
            quit()
