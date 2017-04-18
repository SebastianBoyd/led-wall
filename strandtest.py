#!/usr/bin/python

import time
import random
from dotstar import Adafruit_DotStar

numpixels = 80 # Number of LEDs in strip

# Here's how to control the strip from any two GPIO pins:
datapin   = 23
clockpin  = 27

# Alternate ways of declaring strip:
# strip   = Adafruit_DotStar(numpixels)           # Use SPI (pins 10=MOSI, 11=SCLK)
# strip   = Adafruit_DotStar(numpixels, 32000000) # SPI @ ~32 MHz
# strip   = Adafruit_DotStar()                    # SPI, No pixel buffer
# strip   = Adafruit_DotStar(32000000)            # 32 MHz SPI, no pixel buf
# See image-pov.py for explanation of no-pixel-buffer use.
# Append "order='gbr'" to declaration for proper colors w/older DotStar strips)

strip.begin()           # Initialize pins for output
strip.setBrightness(255) # Limit brightness to ~1/4 duty cycle


head  = 0               # Index of first 'on' pixel
tail  = -10             # Index of last 'off' pixel
color = 0        # 'On' color (starts red)
colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFF00FF, 0x00FFFF,
          0x2196f3, 0xFF5722, 0x009688, 0x673AB7, 0xE91E63, 0x7ff088]

while True:
    while head < numpixels:
        strip.setPixelColor(head, colors[color]) # Turn on 'head' pixel
        strip.setPixelColor(tail, 0)     # Turn off 'tail'
        strip.show()                     # Refresh strip
        time.sleep(1.0 / 20)             # Pause 20 milliseconds (~50 fps)
        head += 1                        # Advance head position
        tail += 1

    head = 70
    tail = 80

    color +=1
    if color == len(colors):
        color = 0
    while head >= 0:
        strip.setPixelColor(head, colors[color]) # Turn on 'head' pixel
        strip.setPixelColor(tail, 0)     # Turn off 'tail'
        strip.show()                     # Refresh strip
        time.sleep(1.0 / 20)             # Pause 20 milliseconds (~50 fps)
        head = head - 1
        tail = tail - 1

    head = 10
    tail = 0

    color +=1
    if color == len(colors):
        color = 0
