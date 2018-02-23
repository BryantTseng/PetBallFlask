import sys
import os
os.system("raspivid -t 999999 -h 1080 -w 1920 -fps 30 -hf -b 2000000 -o - | gst-launch-1.0 -v fdsrc ! h264parse !  rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host= "+ipaddress+" port=5000")