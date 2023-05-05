import pygame
from support import import_csv_layout, import_cut_graphics, import_folder_images_dict
from settings import tiles_size
from tiles import Tile, StaticTile

directory = 'Graphics/Terrain/TilesMapas'

class Level:
    def __init__(self,level_data,surface):
        self.display_surface = surface
        
        terrain_layout = import_csv_layout(level_data['Terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'Terrain')
        
        terrain_tiles_images = import_folder_images_dict('Graphics/Terrain/TilesMapas') #função Python que usa a biblioteca Pygame para carregar imagens de uma pasta especificada e retorna um dicionário que mapeia os nomes das imagens (sem a extensão do arquivo) para objetos de imagem 
        print(terrain_tiles_images)
        
    #percorre as linhas do mapa e as númera
    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):    #lendo linha por linha do level_map horizontal
            for col_index, val in enumerate(row):   #lendo colunas na vertical
                if val != '-1':
                    x = col_index * tiles_size  #obtendo a posição de x
                    y = row_index * tiles_size  #obtendo a posição de y
    
            
                   
                    if type == 'Terrain':
                                sprite = Tile(tiles_size,x,y)
                                
                                terrain_tile_list = import_cut_graphics(directory) #criando lista de sprites aq
                                #print(len(terrain_tile_list))
                                
                                tile_surface = terrain_tile_list[int(val)]  #aq
                                sprite = StaticTile(tiles_size,x,y,tile_surface) #criando sprite aq
                                sprite_group.add(sprite)
                                
        return sprite_group
        
    def run(self):
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(0)