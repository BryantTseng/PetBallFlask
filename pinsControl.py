from __future__ import print_function
#from flaskext.mysql import MySQL
from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time
import sys
import os
from subprocess import Popen
import pygame
import socket

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   11 : {'name' : 'Red', 'state' : GPIO.LOW},
   13 : {'name' : 'Green', 'state' : GPIO.LOW},
   15 : {'name' : 'Blue', 'state' : GPIO.LOW}
   }
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)
ipaddress = "0.0.0.0"

@app.route("/")
def hello():
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
    print("hello", file=sys.stderr)
    return 'hello world'

@app.route("/status")
def data():
    for pin in pins:
       pins
    return  
@app.route('/camera/<command>')
def camera(command):
    if command =='start':
        #p = Popen(['ls'])
        p = Popen(['raspvid', '-t', '999999', '-h', '1080', '-w', '1920', '-fps', '30', '-hf', '-b', '2000000', '-o', '-', '|', 'gst_launch-1.0', '-v', 'fdsrc', '!', 'h264parse', '!', 'rtph264pay', 'config-interval=1', 'pt=96', '!', 'gdppay', '!', 'tcpserversink', 'host=', ipaddress, 'port=5000')
        #os.system("raspivid -t 999999 -h 1080 -w 1920 -fps 30 -hf -b 2000000 -o - | gst-launch-1.0 -v fdsrc ! h264parse !  rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host= "+ipaddress+" port=5000")
    elif command == 'stop':
        print('stop')
    elif command == 'capture':
        print('capture')
    return 'camera'
@app.route('/movemment/<action>')
def command(action):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1',8998))
    direction = request.args.get('direction')
    if direction == '1':    
        if action == 'go':
            s.send('111')
        elif action =='stop':
            s.send('110')
    elif direction == '2':
        if action == 'go':
            s.send('121')
        elif action =='stop':
            s.send('120')
    elif direction == '3':
        if action == 'go':
            s.send('131')
        elif action =='stop':
            s.send('130')
    elif direction == '4':
        if action == 'go':
            s.send('141')
        elif action =='stop':
            s.send('140')
    data = s.recv(1024)
    print(data)
    return "yo"
            
@app.route('/color/<color>')
def color(color):
    if color == 'Yellow':
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(15, GPIO.LOW)
        print('yellow')
    elif color == 'Blue':
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(15, GPIO.LOW)
        print('blue')
    return 'color shown'
@app.route('/music/<track>')
def music(track):
    pygame.mixer.init()
    if track == 'a':
        pygame.mixer.music.load('cartoon001.wav')
    elif track == 'b':
        pygame.mixer.music.load('b')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    return 'music played'
@app.route("/readPin/<pin>")
def readPin(pin):
   try:
      GPIO.setup(int(pin), GPIO.IN)
      if GPIO.input(int(pin)) == True:
         response = "Pin number " + pin + " is high!"
      else:
         response = "Pin number " + pin + " is low!"
   except:
      response = "There was an error reading pin " + pin + "."

   templateData = {
      'title' : 'Status of Pin' + pin,
      'response' : response
      }

   return render_template('pin.html', **templateData)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)