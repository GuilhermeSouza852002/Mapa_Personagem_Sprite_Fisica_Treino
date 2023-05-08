import pygame
from support import *
from settings import *
from tiles import Tile, StaticTile
from player import *
from game_data import directory1

class Level:
    def __init__(self,level_data,surface):  #O parâmetro level_data é um dicionário que provavelmente contém informações sobre o nível do jogo, como o mapa, os personagens, inimigos, itens, etc. O parâmetro surface é a superfície do Pygame na qual o nível será desenhado.
        self.display_surface = surface  #inicializa a variável display_surface com a superfície recebida como parâmetro.
        
        player_layout = import_csv_layout(level_data['Player'])
        self.player = pygame.sprite.GroupSingle()
        #self.camera_group = CameraGroup()
        self.player_setup(player_layout)
        
        terrain_layout = import_csv_layout(level_data['Terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'Terrain')    #chama o método create_tile_group para criar um grupo de sprites (imagens ou objetos que podem ser desenhados na tela) a partir do layout do terreno. O método create_tile_group recebe o layout do terreno e uma string 'Terrain' como parâmetros, e provavelmente retorna um grupo de sprites que representam o terreno do nível. Esses sprites podem ser desenhados na tela posteriormente usando a superfície display_surface.
        
        #print dos tijolos do mapa
        terrain_tiles_images = import_folder_images_dict(directory1) #função Python que usa a biblioteca Pygame para carregar imagens de uma pasta especificada e retorna um dicionário que mapeia os nomes das imagens (sem a extensão do arquivo) para objetos de imagem 
        print(terrain_tiles_images)
        
        #print do recorte da spritesheet
        path = 'Graphics/Character/AnimationSheet_Character.png' 

        frames = import_folder(path, frame_width, frame_height)

        # Verificar o conteúdo dos frames
        for i, frames in enumerate(frames):
            print(f"Frames {i+1}:")
            print(frames)
            print("---")
        
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
        
    def player_setup(self,layout):
        for row_index, row in enumerate(layout):
            for col_index,val in enumerate(row):
                x = col_index * tiles_size
                y = row_index * tiles_size
                if val == '0':
                    #print('Jogador aqui!')
                    sprite = Player((x,y),self.display_surface)
                    self.player.add(sprite)
                    
    def run(self):
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(0)
        
        self.player.update()
        self.player.draw(self.display_surface)  # chame o método custom_draw do objeto CameraGroup
                    
class CameraGroup(pygame.sprite.GroupSingle):	#herdando sprite.Group
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()	#estamos dando ao CameraGroup o que queremos desenhar, assim não á necessidade de passar nenhum argumento para custom_draw
		self.offset = pygame.math.Vector2(100,300) #posição superior a esquerda x e y

		# camera
  		# devemos pegar a posição e o tamanho do retângulo
		cam_left = camera_borders['left']	#cria uma borda do tamanho que foi definido o left
		cam_top = camera_borders['top']		#cria uma borda do tamanho que foi definido o top
		#descobrindo a altura e a lagurar do retângulo
		cam_width = self.display_surface.get_size()[0] - (cam_left + camera_borders['right'])	#subtrai a largura total da tela left e right pra gerar a borda da tela da nova largura
		cam_height = self.display_surface.get_size()[1] - (cam_top + camera_borders['bottom'])	#subtrai a autura total da tela top e bottom pra gerar a borda da tela da nova autura

		self.camera_rect = pygame.Rect(cam_left,cam_top,cam_width,cam_height) #pegando a camera que sera movida pelo jogador

	def custom_draw(self,player):
     	# movendo a camera
		if player.rect.left < self.camera_rect.left:	#o player esta mais para a esquerda da camera
			self.camera_rect.left = player.rect.left	#então a camera é destruida e jogada para a esquerda
		if player.rect.right > self.camera_rect.right:	#o player esta mais para a direita da camera
			self.camera_rect.right = player.rect.right	#então a camera é destruida e jogada para a direita
		if player.rect.top < self.camera_rect.top:		#o player esta mais para cima da camera
			self.camera_rect.top = player.rect.top		#então a camera é destruida e jogada para cima
		if player.rect.bottom > self.camera_rect.bottom:#o player esta mais para baixo da camera
			self.camera_rect.bottom = player.rect.bottom#então a camera é destruida e jogada para baixo

		# camera offset 
		# deslocamento da camera
		self.offset = pygame.math.Vector2(
      	# pegando a posição superior esquerda da tela para que o jogador sempre esteja no centro da tela	
			self.camera_rect.left - camera_borders['left'],
			self.camera_rect.top - camera_borders['top'])

		for sprite in self.sprites():	#replicando todos os elementos na tela
			offset_pos = sprite.rect.topleft - self.offset #posição de deslocamento automatico
			self.display_surface.blit(sprite.image,offset_pos) #desenhado todos os elementos na tela