import pygame
from random import randint
from math import hypot, degrees, atan2

class Asteroid(pygame.sprite.Sprite) :
    def __init__(self, player_x, player_y, SCREEN_WIDTH, SCREEN_HEIGHT):
        pygame.sprite.Sprite.__init__(self)
        self.speed = randint(1, 4)
        self.diameter = randint(15, 50)
        self.pos = (0, 0)
        self.angle = 0
        self.original_image = pygame.image.load('assets/asteroids/asteroid' + str(randint(1, 8)) + '.png')
        self.image = self.original_image

        self.initialiser_coordonnees(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.direction = (player_x - self.pos[0], player_y - self.pos[1])
        length = hypot(*self.direction)
        
        if length == 0.0:
            self.direction = (0, -1)
        else:
            self.direction = (self.direction[0]/length, self.direction[1]/length)

        if (0 <= self.direction[0] < 1):
            self.direction = (1, self.direction[1])
        if (-1 < self.direction[0] < 0):
            self.direction = (-1, self.direction[1])

        if (0 <= self.direction[1] < 1):
            self.direction = (self.direction[0], 1)
        if (-1 < self.direction[1] < 0):
            self.direction = (self.direction[0], -1)

            # Problème avec les entiers et pygame, cette méthode perd en précision et on ne vise pas bien le vaisseau, à revoir

        self.rect = self.image.get_rect(center = self.pos)

    def initialiser_coordonnees(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        # Décider si l'astéroide apparait à droite, à gauche, en haut ou en bas de l'écran
        position = randint(0, 3)

        match position :
            case 0 :
                # Gauche
                self.pos = (0, randint(0, SCREEN_HEIGHT))
            case 1 :
                # Droite
                self.pos = (SCREEN_WIDTH, randint(0, SCREEN_HEIGHT))
            case 2 :
                # Haut
                self.pos = (randint(0, SCREEN_WIDTH), 0)
            case 3 :
                # Bas
                self.pos = (randint(0, SCREEN_WIDTH), SCREEN_HEIGHT)


    def move(self):
        self.rect.move_ip(self.direction[0]*self.speed, self.direction[1]*self.speed)

    def isOutOfRange(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        if not (self.pos[1] < 0 or self.pos[1] > SCREEN_HEIGHT or self.pos[0] < 0 or self.pos[0] > SCREEN_WIDTH):
            return True
        return False
