import pygame, sys
from pygame.locals import *
import math
import Map
from Map import Hexagon
import itertools
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)



pygame.init()

screenWidth = 1250
screenHeight = 1250
gameDisplay = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)


myfont = pygame.font.SysFont("Comic Sans MS", 15)


gameDisplay.fill(black)

gameSpace = Map.map()
for hexagon in gameSpace.tiles:
    label = myfont.render("{}".format((hexagon.xCoord, hexagon.yCoord)), 1, white)
    gameDisplay.blit(label, (hexagon.xPixel, hexagon.yPixel))


for tile in gameSpace.tiles:
    pygame.draw.polygon(gameDisplay, green, tile.vertices, 1)

carImg = pygame.image.load('racecar.png')
imagePoint = Hexagon((0, 0))
x,y = imagePoint.xCoord, imagePoint.yCoord
gameDisplay.blit(carImg, (x,y))



while True:
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()


            print(pos, Map.pixel_to_offset(pos))



        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
