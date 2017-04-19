#!/usr/bin/python

import time
import random
from dotstar import Adafruit_DotStar
from PIL import Image
import math

datapins = [13, 16, 22, 24, 25, 5, 18, 4, 17, 23]
clockpin = 27
strips = []

color_library = [0xFF0000, 0x00FF00, 0x0000FF, 0xFF00FF, 0x00FFFF,
          0x2196f3, 0xFF5722, 0x009688, 0x673AB7, 0xE91E63, 0x7ff088]

def fromRGB(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    rgb = (red<<16) + (green<<8) + blue
    return rgb

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

class LedStrip:
    forward = True
    numpixels = 80
    head = 0
    tail = -10
    def random_color(self):
        return random.choice(color_library)
    def __init__(self, datapin, clockpin, brightness):
        self.datapin = datapin
        self.clockpin = clockpin
        self.strip = Adafruit_DotStar(self.numpixels, self.datapin, self.clockpin, order='bgr')
        self.strip.begin()
        self.set_brightness(brightness)
        self.color = self.random_color()
    def set_pixel(self, pos, color):
        self.strip.setPixelColor(pos, color)
    def set_brightness(self, brightness):
        self.brightness = clamp(brightness, 0, 255)
        self.strip.setBrightness(self.brightness)
    def render(self):
        self.strip.show()

class LedScreen:
    strips = []
    def __init__(self, datapins, clockpin, brightness=25):
        self.datapins = datapins
        self.clockpin = clockpin
        self.brightnes = clamp(brightness, 0, 255)
        for d in self.datapins:
            self.strips.append(LedStrip(d, self.clockpin, brightness))
    def set_brightness(self, brightness):
        self.brightness = clamp(brightness, 0, 255)
        for s in self.strips:
            s.set_brightness(brightness)
        self.render()
    def set_pixel(self, x, y, color):
        if x % 2 == 0:
            strip = x / 2
            num = 40 - 1 - y
        else:
            strip = (x - 1) / 2
            num = y + 40
        self.strips[strip].set_pixel(num, color)
    def render(self):
        for s in self.strips:
            s.render()
    def display_image(self, url):
        im = Image.open(url)
        size = im.size
        pix = im.getdata()
        for i in range(len(pix)):
            y = i / size[0]
            x = i - y * size[0]
            self.set_pixel(x, y, fromRGB(pix[i]) )
        self.render()

def test():
    screen = LedScreen(datapins, clockpin, brightness=25)
    while True:
        screen.display_image('test-img.png')
        time.sleep(10)
        screen.display_image('boat.png')
        time.sleep(10)

test()
