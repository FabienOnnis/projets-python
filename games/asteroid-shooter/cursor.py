import pygame

class Cursor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load('striker.png')
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (x, y))

    def move(self, x, y):
        self.rect = self.image.get_rect(center = (x, y))
