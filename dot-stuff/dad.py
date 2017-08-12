import main
import time

delay = 0.5
screen = main.LedScreen(brightness=255)
while True:
    screen.display_image('nothing.png')
    time.sleep(delay)
    screen.display_image('d.png')
    time.sleep(delay)
    screen.display_image('da.png')
    time.sleep(delay)
    screen.display_image('dad.png')
    time.sleep(delay)
