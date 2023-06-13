import pygame
from support import *
from settings import *

"""
# Classe da câmera
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(screen_width / 2)
        y = -target.rect.y + int(screen_height / 2)

        # Limita a câmera aos limites do cenário
        x = min(0, x)  # limite esquerdo
        y = min(0, y)  # limite superior
        x = max(-(self.width - screen_width), x)  # limite direito
        y = max(-(self.height - screen_height), y)  # limite inferior

        self.camera = pygame.Rect(x, y, self.width, self.height)
"""

# Corpo do player
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface):
        super().__init__()
        self.image = pygame.Surface((32, 32))  # tamanho player
        self.image.fill('#FFFFFF')  # cor player
        self.rect = self.image.get_rect(topleft=pos)
        
        # movimentação do player
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 1  # velocidade player
        self.gravity = 0.8  # gravidade
        self.jump_speed = 16  # velocidade do pulo

        self.display_surface = surface
        self.current_x = None

        # player status
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:  # direita
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:  # esquerda
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:  # o player so pode pular se apertar espaço e se on_floor for verdadeiro
            self.direction.y = -self.jump_speed

    def horizontal_movement_collision(self, terrain_sprites):
        player = self
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = terrain_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self, terrain_sprites):
        player = self
        collidable_sprites = terrain_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True  # Define como verdadeiro quando colide com o chão
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False


    def get_player_on_ground(self):
        if self.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
    
    def update(self, terrain_sprites):
        self.get_input()
        self.rect.x += self.direction.x * self.speed
        self.horizontal_movement_collision(terrain_sprites)
        self.get_player_on_ground()
        self.apply_gravity()
        self.vertical_movement_collision(terrain_sprites)
