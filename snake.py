from main import *
import random

datapins = [13, 16, 22, 24, 25, 5, 18, 4, 17, 23]
clockpin = 27

def random_location(padding=0):
    x = random.randint(0 + padding, 19 - padding)
    y = random.randint(0 + padding, 39 - padding)
    return(x, y)

class Snake:
    snake = []
    direction = (0, 1) # (x, y)
    def __init__(self, screen):
        self.screen = screen
        self.screen.clear()
        self.add_point(random_location(padding=2))
    def add_point(self, coordinates):
        self.snake.append(coordinates)
        self.screen.set_pixel(coordinates, 0x00FF00)
        self.screen.render()
    def set_dir(self, direction):
        if (direction[0] + self.direction[0]) != 0 and (direction[1] + self.direction[1]) != 0:
            self.direction = direction
    def move(self, eat=False):
        old = self.snake[-1]
        new = (old[0] + self.direction[0], old[1] + self.direction[1])
        self.add_point(new)

screen = LedScreen(datapins, clockpin, brightness=100)

screen.display_image('test-img.png')
time.sleep(1)
s = Snake(screen)
while True:
    cmd = raw_input()
    if cmd == 'w':
        s.set_dir((0, -1))
    elif cmd == 'a':
        s.set_dir((-1, 0))
    elif cmd == 's':
        s.set_dir((0, 1))
    elif cmd == 'd':
        s.set_dir((1, 0))
    s.move()
