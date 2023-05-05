import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self,size,x,y):
        super().__init__()
        self.image = pygame.Surface((size,size))    #A imagem do sprite é criada usando a classe pygame.Surface, que recebe um parâmetro de tamanho (size, size). O tamanho do sprite é definido como um quadrado com lados de tamanho size.
        #self.image.fill('grey')             #teste cor no bloco
        self.rect = self.image.get_rect(topleft = (x,y)) #A posição do sprite na janela do jogo é definida pelo retângulo associado à imagem do sprite. O retângulo é criado usando o método get_rect da imagem do sprite e definido com o canto superior esquerdo em (x, y) usando o parâmetro topleft.
        
    def update(self,shift): #O método update é responsável por atualizar a posição do sprite na janela do jogo. Ele faz isso adicionando o valor de shift à posição x do retângulo associado à imagem do sprite, movendo o sprite horizontalmente na janela do jogo. O método update é chamado toda vez que um sprite do terreno é atualizado na janela do jogo.
        self.rect.x += shift
        
class StaticTile(Tile): #é usada para criar sprites de tiles que não se movem, como o chão ou paredes do jogo. 
    def __init__(self,size,x,y,surface):
        super().__init__(size,x,y)
        self.image = surface    #a imagem do sprite é definida como a imagem do tile estático surface.