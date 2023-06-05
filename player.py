import pygame
from support import *
from settings import *

#Corpo do player
class Player(pygame.sprite.Sprite):
    def __init__(self,pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((32,32))    #tamanho player
        self.image.fill('#FFFFFF')  #cor player
        self.rect = self.image.get_rect(topleft = pos)
        
        #movimentação do player
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 5                           #velocidade player
        self.gravity = 0.8                       #gravidade
        self.jump_speed = 16                     #velocidade do pulo
        self.collision_sprites = collision_sprites
        #self.display_surface = surface
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
        
        #verifica se teve colisão de sprites na horizontal        
    def horizontal_movement_collision(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0:    #se a direção for menor que zero o player esta indo para esquerda
                    self.rect.left = sprite.rect.right  #então a colisão joga o player pra direita
                elif self.direction.x > 0:  #se a direção for maior que zero o player esta indo para direita
                    self.rect.right = sprite.rect.left  #então a colisão joga o player pra esquerda
    
    #verifica se teve colisão de sprites na vertical  
    def vertical_movement_collidion(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:    #se a direção for maior que zero o player esta descendo
                    self.rect.bottom = sprite.rect.top  #então a colisão joga o player pra cima
                    self.direction.y = 0    #zeramos a gravidade para o player não atravessar o chão
                    self.on_floor = True    #se o jogador tocar o chão ele pode pular novamente com essa condição
                elif self.direction.y < 0:  #se a direção for menor que zero o player esta subindo
                    self.rect.top = sprite.rect.bottom  #então a colisão joga o player pra baixo
                    self.direction.y = 0    #zeramos a gravidade para o player não planar ao atingir o teto
                
            if self.on_floor and self.direction.y != 0: # se subirmos ou descermos, assim evita que o jogador possa dar um pulo no ar
                self.on_floor =  False  # o on_floor se torna falso novamente      
            
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
    
    def update(self):
        self.get_input()
        self.rect.x += self.direction.x * self.speed
        self.horizontal_movement_collision()
        self.apply_gravity()
        self.vertical_movement_collidion()
        