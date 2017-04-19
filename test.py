import time
import random
from dotstar import Adafruit_DotStar

numpixels = 80 # Number of LEDs in strip

# Here's how to control the strip from any two GPIO pins:
datapins = [16, 13]
clockpin = 27

a = Adafruit_DotStar(numpixels, datapins[0], clockpin, order='bgr')
a.begin()
a.setBrightness(100)

b = Adafruit_DotStar(numpixels, datapins[1], clockpin, order='bgr')
b.begin()
b.setBrightness(100)

a.setPixelColor(68, 0x0000FF)
a.show()
time.sleep(2)
b.setPixelColor(68, 0x0000FF)
b.show()
