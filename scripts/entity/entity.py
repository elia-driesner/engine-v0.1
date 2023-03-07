import pygame
pygame.init()
from scripts.sprite import Sprite

class Entity:
    def __init__(self, pos, size):
        self.x, self.y = pos[0], pos[1]
        self.width, self.height = size[0], size[1]
        
        self.image = None
        self.rect = None
        self.mask = None
        
    def draw(self, wn):
        """draws the entity on screen"""
        wn.blit(self.image, (self.x, self.y))
    
    def load_images(self, path, image_size, sprite_rows, spite_cols):
        """Gets images from sprite and saves them in a array"""
        
        self.images = [] 
        self.sprite = Sprite(pygame.image.load(str(path)), image_size, (self.width, self.height))
        for i in range(0, sprite_rows):
            row = []
            for j in range(0, spite_cols):
                row.append(self.sprite.cut(j, i))
            self.images.append(row)
        self.image = self.images[0][0]
        self.rect = self.image.get_rect()