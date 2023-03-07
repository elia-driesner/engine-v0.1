import pygame

class Entity:
    def __init__(self, pos, size):
        self.x, self.y = pos[0], pos[1]
        self.width, self.height = size[0], size[1]