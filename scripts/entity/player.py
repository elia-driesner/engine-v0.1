import pygame
pygame.init()
from scripts.entity.entity import Entity

class Player(Entity):
    def __init__(self, pos, size):
        Entity.__init__(self, pos, size)
        
    def update(self):
        self.draw()
    
    def initialize(self):
        self.load_images('assets/images/player/player_sprite.png', (16, 32), 5, 11)