import pygame, sys, random, time

from scripts.entity.entity import Entity
from scripts.entity.player import Player, PlayerIndicator
from scripts.map.map import Map
from scripts.map.background import Background
from scripts.text.customfont import CustomFont
from networking.network import Network

class Game:
    def __init__(self):  
        # pygame init
        # self.width, self.height = 960, 540
        self.width, self.height = 1920, 1080
        if self.width == 1920:
            self.display = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.display = pygame.display.set_mode((self.width, self.height))
        self.window = pygame.Surface((1920, 1080))
        pygame.display.set_caption('Smash')
        self.clock = pygame.time.Clock()
        
        self.run = True
        self.max_fps = 60 
        self.scroll = [0, 0]
        self.dt = 0
        self.frame_length = time.time()
        self.render_offset = [0, 0]
        self.screen_shake = 0
        self.camera_smoothing = 8
                
        # player, enemy, map and font init
        self.map = Map(25, (self.width, self.height), './assets/map/map_data/floating-islands.csv', './assets/map/tilesets/grass-tileset.png')
        self.map.load_csv_data()
        self.map.load_images()
        self.map_output = self.map.draw_map(self.scroll)
        self.tile_list = self.map_output[1]
        self.map_surface = self.map_output[0]
        
        self.player_spawn = self.map_output[2]
        self.enemy_spawn = self.map_output[3]
        
        self.player = Player(self.player_spawn, (25, 50))
        self.player.initialize()
        self.player_inicator = PlayerIndicator()
        self.enemy_pos = self.enemy_spawn
        self.enemy = Player(self.enemy_spawn, (25, 50))
        self.enemy.initialize()
        
        self.bg = Background()
        
        self.font = CustomFont()
        self.font.load_font()
        self.fps_text = self.font.write_text('FPS 60', 1)
        
    def loop(self):
        """game loop"""
        # self.n = Network('192.168.110.159', 5555)
        while self.run:
            # pos = (int(self.player.x), int(self.player.y), int(self.n.id))
            # self.enemy_pos = self.n.send(self.n.make_pos(pos))
            # self.enemy_pos = self.n.read_pos(self.enemy_pos)
            if self.enemy_pos:
                self.enemy.x = int(self.enemy_pos[0])
                self.enemy.y = int(self.enemy_pos[1])
                
            if self.player.y > 800:
                self.player.x = self.player_spawn[0]
                self.player.y = self.player_spawn[1]
                self.player.position.x = self.player_spawn[0]
                self.player.position.y = self.player_spawn[1]
            
            self.clock.tick(self.max_fps)
            self.calculate_dt()
            self.events()
            
            self.scroll[0] += int((self.player.rect.x  - self.scroll[0] - (self.width / 2)) / self.camara_smoothing)
            self.scroll[1] += int((self.player.rect.y - self.scroll[1] - (self.height / 2)) / self.camara_smoothing)
            
            self.render()
            self.frame_length = time.time()
    
    def events(self):
        """"checks if window was quit using the x button"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.run = False
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    pygame.quit()
                    self.run = False
                    sys.exit(0)
    
    def render(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.map_surface, (0 - self.scroll[0], 0 - self.scroll[1]))
        self.player.update(self.window, self.dt, self.tile_list, self.scroll)
        self.enemy.draw(self.window, self.scroll)
        self.player_inicator.animations()
        
        self.player_inicator.draw(self.player.rect, self.window, self.scroll)
        
        self.window.blit(self.fps_text, (5, 5))
        
        self.display.blit(self.window, self.render_offset)
        pygame.display.update()
                    
    def calculate_dt(self):
        """Calculates the deltatime between each frame"""
        self.dt = time.time() - self.frame_length
        self.dt *= 60
        self.camara_smoothing = 8 - int(self.dt)
        fps = str(int(self.clock.get_fps()))
        self.fps_text = self.font.write_text(f'{fps} FPS', 1)
                    
game = Game()
game.loop()