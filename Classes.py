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

class Objective(POI):
    def __init__(self, location, NumEnemys):
        super(Objective, self).__init__(location,NumEnemys= NumEnemys, EnemySpawn= True)
    def Complete(self):
        pass
class Treasure(POI):
    def __init__(self, location, direction, NumEnemys, contains):
        super(Treasure, self).__init__(location, NumEnemys=NumEnemys, EnemySpawn= True)
        self.contains = contains
        self.direction = direction
    def open(self):
        pass
class Jar(POI):
    def __init__(self,location):
        super(Jar, self).__init__(location)
    def open(self):
        pass

