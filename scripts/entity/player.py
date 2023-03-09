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
        self.speed = 3
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
        self.limit_velocity(12)
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
    
    def jump(self):
        """checks if player is able to jump and sets the velocity"""
        if self.on_ground:
            self.last_jump = time.time()
            self.double_jump = True
            self.is_jumping = True
            self.is_falling = False
            self.velocity.y -= 13
            self.rect.y = self.y
            self.on_ground = False
        elif self.double_jump and self.on_ground == False and time.time() - self.last_jump > 0.3:
            self.double_jump = False
            self.is_jumping = True
            self.is_falling = False
            self.velocity.y -= 13
            self.on_ground = False
        if self.velocity.y <= -15.5:
            self.velocity.y = -15
    
    def horizontal_collision(self, tiles):
        """checks for collision left and right and stopps player from moving in that direction"""
        for tile in tiles:
            tile_rect = tile[0].get_rect()
            tile_rect.x = tile[1][0]
            tile_rect.y = tile[1][1]
            if self.rect.colliderect(tile_rect):
                if self.velocity.x > 0:  # Hit tile moving right
                    self.position.x = tile_rect.left - self.rect.w
                    self.x = self.position.x
                elif self.velocity.x < 0:  # Hit tile moving left
                    self.position.x = tile_rect.right
                    self.x = self.position.x
        self.rect.x = self.x
    
    def vertical_collision(self, tiles):
        """prevents player from falling through ground"""
        self.on_ground = False
        for tile in tiles:
            tile_rect = tile[0].get_rect()
            tile_rect.x = tile[1][0]
            tile_rect.y = tile[1][1]
            if self.rect.colliderect(tile_rect):
                if self.velocity.y >= 0:  # Hit tile from the top
                    self.on_ground = True
                    self.is_jumping = False
                    self.is_falling = False
                    self.velocity.y = 0
                    self.acceleration.y = self.gravity
                    if self.keys[pygame.K_SPACE]:
                        self.position.y = self.y - 20
                        self.rect.y = self.position.y
                    else:
                        self.rect.bottom = tile_rect.top
                elif self.velocity.y < 0:  # Hit tile from the bottom
                    self.velocity.y = 0
                    self.position.y = tile_rect.bottom
                    self.rect.top = self.position.y
        
    
    def limit_velocity(self, max_vel):
        """limits the velocity of the player"""
        min(-max_vel, max(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01: self.velocity.x = 0
          
    def update(self, wn, dt, tiles, scroll):
        """Draws and moves the player"""
        self.keys = pygame.key.get_pressed()
        self.draw(wn, scroll)
        self.horizontal_movement(dt)
        self.horizontal_collision(tiles)
        self.vertical_movement(dt)
        self.vertical_collision(tiles)
    
    def initialize(self):
        """Loads images"""
        self.load_images('assets/images/player/player_sprite.png', (16, 32), 5, 11)