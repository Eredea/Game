import pygame

hp = 10
attack = 7
defense = 8
movementSpeed = 5

defaultStats = {'hp':10,
                'attack':7,
                'defense':8,
                'movementSpeed':5

}
class Character(pygame.sprite.Sprite):

    def __init__(self, imageLoc, characterLoadout = defaultStats, color = None):

        for key, value in characterLoadout.items():
            self.__setattr__(key,value)


        super().__init__()
        self.image =  pygame.image.load(imageLoc)
        self.image.set_colorkey((255,255,255))
