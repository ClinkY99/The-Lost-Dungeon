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
class enemy(pygame.sprite.Sprite):
    def __init__(self, ):
        pass

class Player(pygame.sprite.Sprite):
    def __init__(self, startloc):
        super(Player, self).__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill((210, 75, 222))
        self.tinyimage = pygame.Surface((5,5))
        self.tinyimage.fill((210,75,222))
        self.rect = self.tinyimage.get_rect()
        self.rect.x = startloc[0]
        self.rect.y = startloc[1]
        self.speed = 2
        self.obstruction = None
    def Inventory(self):
        pass
    def Attack(self, angle):
        pass
    def Health(self):
        pass
    def MoveUp(self, moveTime, screensize: tuple):
        if moveTime <= 50:
            location = (screensize[0]/2-25, screensize[1]/2 -moveTime-25)
        else:
            location = (screensize[0]/2 -25, screensize[1]/2-75)
        return location
    def MoveDown(self, moveTime, screensize: tuple):
        if moveTime <= 50:
            location = (screensize[0]/2-25, screensize[1]/2+moveTime-25)
        else:
            location = (screensize[0]/2 -25, screensize[1]/2+25)
        return location
    def MoveLeft(self, moveTime, screensize: tuple):
        if moveTime <= 50:
            location = (screensize[0]/2-25-moveTime, screensize[1]/2-25)
        else:
            location = (screensize[0]/2 -75, screensize[1]/2-25)
        return location
    def MoveRight(self, moveTime, screensize: tuple):
        if moveTime <= 50:
            location = (screensize[0]/2-25+moveTime, screensize[1]/2-25)
        else:
            location = (screensize[0]/2 +25, screensize[1]/2-25)
        return location
    def Sprint(self):
        pass
    def Checkcollisions(self, obstructions):
        for obstruction in obstructions:
            if self.rect.colliderect(obstruction):
                self.obstruction = obstruction
                return True
        return False
    def MoveFromWall(self, speed, camera_X, camera_Y, playerLocation):
        overlaprect = self.rect.clip(self.obstruction)

        if overlaprect.width > overlaprect.height:
            if playerLocation[1] < self.obstruction.y:
                camera_Y += speed
                playerLocation[1] -= speed/5
            else:
                camera_Y -= speed
                playerLocation[1] += speed/5
        else:
            if playerLocation[0] < self.obstruction.x:
                camera_X += speed
                playerLocation[0] -= speed/5
            else:
                camera_X -= speed
                playerLocation[0] += speed/5
        return [camera_X,camera_Y]