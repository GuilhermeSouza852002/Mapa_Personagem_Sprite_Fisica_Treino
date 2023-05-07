import pygame
import os
from os import walk
from settings import tiles_size
from csv import reader

def import_folder(path, frame_width, frame_height): #importar uma pasta de spritesheets em uma lista de superfícies no Pygame. Cada spritesheet é recortada em frames individuais com base nas dimensões fornecidas.
    surface_list = []

    spritesheet = pygame.image.load(path).convert_alpha()
    sheet_width, sheet_height = spritesheet.get_size()

    #o loop externo percorre as linhas (coordenada Y) e o loop interno percorre as colunas (coordenada X). Isso garante que os frames sejam importados corretamente na ordem correta.
    for y in range(0, sheet_height, frame_height):
        for x in range(0, sheet_width, frame_width):
            frame = pygame.Surface((frame_width, frame_height)).convert_alpha() #pygame.Surface((frame_width, frame_height)).convert_alpha() cria uma nova superfície para cada frame com canal alfa habilitado, o que permite uma melhor manipulação e transparência das imagens.
            frame.blit(spritesheet, (0, 0), (x, y, frame_width, frame_height))
            surface_list.append(frame)

    return surface_list

#transformando o arquivo csv em lista
def import_csv_layout(path):
    terrain_map = []    #criada uma lista vazia
    with open(path) as map: # usando a função open e o comando with, que garante que o arquivo seja fechado corretamente após o uso.
        level = reader(map,delimiter = ',') #A função reader recebe dois parâmetros: o arquivo CSV e o delimitador utilizado para separar as colunas do arquivo (neste caso, uma vírgula).
        for row in level:
            terrain_map.append(list(row))   #a função converte a linha em uma lista usando a função list 
        return terrain_map  

def import_folder_images_dict(path):    #função para teste dos arquivos, só pra saber se o problema ta no diretorio ou no codigo
    terrain_dict = {}   #criado um dicionário vazio
    
    for folder_name, sub_folders, img_files in walk(path):  #A função então itera através de todas as pastas e arquivos na pasta especificada em path, usando a função walk do módulo os.
        for image_name in img_files:
            full_path = path + '/' + image_name
            image_surf = pygame.image.load(full_path)
            terrain_dict[image_name.split('.')[0]] = image_surf #A função então usa o método split da string image_name para separar o nome do arquivo e sua extensão, que é usada para criar a chave do dicionário.
            
    return terrain_dict
    

def import_cut_graphics(directory):  #importa todas as imagens de uma determinada pasta, corta-as em pedaços menores e retorna uma lista com todas essas peças.
    
    all_surfaces = []
    all_tiles = []

    #Para utilizá-la, é necessário fornecer o caminho do diretório onde as imagens estão localizadas, utilizando uma string como argumento da função. É importante garantir que todas as imagens da pasta estejam no formato PNG ou JPG.
    # Loop para carregar cada imagem na pasta
    for filename in os.listdir(directory):
        if filename.split('.')[0]:
            # Caminho completo para o arquivo
            file_path = os.path.join(directory, filename)

            #A função percorre todas as imagens da pasta, carrega cada uma delas utilizando a função pygame.image.load(), converte-as para um formato que seja compatível com a superfície de exibição utilizando convert_alpha(), corta a imagem em pedaços menores e adiciona cada um desses pedaços em uma lista.
            # Carregar a imagem e adicioná-la à lista de superfícies
            surface = pygame.image.load(file_path).convert_alpha()
            all_surfaces.append(surface)

            # Cortar a imagem em azulejos
            tile_num_x = int(surface.get_size()[0] / tiles_size)   
            tile_num_y = int(surface.get_size()[1] / tiles_size)

            for row in range(tile_num_y):
                for col in range(tile_num_x):
                    x = col * tiles_size
                    y = row * tiles_size
                    new_surf = pygame.Surface((tiles_size,tiles_size), flags=pygame.SRCALPHA)
                    new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tiles_size, tiles_size))
                    all_tiles.append(new_surf)

    return all_tiles