import pygame
from random import *

class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.live=True
        self.image = pygame.image.load("source/enemy0.png")
        self.mask =pygame.mask.from_surface(self.image)
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("source/enemy0_down1.png"),\
            pygame.image.load("source/enemy0_down2.png"),\
            pygame.image.load("source/enemy0_down3.png")])
        self.rect = self.image.get_rect()
        self.width ,self.height = bg_size[0],bg_size[1]
        self.speed =2 
        self.rect.left,self.rect.top = randint(0,self.width - self.rect.width),randint(-5*self.height,0)
    def Move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else :
            self.Reset()
    
    def Reset(self):
        self.rect.left,self.rect.top = randint(0,self.width - self.rect.width),randint(-5*self.height,0)
        self.live=True
        self.hitted = False

class BigEnemy(pygame.sprite.Sprite):
    Hp = 20
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.live=True
        self.image = pygame.image.load("source/enemy2.png")
        self.mask =pygame.mask.from_surface(self.image)
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("source/enemy2_down1.png"),pygame.image.load("source/enemy2_down2.png"),\
            pygame.image.load("source/enemy2_down3.png"),pygame.image.load("source/enemy2_down4.png"),\
            pygame.image.load("source/enemy2_down5.png")])
        self.image_hit = pygame.image.load("source/enemy2_hit.png")
        self.rect = self.image.get_rect()
        self.width ,self.height = bg_size[0],bg_size[1]
        self.speed =1 
        self.rect.left,self.rect.top = randint(0,self.width - self.rect.width),randint(-15*self.height,-5*self.height)
        self.Hp = BigEnemy.Hp
        self.hit = False
        self.hitted = False
    def Move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else :
            self.Reset()
    
    def Reset(self):
        self.rect.left,self.rect.top = randint(0,self.width - self.rect.width),randint(-15*self.height,-5*self.height)
        self.live=True
        self.Hp = BigEnemy.Hp
        self.hitted =False

class MidEnemy(pygame.sprite.Sprite):
    Hp = 8
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.live=True
        self.image = pygame.image.load("source/enemy1.png")
        self.mask =pygame.mask.from_surface(self.image)
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("source/enemy1_down1.png"),\
            pygame.image.load("source/enemy1_down2.png"),\
            pygame.image.load("source/enemy1_down3.png")])
        self.image_hit = pygame.image.load("source/enemy1_hit.png")
        self.rect = self.image.get_rect()
        self.width ,self.height = bg_size[0],bg_size[1]
        self.speed =1 
        self.rect.left,self.rect.top = randint(0,self.width - self.rect.width),randint(-10*self.height,-self.height)
        self.Hp = MidEnemy.Hp
        self.hit = False
        self.hitted = False
    def Move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else :
            self.Reset()
    
    def Reset(self):
        self.rect.left,self.rect.top = randint(0,self.width - self.rect.width),randint(-10*self.height,-self.height)
        self.live=True
        self.Hp = MidEnemy.Hp
        self.hitted = False