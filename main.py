import pygame, sys
from settings import *

#Setup do pygame
#Iniciação do jogo

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height)) #Definindo a janela de exibição
pygame.display.set_caption('Game teste 1')  #Nome do display
clock = pygame.time.Clock() #Pygame que inicializa um relógio Pygame e executa um loop contínuo


#O loop verifica continuamente eventos usando pygame.event.get(), e se o evento for um evento QUIT (como o usuário clicando no botão de fechar), ele fecha o módulo Pygame e sai do programa usando pygame.quit () e sys.exit ().
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    screen.fill('black')
    pygame.display.update() #Atualiza a exibição usando
    clock.tick(fps) #Define a taxa máxima de quadros do jogo
    