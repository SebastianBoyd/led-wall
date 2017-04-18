#!/usr/bin/python

import time
import random
from dotstar import Adafruit_DotStar

numpixels = 80 # Number of LEDs in strip

# Here's how to control the strip from any two GPIO pins:
datapins = [23, 17, 4, 18]
clockpin = 27
strips = []

colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFF00FF, 0x00FFFF,
          0x2196f3, 0xFF5722, 0x009688, 0x673AB7, 0xE91E63, 0x7ff088]

class LedStrip:
    forward = True
    numpixels = 80
    head = 0
    tail = -10
    def random_color(self):
        return random.choice(colors)
    def __init__(self, datapin, clockpin):
        self.datapin = datapin
        self.clockpin = clockpin
        self.strip = Adafruit_DotStar(self.numpixels, self.datapin, self.clockpin, order='bgr')
        self.strip.begin()
        self.strip.setBrightness(255)
        self.color = self.random_color()
    def step(self):
        if self.forward:
            if self.head < self.numpixels:
                self.strip.setPixelColor(self.head, self.color) # Turn on 'head' pixel
                self.strip.setPixelColor(self.tail, 0)     # Turn off 'tail'
                self.head += 1
                self.tail += 1
            else:
                self.color = self.random_color()
                self.head = 70
                self.tail = 80
                self.forward = False

        else: # backwards
            if self.head >= 0:
                self.strip.setPixelColor(self.head, self.color) # Turn on 'head' pixel
                self.strip.setPixelColor(self.tail, 0)     # Turn off 'tail'
                self.head = self.head - 1
                self.tail = self.tail - 1
            else:
                self.head = 10
                self.tail = 0
                self.color = self.random_color()
                self.forward = True
    def render(self):
        self.strip.show()

for d in datapins:
    strips.append(LedStrip(d, clockpin))
while True:
    for s in strips:
        s.step()
    time.sleep(1.0 / 10)
    for s in strips:
        s.render()
