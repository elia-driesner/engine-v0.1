import pygame
pygame.init()

class Background:
    def __init__(self): 
        """handels the moving background"""
        self.line = pygame.image.load('assets/map/background/background_layer_1.png')
        self.background = pygame.image.load('assets/map/background/background_layer_2.png')
        
        self.lines = []
        self.surface = pygame.Surface((1920, 1080 * 4))
        self.offset = 90
        self.add_lines()
        self.move_lines = True

    def draw(self):
        """draws every layer on screen"""
        self.surface.fill((32, 32, 52))
        for line in self.lines:
            pygame.draw.line(self.surface, (5, 5, 20), (line.x + line.width, line.y + line.height), (line.x, line.y), 45)
            if self.move_lines:
                line.move()
        return self.surface

        
    
    def add_lines(self):
        y = -1920
        for i in range(0, 40):
            self.lines.append(Line(0, y, 1920, 1080))
            y += self.offset

class Line:
    def __init__(self, x, y, width, height):
        """a line for the moving background"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed_y = 1
    
    def reset(self):
        """if line is out of the screen it resets"""
        if self.y > self.height:
            self.y = 0 - self.height
    
    def move(self):
        self.y += self.speed_y
        self.reset()
    