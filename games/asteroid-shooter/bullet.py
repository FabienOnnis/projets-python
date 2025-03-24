import pygame
from math import hypot, degrees, atan2

class Bullet:
    def __init__(self, x, y, mouse_x, mouse_y):
        self.speed = 7
        self.pos = (x, y)
        self.direction = (mouse_x - x, mouse_y - y)
        self.rect = None
        length = hypot(*self.direction)
        
        if length == 0.0:
            self.direction = (0, -1)
        else:
            self.direction = (self.direction[0]/length, self.direction[1]/length)

    def draw(self, surface):
        self.rect = pygame.draw.circle(surface, 'white', self.pos, 3)

    def updatePos(self):
        self.pos = (self.pos[0]+self.direction[0]*self.speed,
                    self.pos[1]+self.direction[1]*self.speed)

    def isOutOfRange(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        if not (self.pos[1] < 0 or self.pos[1] > SCREEN_HEIGHT or self.pos[0] < 0 or self.pos[0] > SCREEN_WIDTH):
            return True
        return False
