import pygame
from support import import_csv_layout, import_cut_graphics, import_folder_images_dict
from settings import tiles_size
from tiles import Tile, StaticTile
from game_data import directory1

class Level:
    def __init__(self,level_data,surface):  #O parâmetro level_data é um dicionário que provavelmente contém informações sobre o nível do jogo, como o mapa, os personagens, inimigos, itens, etc. O parâmetro surface é a superfície do Pygame na qual o nível será desenhado.
        self.display_surface = surface  #inicializa a variável display_surface com a superfície recebida como parâmetro.
        
        terrain_layout = import_csv_layout(level_data['Terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'Terrain')    #chama o método create_tile_group para criar um grupo de sprites (imagens ou objetos que podem ser desenhados na tela) a partir do layout do terreno. O método create_tile_group recebe o layout do terreno e uma string 'Terrain' como parâmetros, e provavelmente retorna um grupo de sprites que representam o terreno do nível. Esses sprites podem ser desenhados na tela posteriormente usando a superfície display_surface.
        
        terrain_tiles_images = import_folder_images_dict(directory1) #função Python que usa a biblioteca Pygame para carregar imagens de uma pasta especificada e retorna um dicionário que mapeia os nomes das imagens (sem a extensão do arquivo) para objetos de imagem 
        print(terrain_tiles_images)
        
    #percorre as linhas do mapa e as númera
    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()    #criar um objeto pygame.sprite.Group(), que é um grupo de sprites vazio.
        for row_index, row in enumerate(layout):    #lendo linha por linha do level_map horizontal
            for col_index, val in enumerate(row):   #lendo colunas na vertical
                if val != '-1': 
                    #o método calcula as coordenadas x e y do sprite com base na linha e coluna atuais do loop, multiplicando-as pelo tamanho dos tiles do jogo (tiles_size).
                    x = col_index * tiles_size  #obtendo a posição de x
                    y = row_index * tiles_size  #obtendo a posição de y
    
            
                   
                    if type == 'Terrain':
                                sprite = Tile(tiles_size,x,y)
                                
                                terrain_tile_list = import_cut_graphics(directory1) #criando lista de sprites 
                                #print(len(terrain_tile_list))
                                
                                tile_surface = terrain_tile_list[int(val)]  
                                sprite = StaticTile(tiles_size,x,y,tile_surface) #criando sprite 
                                sprite_group.add(sprite)    #adiciona as sprites ao sprite_group
                                
        return sprite_group
        
    def run(self):
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(0)