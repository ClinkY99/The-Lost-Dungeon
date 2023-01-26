import pygame
#class Enemy(pygame.sprite.Sprite):


class Tile():
    def __init__(self):
        self.Active = False
        self.wall = [False,False,False,False]
        self.corner = [False,False,False,False]