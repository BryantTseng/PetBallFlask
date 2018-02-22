from __future__ import print_function
from flaskext.mysql import MySQL
from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time
import sys
import os
import pygame

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   6 : {'name' : 'LeftMotorForward', 'state' : GPIO.LOW},
   13 : {'name' : 'LeftMotorBackward', 'state' : GPIO.LOW},
   19 : {'name' : 'RightMotorForward','state' : GPIO.LOW},
   26 : {'name' : 'RightMotorBackward','state' : GPIO.LOW},
   11 : {'name' : 'Red', 'state' : GPIO.LOW},
   13 : {'name' : 'Green', 'state' : GPIO.LOW},
   15 : {'name' : 'Blue', 'state' : GPIO.LOW}
   #16 : {'name' : 'test1','state':GPIO,Low},
   #20 : {'name' : 'test2','state':GPIO.Low}
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
        os.system("raspivid -t 999999 -h 1080 -w 1920 -fps 30 -hf -b 2000000 -o - | gst-launch-1.0 -v fdsrc ! h264parse !  rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host= "+ipaddress+" port=5000")
    elif command == 'stop':
        print('stop')
    elif command == 'capture':
        print('capture')
    return 
@app.route('/movemment/<action>')
def command(action):
    direction = request.args.get('direction')
    if direction == '1':    
        if action == 'go':
            GPIO.output(6,GPIO.HIGH)
        elif action =='stop':
            GPIO.output(6,GPIO.LOW)
    elif direction == '2':
        if action == 'go':
            GPIO.output(13,GPIO.HIGH)
        elif action =='stop':
            GPIO.output(13,GPIO.LOW)
    elif direction == '3':
        if action == 'go':
            GPIO.output(19,GPIO.HIGH)
        elif action =='stop':
            GPIO.output(19,GPIO.LOW)
    elif direction == '4':
        if action == 'go':
            GPIO.output(26,GPIO.HIGH)
        elif action =='stop':
            GPIO.output(26,GPIO.LOW)
    return "yo"
            
@app.route('color/<color>')
def color(color):
    if color == 'Red':
        print('red')
    elif color == 'Blue':
        print('blue')
    elif color == 'Green':
        print('green')
    return 'color shown'
@app.route('music/<track>')
def music(track):
    pygame.mixer.init()
    if track == 'a':
        pygame.mixer.music.load('a')
    elif track == 'b':
        pygame.mixer.music.load('b')
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
