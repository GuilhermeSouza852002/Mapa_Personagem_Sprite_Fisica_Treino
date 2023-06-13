import pygame
from support import *
from settings import *
from tiles import Tile, StaticTile
from player import *
from game_data import directory1

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
                    
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8
        
    def run(self):
        # terrain 
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # player sprites
        self.player.update(self.terrain_sprites)
        self.scroll_x()
        self.player.draw(self.display_surface)
