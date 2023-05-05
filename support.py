import pygame
import os
from os import walk
from settings import tiles_size
from csv import reader

#transformando o arquivo csv em lista
def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map,delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map  

def import_folder_images_dict(path):    #função para teste dos arquivos, só pra saber se o problema ta no diretorio ou no codigo
    terrain_dict = {}
    
    for folder_name, sub_folders, img_files in walk(path):
        for image_name in img_files:
            full_path = path + '/' + image_name
            image_surf = pygame.image.load(full_path)
            terrain_dict[image_name.split('.')[0]] = image_surf
            
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