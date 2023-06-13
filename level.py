import pygame
from support import *
from settings import *
from tiles import Tile, StaticTile
from player import *
from game_data import directory1

class Camera:
    def __init__(self, display_surface, player):
        self.display_surface = display_surface
        self.player = player
        self.world_shift = pygame.Vector2(0, 0)

    def update(self):
        player_x = self.player.rect.centerx
        player_y = self.player.rect.centery

        if player_x < screen_width / 4 and self.player.direction.x < 0:
            self.world_shift.x = 4
            self.player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and self.player.direction.x > 0:
            self.world_shift.x = -4
            self.player.speed = 0
        else:
            self.world_shift.x = 0
            self.player.speed = 4

        if player_y < screen_height / 4 and self.player.direction.y < 0:
            self.world_shift.y = 4
            self.player.speed = 0
        elif player_y > screen_height - (screen_height / 4) and self.player.direction.y > 0:
            self.world_shift.y = -4
            self.player.speed = 0
        else:
            self.world_shift.y = 0
            self.player.speed = 4

    def apply(self, sprite):
        sprite.rect.x += self.world_shift.x
        sprite.rect.y += self.world_shift.y

    def apply_to_group(self, sprite_group):
        for sprite in sprite_group:
            self.apply(sprite)

class Level:
    def __init__(self, level_data, surface):  #O parâmetro level_data é um dicionário que provavelmente contém informações sobre o nível do jogo, como o mapa, os personagens, inimigos, itens, etc. O parâmetro surface é a superfície do Pygame na qual o nível será desenhado.
        # general setup
        self.display_surface = surface  #inicializa a variável display_surface com a superfície recebida como parâmetro.
        self.world_shift = 0
        
        # player
        player_layout = import_csv_layout(level_data['Player'])
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
        
        # terrain setup
        terrain_layout = import_csv_layout(level_data['Terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'Terrain')
        
        #Camera
        camera = Camera(self.display_surface, self.player.sprite)
        self.camera = camera
        
        #print terrain
        terrain_tiles_images = import_folder_images_dict(directory1)
        print(terrain_tiles_images)
        
        #print spritesheets
        path = 'Graphics/Character/AnimationSheet_Character.png'
        frames = import_folder(path, frame_width, frame_height)
        
        for i, frames in enumerate(frames):
            print(f"Frames {i+1}:")
            print(frames)
            print("---")
        
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tiles_size
                    y = row_index * tiles_size
                   
                    if type == 'Terrain':
                        sprite = Tile(tiles_size, x, y)
                        
                        terrain_tile_list = import_cut_graphics(directory1)
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tiles_size, x, y, tile_surface)
                        sprite_group.add(sprite)
                                
        return sprite_group
        
    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tiles_size
                y = row_index * tiles_size
                if val == '0':
                    sprite = Player((x,y),self.display_surface)
                    self.player.add(sprite)
        
    def run(self):
        self.camera.update()

        # terrain
        self.camera.apply_to_group(self.terrain_sprites)
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # player sprites
        self.camera.apply(self.player.sprite)
        self.player.update(self.terrain_sprites)
        self.player.draw(self.display_surface)
