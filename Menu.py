import pygame
teal = (0,128,128)
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
pygame.init()
myfont = pygame.font.SysFont("freesansbold.ttf", 20)

class GameMenu(pygame.Surface):
    fontSize = 20
    def __init__(self, x, y, width, height):
        super().__init__((width,height))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.optionBoxes = []


    def renderMultiLineLabel(self, text):
        label = []
        for line in text:
            label.append(myfont.render(line, True, white))
        for line in range(len(label)):
            self.blit(label[line], (0, 0+ (line * 20) + (15 * line)))


class StatsScreen(GameMenu):

    def __init__(self, character, x,y,width,height):
        super().__init__(x,y,width,height)
        self.character = character
        pygame.draw.rect(self, teal, self.get_rect())
        self.renderMultiLineLabel(self.prepare_text(character))

    def prepare_text(self,character):
        text = \
        ["Health: {}".format(character.hp),
            "Attack: {}".format(character.attack),
         "Defense: {}".format(character.defense),
         "Movement Speed: {}".format(character.movementSpeed),
         ]
        return text
