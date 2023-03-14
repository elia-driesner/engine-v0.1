import pygame
pygame.init()

class Background:
    def __init__(self): 
        self.foreground = pygame.image.load('assets/map/background/background_layer_1.png')
        self.background = pygame.image.load('assets/map/background/background_layer_2.png')

    # def draw(self, wn):
    #     wn.blit(self.background, (0, 0))
    #     wn.blit(self.foreground, (0, 0))
