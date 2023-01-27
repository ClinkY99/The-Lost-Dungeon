import pygame
#class Enemy(pygame.sprite.Sprite):


class Tile():
    def __init__(self):
        self.Active = False
        self.wall = [False,False,False,False]
        self.corner = [False,False,False,False]
        self.enemys = False
class EnemySpawn():
    def __init__(self, NumberEnemys, Location):
        self.NumberEnemys= None
        self.Location = None
class StartLoc():
    def __init__(self, Location):
        self.Location = Location
    def Spawn(self):
        pass

class POI():
    def __init__(self, Location, EnemySpawn = False, NumEnemys = 0):
        self.Location = (Location[0]*10, Location[1]*10)
        if EnemySpawn:
            self.NumEnemys = NumEnemys
        else:
            self.NumEnemys = -1

class Objective():
    def __init__(self, location, NumEnemys):
        self.POI = POI(location, True, NumEnemys)
    def Complete(self):
        pass
class Treasure():
    def __init__(self,location, NumEnemys, contains):
        self.POI = POI(location, True, NumEnemys)
        self.contains = contains
    def open(self):
        pass
class Jar():
    def __init__(self,location, NumEnemys):
        self.POI = POI(location, True, NumEnemys)
    def open(self):
        pass

