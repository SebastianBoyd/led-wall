""" bounce.py 
    bounce on screen boundary contact
    only change is in ball.checkBounds.
"""

import pygame
import main
import os, sys
os.environ["SDL_VIDEODRIVER"] = "dummy"
def fromRGB(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    rgb = (red<<16) + (green<<8) + blue
    return rgb
ledScreen = main.LedScreen(brightness=255)

#pygame.init()

class Ball(pygame.sprite.Sprite):
    def __init__(self, screen, background):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.background = background
        
        self.image = pygame.Surface((4, 4))
        self.image.fill((0, 0, 0))
        pygame.draw.circle(self.image, (0, 0, 255), (2, 2), 2) 
        self.rect = self.image.get_rect()
        
        self.rect.center = (10, 20)
        
        self.dx = 1
        self.dy = 1
    
    def update(self):
        oldCenter = self.rect.center
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        
        self.checkBounds()        
    
    def checkBounds(self):
        """ bounce on encountering any screen boundary """
        
        if self.rect.right >= self.screen.get_width():
            self.dx *= -1
        if self.rect.left <= 0:
            self.dx *= -1
        if self.rect.bottom >= self.screen.get_height():
            self.dy *= -1
        if self.rect.top  <= 0:
            self.dy *= -1

def main():
    screen = pygame.display.set_mode((20, 40))
    pygame.display.set_caption("Boundary-checking: bounce")
    
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    ball = Ball(screen, background)
    allSprites = pygame.sprite.Group(ball)
    
    clock = pygame.time.Clock()
    keepGoing = True
    
    while keepGoing:
        #clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)\

        pygame.display.flip()

        copy = screen.copy()
        pixels = pygame.surfarray.pixels3d(copy)
        for x, col in enumerate(pixels):
            for y, color in enumerate(col):
                ledScreen.set_pixel((x, y), fromRGB(color))
                pass
        ledScreen.render()
        # del pixels
        # del copy


if __name__ == "__main__":
    main()