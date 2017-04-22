from main import *
import random
from flask import Flask
import time
app = Flask(__name__)

datapins = [13, 16, 22, 24, 25, 5, 18, 4, 17, 23]
clockpin = 27

class Snake:
    snake = []
    apples = []
    snake_color = 0x00FFFF
    apple_color = 0xFF00FF
    direction = (0, 1) # (x, y)
    url = "/snake"
    def __init__(self, screen):
        self.screen = screen
        self.screen.clear()
        self.add_point(self.random_location(padding=2))
        self.add_apple()
        self.setup_server()
    def add_point(self, coordinates):
        self.snake.append(coordinates)
        self.screen.set_pixel(coordinates, self.snake_color)
        self.screen.render()
    def random_location(self, padding=0):
        while True:
            x = random.randint(0 + padding, 19 - padding)
            y = random.randint(0 + padding, 39 - padding)
            if (x, y) not in self.snake and (x, y) not in self.apples:
                break
        return(x, y)
    def set_dir(self, direction):
        if (direction[0] + self.direction[0]) != 0 and (direction[1] + self.direction[1]) != 0:
            self.direction = direction
    def remove_tail(self):
        self.screen.set_pixel((self.snake[0][0], self.snake[0][1]), 0)
        self.snake.pop(0)
    def move(self, eat=False):
        print(self.apples)
        old = self.snake[-1]
        new = (old[0] + self.direction[0], old[1] + self.direction[1])
        self.add_point(new)
        if new in self.apples:
            self.remove_apple(new)
            self.add_apple()
        else:
            self.remove_tail()
    def add_apple(self):
        l = self.random_location()
        self.apples.append(l)
        self.screen.set_pixel(l, self.apple_color)
    def remove_apple(self, coordinates):
        self.apples.remove(coordinates)
        self.screen.set_pixel(coordinates, self.snake_color)
    def setup_server(self):
        @app.route(self.url + "/up")
        def up():
            self.set_dir((0, -1))
            return "ok"
        @app.route(self.url + "/down")
        def down():
            self.set_dir((0, 1))
            return "ok"
        @app.route(self.url + "/left")
        def left():
            self.set_dir((-1, 0))
            return "ok"
        @app.route(self.url + "/right")
        def right():
            self.set_dir((1, 0))
            return "ok"
        @app.route(self.url + "/move")
        def move_url():
            self.move()
            return "ok"



# while True:
#     cmd = raw_input()
#     if cmd == 'w':
#         s.set_dir((0, -1))
#     elif cmd == 'a':
#         s.set_dir((-1, 0))
#     elif cmd == 's':
#         s.set_dir((0, 1))
#     elif cmd == 'd':
#         s.set_dir((1, 0))
#     s.move()
@app.route("/snake")
def controller():
    return app.send_static_file('snake_controller.html')

if __name__ == "__main__":
    print('run')
    screen = LedScreen(datapins, clockpin, brightness=100)
    screen.display_image('test-img.png')
    time.sleep(1)
    s = Snake(screen)
    app.run(host="0.0.0.0", port=int("5000"))
