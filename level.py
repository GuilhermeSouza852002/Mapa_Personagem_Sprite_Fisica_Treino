import pygame
from support import *
from settings import *
from tiles import Tile, StaticTile
from player import *
from game_data import directory1

class Level:
    def __init__(self, level_data, surface):  #O parâmetro level_data é um dicionário que provavelmente contém informações sobre o nível do jogo, como o mapa, os personagens, inimigos, itens, etc. O parâmetro surface é a superfície do Pygame na qual o nível será desenhado.
        self.display_surface = surface  #inicializa a variável display_surface com a superfície recebida como parâmetro.
        
        # sprite group setup
        self.visible_sprites = CameraGroup()
        self.active_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        
        player_layout = import_csv_layout(level_data['Player'])
        self.player_setup(player_layout)
        
        terrain_layout = import_csv_layout(level_data['Terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'Terrain')
        
        terrain_tiles_images = import_folder_images_dict(directory1)
        print(terrain_tiles_images)
        
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
                    sprite = Player((x, y), [self.visible_sprites, self.active_sprites], self.collision_sprites)
                    self.active_sprites.add(sprite)
                    
    def run(self):
        
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(0)
        
        self.active_sprites.update()
        self.visible_sprites.custom_draw(self.active_sprites)
                    
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(100, 300)

        cam_left = camera_borders['left']
        cam_top = camera_borders['top']
        cam_width = self.display_surface.get_size()[0] - (cam_left + camera_borders['right'])
        cam_height = self.display_surface.get_size()[1] - (cam_top + camera_borders['bottom'])

        self.camera_rect = pygame.Rect(cam_left, cam_top, cam_width, cam_height)

    def custom_draw(self, player):
        for sprite in player.sprites():  # Iterar sobre as sprites do player
            if sprite.rect.left < self.camera_rect.left:
                self.camera_rect.left = sprite.rect.left
            if sprite.rect.right > self.camera_rect.right:
                self.camera_rect.right = sprite.rect.right
            if sprite.rect.top < self.camera_rect.top:
                self.camera_rect.top = sprite.rect.top
            if sprite.rect.bottom > self.camera_rect.bottom:
                self.camera_rect.bottom = sprite.rect.bottom

        self.offset = pygame.math.Vector2(
            self.camera_rect.left - camera_borders['left'],
            self.camera_rect.top - camera_borders['top']
        )

        for sprite in player.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)