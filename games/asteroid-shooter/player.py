import pygame

class Player(pygame.sprite.Sprite) :
    def __init__(self, x, y, max_x, max_y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.max_x = max_x
        self.max_y = max_y
        self.width = width
        self.height = height
        self.original_image = pygame.image.load('ship.png')
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (x, y))
        self.velocity = 5
        self.pv = 10
        self.pv_img = pygame.image.load('heart.png')
        self.score = 0

    def point_at(self, x, y):
        direction = pygame.math.Vector2(x, y) - self.rect.center
        angle = direction.angle_to((0, -1))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, x, y):
        if (self.rect[0] <= 0 and x < 0):
            x = 0
        if (self.rect[0] + self.width > self.max_x and x > 0):
            x = 0
        if (self.rect[1] <= 0 and y < 0):
            y = 0
        if (self.rect[1] + self.height > self.max_y and y > 0):
            y = 0
        self.rect.move_ip(x * self.velocity, y * self.velocity)
