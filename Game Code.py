import pygame, sys
from pygame.locals import *
import math
import Map
from Map import Hexagon
from Character import Character
import Tiles
import random
from Menu import GameMenu, StatsScreen

screenWidth = 1250
screenHeight = 1250

teal = (0,128,128)
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

colors = [white, black, red, green, blue]

def create_stats_screen(location, character):
    pygame.draw.rect(gameDisplay, red, (*location, 300, 400))
    healthLabel = myFont.render("Hp: {}".format(character.hp), 1, white)
    attackLabel = myFont.render("Attack: {}".format(character.attack), 1, white)
    defenseLabel = myFont.render("Defense: {}".format(character.defense), 1, white)
    movementSpeedLabel = myFont.render("Movement Speed: {}".format(character.movementSpeed), 1, white)

    x,y = location
    labelCoordinates = [(x, y+ i*20) for i in range(4)]
    labels = [healthLabel, attackLabel, defenseLabel, movementSpeedLabel]
    for label, labelCoordinate in zip(labels, labelCoordinates):
        gameDisplay.blit(label, labelCoordinate)

def draw_map(map, display):
    display.fill(black)
    def render_tile(tile):
        pygame.draw.polygon(gameDisplay, tile.color, tile.vertices)
        #TODO Check convert alpha and colorkey to ignore the white
        #tileImage = pygame.image.load(tile.tilePic)
        #tileImage.set_colorkey((255,255,255))
        #gameDisplay.blit(tileImage.convert_alpha(),(tile.xPixel - tileImage.get_rect().size[0] / 2, tile.yPixel - tileImage.get_rect().size[1] / 2) )
        if tile.inhabited:
            gameDisplay.blit(tile.character.image.convert_alpha(), (tile.xPixel - tile.character.image.get_rect().size[0] / 2, tile.yPixel - tile.character.image.get_rect().size[1] / 2))

    for tile in map.tiles:
        render_tile(tile)
    map.hasChanged = False



pygame.init()
clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)

myFont = pygame.font.SysFont("freesansbold.ttf", 20)

car = Character('racecar.png')
mario = Character('MarioPixel.png')
raphael = Character("raphael.png")

gameDisplay.fill(black)
hexagonMap = Map.map()
hexagonMap.place_char(car, hexagonMap.tiles[0])
hexagonMap.place_char(mario, hexagonMap.tiles[1])
hexagonMap.place_char(raphael, hexagonMap.tiles[2])

draw_map(hexagonMap, gameDisplay)


def mouseOnWindowOption(mousePosition, openWindows):
    for window in openWindows:
        for optionsBox in window.optionBoxes:
            if optionsBox.x < mousePosition < optionsBox.width and optionsBox.y > mousePosition > optionsBox.height:
                return optionsBox.action()

    return None



openWindows = set()

def open_window(window, gameDisplay):
    openWindows.add(window)
    gameDisplay.blit(window, (window.x, window.y))

def close_window(window):
    openWindows.remove(window)
    draw_map(hexagonMap, gameDisplay)

statsScreen = StatsScreen(mario, 700, 0, 500, 500)

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def game_intro():
    pass

characterSelected = False
movingChar = False




while True:

    if hexagonMap.hasChanged:
        draw_map(hexagonMap, gameDisplay)
        if openWindows:
            for window in openWindows:
                gameDisplay.blit(window, (window.x,window.y))

    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if mouseOnWindowOption(pos,openWindows):
                mouseOnWindowOption()


            tileSelected = [hexagon for hexagon in hexagonMap.tiles if (hexagon.xCoord, hexagon.yCoord) == Map.pixel_to_offset(pos)][0] if Map.pixel_to_offset(pos) in Map.map.fullMapCoords else hexagonMap.tiles[0]

            if event.button == 1:
                if movingChar:
                    movingChar = False
                    hexagonMap.move_char(movingFrom, tileSelected)

                elif tileSelected.inhabited:
                    movingFrom = tileSelected
                    movingChar = True

            if event.button == 3:
                if tileSelected.inhabited and statsScreen not in openWindows:
                    statsScreen.character = tileSelected.character
                    open_window(statsScreen, gameDisplay)
                elif statsScreen in openWindows:
                    close_window(statsScreen)






        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    pygame.display.update()
