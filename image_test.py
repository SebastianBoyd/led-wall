#!/usr/bin/python

import time
import random
from dotstar import Adafruit_DotStar
from PIL import Image
import math

datapins = [23, 17, 4, 18, 5, 25, 24, 22, 16, 13]
clockpin = 27
strips = []

colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFF00FF, 0x00FFFF,
          0x2196f3, 0xFF5722, 0x009688, 0x673AB7, 0xE91E63, 0x7ff088]

def fromRGB(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    rgb = (red<<16) + (green<<8) + blue
    return rgb

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
    def display_pixel(self, pos, color):
        self.strip.setPixelColor(pos, color)
    def render(self):
        self.strip.show()
for d in datapins:
    strips.append(LedStrip(d, clockpin))

im = Image.open("test-img.png")
size = im.size
pix = im.getdata()
for i in range(len(pix)):
    y = i / size[0]
    x = i - y * size[0]
    if x % 2 == 0:
        strip = x / 2
        num = 80 - 1 - y
    else:
        strip = (x - 1) / 2
        num = y
    strips[strip].display_pixel(num, fromRGB(pix[i]))
for s in strips:
    s.render()
