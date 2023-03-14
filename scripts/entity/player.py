import pygame
import time
pygame.init()
from scripts.entity.entity import Entity
from scripts.sprite import Sprite

class Player(Entity):
    def __init__(self, pos, size):
        Entity.__init__(self, pos, size)
        
        # Movement variables
        self.gravity, self.friction = 0.9, -.3
        self.position, self.velocity = pygame.math.Vector2(self.x, self.y), pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        
        self.is_jumping, self.on_ground, self.is_falling = False, False, True
        self.speed = 6
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
        if self.velocity.y > 16: self.velocity.y = 16
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
            self.velocity.y -= 17
            self.rect.y = self.y
            self.on_ground = False
        elif self.double_jump and self.on_ground == False and time.time() - self.last_jump > 0.3:
            self.double_jump = False
            self.is_jumping = True
            self.is_falling = False
            self.velocity.y -= 17
            self.on_ground = False
        if self.velocity.y <= -32.5:
            self.velocity.y = -32
    
    def horizontal_collision(self, tiles):
        """checks for collision left and right and stopps player from moving in that direction"""
        for tile in tiles:
            tile_rect = tile[0].get_rect()
            tile_rect.x = tile[1][0]
            tile_rect.y = tile[1][1]
            if self.rect.colliderect(tile_rect):
                if self.velocity.x > 0:  # Hit tile moving right
                    self.velocity.x = 0
                    self.position.x = tile_rect.left - self.rect.w
                    self.x = self.position.x
                elif self.velocity.x < 0:  # Hit tile moving left
                    self.velocity.x = 0
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
                        self.double_jump = True
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
        
class PlayerIndicator:
    def __init__(self):
        self.size = 13
        self.sprite = Sprite(pygame.image.load(str('assets/images/player/player_indicator.png')), (16, 16), (self.size, self.size))
        self.indicator_image = None
        self.indicator_images = []
        self.x = 0
        self.y = 0
        
        self.animation_frame = 0
        
        self.load_images()
        
    
    def load_images(self):
        for i in range(0, 6):
            self.indicator_images.append(self.sprite.cut(i, 0))
        self.indicator_image = self.indicator_images[0]
        self.rect = self.indicator_image.get_rect()
        
    def animations(self):
        if self.animation_frame > len(self.indicator_images):
            self.animation_frame = 0
        
        if self.animation_frame > 0:
            self.indicator_image = self.indicator_images[int(self.animation_frame)]
        elif self.animation_frame > 1:
            self.indicator_image = self.indicator_images[int(self.animation_frame)]
        elif self.animation_frame > 2:
            self.indicator_image = self.indicator_images[int(self.animation_frame)]
        elif self.animation_frame > 3:
            self.indicator_image = self.indicator_images[int(self.animation_frame)]
        elif self.animation_frame > 4:
            self.indicator_image = self.indicator_images[int(self.animation_frame)]
        elif self.animation_frame > 5:
            self.indicator_image = self.indicator_images[int(self.animation_frame)]
            
        self.animation_frame += 0.1
    
    def draw(self, player_rect, wn, scroll):
        self.indicator_image.set_colorkey((0, 0, 0))
        player_center = player_rect.center
        wn.blit(self.indicator_image, ((player_rect.center[0] - self.size/2) - scroll[0], player_rect.y - player_rect.height / 2 - 8 - scroll[1]))
        
        