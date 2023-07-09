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
        #self.image.fill('#FFFFFF')  # cor player
        self.animation_dict = {}  # Dicionário para armazenar as diferentes animações
        self.load_animations()  # Carregar as animações do jogador
        self.rect = self.image.get_rect(topleft=pos)
        
        # movimentação do player
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5  # velocidade player
        self.gravity = 0.8  # gravidade
        self.jump_speed = 16  # velocidade do pulo

        self.last_direction = 'direita'  # Atributo para rastrear a última direção do personagem
        
        self.display_surface = surface
        self.current_x = None
        self.current_animation = None  # Adicione essa linha para definir o atributo current_animation como None
        
        # player status
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        
        
    #sprites do player
    def load_animations(self):
        spritesheet = pygame.image.load('Graphics/Character/AnimationSheet_Character.png')
        
        # Definir as dimensões dos sprites individuais
        sprite_width = 32
        sprite_height = 32

        # Definir as coordenadas de recorte dos sprites para cada animação
        parado_coordinates = [
            (0, 0, sprite_width, sprite_height),    # Coordenadas do primeiro sprite de "pular"
            (32, 0, sprite_width, sprite_height),   # Coordenadas do segundo sprite de "pular"
            # Adicione mais coordenadas de recorte para os outros sprites de "pular"
        ]
        
        pular_coordinates = [
            (0, 160, sprite_width, sprite_height),    # Coordenadas do primeiro sprite de "pular"
            (32, 160, sprite_width, sprite_height),   # Coordenadas do segundo sprite de "pular"
            (64, 160, sprite_width, sprite_height),
            (96, 160, sprite_width, sprite_height),
            (128, 160, sprite_width, sprite_height),
            (160, 160, sprite_width, sprite_height),
            (192, 160, sprite_width, sprite_height),
            (224, 160, sprite_width, sprite_height),
            # Adicione mais coordenadas de recorte para os outros sprites de "pular"
        ]

        andar_direita_coordinates = [
            (0, 96, sprite_width, sprite_height),    # Coordenadas do primeiro sprite de "andar para direita"
            (32, 96, sprite_width, sprite_height),   # Coordenadas do segundo sprite de "andar para direita"
            (64, 96, sprite_width, sprite_height),
            (96, 96, sprite_width, sprite_height),
            (128, 96, sprite_width, sprite_height),
            (160, 96, sprite_width, sprite_height),
            (192, 96, sprite_width, sprite_height),
            (224, 96, sprite_width, sprite_height),
            # Adicione mais coordenadas de recorte para os outros sprites de "andar para direita"
        ]

        andar_esquerda_coordinates = [
            (224, 96, sprite_width, sprite_height),    # Coordenadas do primeiro sprite de "andar para esquerda"
            (192, 96, sprite_width, sprite_height),   # Coordenadas do segundo sprite de "andar para esquerda"
            (160, 96, sprite_width, sprite_height),
            (128, 96, sprite_width, sprite_height),
            (96, 96, sprite_width, sprite_height),
            (64, 96, sprite_width, sprite_height),
            (32, 96, sprite_width, sprite_height),
            (0, 96, sprite_width, sprite_height),
            # Adicione mais coordenadas de recorte para os outros sprites de "andar para esquerda"
        ]
        # Carregar os sprites das animações e adicioná-los ao dicionário de animações
        self.animation_dict['parado'] = self.load_sprites(spritesheet, parado_coordinates)
        self.animation_dict['pular'] = self.load_sprites(spritesheet, pular_coordinates)
        self.animation_dict['andar_direita'] = self.load_sprites(spritesheet, andar_direita_coordinates)
        self.animation_dict['andar_esquerda'] = self.load_sprites(spritesheet, andar_esquerda_coordinates)
        
    def load_sprites(self, spritesheet, coordinates):
        sprites = []
        for coords in coordinates:
            sprite_image = spritesheet.subsurface(pygame.Rect(coords))
            sprites.append(sprite_image)
        return sprites
        
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:  # direita
            self.direction.x = 1
            if self.on_ground:
                self.current_animation = 'andar_direita'
            else:
                self.current_animation = 'pular'

        elif keys[pygame.K_LEFT]:  # esquerda
            self.direction.x = -1
            if self.on_ground:
                self.current_animation = 'andar_esquerda'
            else:
                self.current_animation = 'pular'

        else:
            self.direction.x = 0
            if self.on_ground:
                self.current_animation = 'parado'
            else:
                self.current_animation = 'pular'

        if keys[pygame.K_SPACE] and self.on_ground:
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
        
        if self.current_animation is not None:
            sprites = self.animation_dict[self.current_animation]
            sprite_index = (pygame.time.get_ticks() // 100) % len(sprites)
            self.image = sprites[sprite_index]

        # Espelhar a imagem com base na última direção do personagem
        if self.last_direction == 'esquerda':
            self.image = pygame.transform.flip(self.image, True, False)

        # Atualizar a última direção do personagem se ele estiver se movendo
        if self.direction.x < 0:
            self.last_direction = 'esquerda'
        elif self.direction.x > 0:
            self.last_direction = 'direita'



