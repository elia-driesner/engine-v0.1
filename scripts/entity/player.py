import pygame
import time
pygame.init()
from scripts.entity.entity import Entity

class Player(Entity):
    def __init__(self, pos, size):
        Entity.__init__(self, pos, size)
        
        # Movement variables
        self.gravity, self.friction = .6, -.15
        self.position, self.velocity = pygame.math.Vector2(self.x, self.y), pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        
        self.is_jumping, self.on_ground, self.is_falling = False, False, True
        self.speed = 1.8
        self.double_jump = True
        self.last_jump = time.time()
        
        # animation
        self.steps = 0
        self.animation_duration = 7
        self.flight_duration = 0
        self.direction = 'right'
        self.idle_time = 0
        self.last_image = 0
        self.shake = False
        
    def horizontal_movement(self, dt):
        """checks if player pressed a or d and moves the player in the given direction"""
        self.acceleration.x = 0
        if self.keys[pygame.K_a]:
            self.direction = 'left'
            self.acceleration.x -= self.speed
        elif self.keys[pygame.K_d]:
            self.direction = 'right'
            self.acceleration.x += self.speed
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(7)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
        self.x = self.position.x
        self.rect.x = self.x
    
    def vertical_movement(self, dt):
        """checks if player pressed space and moves the player up or down"""
        if self.keys[pygame.K_SPACE]:               
            self.jump()
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7: self.velocity.y = 7 
        if self.on_ground:                          
            self.is_falling = False
            self.is_jumping = False
            self.velocity.y = 0
        else:
            self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
        if self.y - self.position.y < 0:
            self.is_falling = True
            self.is_jumping = False
        self.y = self.position.y
        self.rect.y = self.y
        
    
    def update(self):
        """Draws and moves the player"""
        self.draw()
    
    def initialize(self):
        """Loads images"""
        self.load_images('assets/images/player/player_sprite.png', (16, 32), 5, 11)