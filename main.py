import pygame, sys
from settings import *

#Setup do pygame
#Iniciação do jogo

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height)) #Definindo a janela de exibição
pygame.display.set_caption('Game teste 1')  #Nome do display
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    screen.fill('black')
    pygame.display.update()
    clock.tick(fps)    
    