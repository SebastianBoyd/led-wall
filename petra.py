import main
import time

delay = 0.1
screen = main.LedScreen(brightness=255)
while True:
    screen.display_image('birthday2.png')
    time.sleep(delay)
    screen.display_image('birthday.png')
    time.sleep(delay)
