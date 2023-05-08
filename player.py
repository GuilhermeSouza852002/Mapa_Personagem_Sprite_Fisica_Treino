import pygame
from support import *
from settings import *

#Corpo do player
class Player(pygame.sprite.Sprite):
    def __init__(self,pos, surface):
        super().__init__()
        self.image = pygame.Surface((32,32))    #tamanho player
        self.image.fill('#FFFFFF')  #cor player
        self.rect = self.image.get_rect(topleft = pos)
        
        #movimentação do player
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 5                           #velocidade player
        #self.gravity = 0.8                       #gravidade
        self.jump_speed = 16                     #velocidade do pulo
        self.display_surface = surface
        self.on_floor = False                    #para o jogador não pular infinitamente, ela começa falsa
        
    def get_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]: #direita
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:  #esquerda
            self.direction.x = -1
        else:
            self.direction.x = 0
            
        if keys[pygame.K_SPACE] and self.on_floor:  #o player so pode pular se apertar espaço e se on_floor for verdadeiro
            self.direction.y = -self.jump_speed
            
    #def apply_gravity(self):
        #self.direction.y += self.gravity
        #self.rect.y += self.direction.y
    
    def update(self):
        self.get_input()
        self.rect.x += self.direction.x * self.speed
        #self.apply_gravity()