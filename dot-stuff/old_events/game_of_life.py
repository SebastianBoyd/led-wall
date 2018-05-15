DEBUG = True

import pygame, copy, math, random, os, sys
#os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.display.init()

PIXEL_SIZE = 1
WIN_WIDTH = 20
WIN_HEIGHT = 40

#Update every 2ms
REFRESH = 2
TARGET_FPS = 1

if not DEBUG:
    import main
    ledScreen = main.LedScreen(brightness=255)

def fromRGB(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    rgb = (red<<16) + (green<<8) + blue
    return rgb

BLUE = (0, 0, 255)

class Grid():
    def __init__(self, *args, **kwargs):
        self.grid = [[False for i in range(WIN_HEIGHT / PIXEL_SIZE)] for i in range(WIN_WIDTH / PIXEL_SIZE)]

    def setCell(self, x, y, stat):
        self.grid[x][y] = stat
        
    def getCell(self, x, y):
        return self.grid[x][y]
     
    def countNeighbours(self, x, y):
        try:
            count = 0
            if self.getCell(x-1,y-1): count += 1
            if self.getCell(x,y-1): count += 1
            if self.getCell(x+1,y-1): count += 1
            if self.getCell(x-1,y): count += 1
            if self.getCell(x+1,y): count += 1
            if self.getCell(x-1,y+1): count += 1
            if self.getCell(x,y+1): count += 1
            if self.getCell(x+1,y+1): count += 1
            
        except:
            return 0

        return count


 
def drawSquare(background, x, y):
    #Random cell colour
    #colour = random.randint(0,255), random.randint(0,255), random.randint(0,255)
    colour = BLUE
    pygame.draw.rect(background, colour, (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))       

def randomize(grid, background):
    #Create the orginal grid pattern randomly
    for x in xrange(0, WIN_WIDTH / PIXEL_SIZE):
        for y in xrange(0, WIN_HEIGHT / PIXEL_SIZE):
            if random.randint(0, 10) == 1:
                grid.setCell(x, y, True)
                drawSquare(background, x, y)

def main():
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    
    clock = pygame.time.Clock()

    isActive = True
    
    final = pygame.time.get_ticks()
    grid = Grid()

    randomize(grid, background)

    screen.blit(background, (0, 0)) 
    pygame.display.flip()

    while isActive:
       

        clock.tick(TARGET_FPS)
        newgrid = Grid()

        if pygame.time.get_ticks() - final > REFRESH * 100:
            #randomize(grid, background)
            pass
        if pygame.time.get_ticks() - final > REFRESH:
            numActive = 0
            background.fill((0, 0, 0))

            for x in xrange(0, WIN_WIDTH / PIXEL_SIZE):
                for y in xrange(0, WIN_HEIGHT / PIXEL_SIZE):
                    if grid.getCell(x, y):
                        if grid.countNeighbours(x, y) < 2:
                            newgrid.setCell(x, y, False)

                        elif grid.countNeighbours(x, y) <= 3:
                            newgrid.setCell(x, y, True)
                            numActive += 1
                            drawSquare(background, x, y)

                        elif grid.countNeighbours(x, y) >= 4:
                            newgrid.setCell(x, y, False)

                    else:
                        if grid.countNeighbours(x, y) == 3:
                            newgrid.setCell(x, y, True)
                            numActive += 1
                            drawSquare(background, x, y)

            final = pygame.time.get_ticks() 

        else:
            newgrid = grid

  

        #Draws the new grid
        grid = newgrid       

        #Updates screen
        screen.blit(background, (0, 0)) 
        pygame.display.flip()
        
        screen_copy = screen.copy()
        pixels = pygame.surfarray.pixels3d(screen_copy)
        for x, col in enumerate(pixels):
            for y, color in enumerate(col):
                if not DEBUG:
                    ledScreen.set_pixel((x, y), fromRGB(color))
                else:
                    pass
                if fromRGB(color) != 0:
                    print ((x, y), fromRGB(color))
        if not DEBUG:
            ledScreen.render()
       
if __name__ == "__main__":
    main()
