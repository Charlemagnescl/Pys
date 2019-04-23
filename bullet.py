import pygame

class Bullet1(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("source/bullet1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = position
        self.speed = 12
        self.live =True
        self.mask = pygame.mask.from_surface(self.image)

    def Move(self):
        self.rect.top -= self.speed

        if self.rect.top < 0:
            self.live = False

    def Reset(self,position):
        self.rect.left,self.rect.top = position
        self.live = True

class Bullet2(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("source/bullet2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = position
        self.speed = 14
        self.live =True
        self.mask = pygame.mask.from_surface(self.image)

    def Move(self):
        self.rect.top -= self.speed

        if self.rect.top < 0:
            self.live = False

    def Reset(self,position):
        self.rect.left,self.rect.top = position
        self.live = True