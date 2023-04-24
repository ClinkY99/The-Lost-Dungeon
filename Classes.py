import math
import random

import pygame
import Functions
class Enemy(pygame.sprite.Sprite):
    def __init__(self,health, speed, attackdamage, location):
        super(Enemy, self).__init__()
        self.speed=speed
        self.health=health
        self.attackdamage=attackdamage
        self.Location = location
        self.image = pygame.Surface((3, 3))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = location[0]
        self.rect.y = location[1]
        self.Bigimage = pygame.Surface((15,15))
        self.Bigimage.fill((255,0,0))
        self.bigrect = self.Bigimage.get_rect()
        self.bigrect.x = location[0] * 5
        self.bigrect.y = location[1] *5
    def moveToPlayer(self, playerlocation, obstructions):
        distance = math.sqrt((playerlocation[0]-self.Location[0])**2 + (playerlocation[1]-self.Location[1])**2)
        if distance < 200:
            angle = math.atan((playerlocation[1] - self.Location[1]) / (playerlocation[0] - self.Location[0]))
            collides = self.rect.collidelist(obstructions)
            if collides:
                overlapRect = self.rect.clip(collides)
                if overlapRect.width > overlapRect.height:
                    if math.cos(math.radians(angle)) > 0:
                        self.rect.x += self.speed
                    else:
                        self.rect.x -= self.speed
                else:
                    if math.sin(math.radians(angle)) > 0:
                        self.rect.y += self.speed
                    else:
                        self.rect.y -= self.speed
            else:
                self.rect.x += self.speed * math.cos(math.radians(angle))
                self.rect.y += self.speed * math.sin(math.radians(angle))
                self.Location = self.rect.x
                self.Location = self.rect.y

    def Update(self, playerlocation, obstructions):
        self.moveToPlayer(playerlocation,obstructions)
        #draw map stuff

class basicenemy(Enemy):
    def __init__(self, location):
        super(basicenemy, self).__init__(1,1,1, location)
        self.weapon=1
        self.armour=1
class Tile():
    def __init__(self):
        self.Active = False
        self.wall = [False,False,False,False]
        self.corner = [False,False,False,False]
        self.enemys = False
class EnemySpawn(pygame.sprite.Sprite):
    def __init__(self, NumberEnemys, Location):
        super(EnemySpawn, self).__init__()
        self.NumberEnemys= NumberEnemys
        self.Location = Location
    def Spawn(self, playerlocation, matrix, map):
        print("spawned")
        self.kill()
    def CheckSpawn(self, playerlocation, matrix, map):
        distance = math.sqrt((playerlocation[0]-self.Location[0])**2 + (playerlocation[1]-self.Location[1])**2)
        if distance < 5:
            self.Spawn(playerlocation, matrix, map)
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

class Objective(pygame.sprite.Sprite):
    def __init__(self, location, NumEnemys):
        super(Objective, self).__init__()
        self.Location = (location[0] * 10, location[1] * 10)
        self.NumEnemys = NumEnemys
        self.image = pygame.transform.scale_by(pygame.image.load('./Art/Interactables/Objectives/Objective Unactive.png').convert(), 5)
        self.rect = self.image.get_rect()
        self.rect.x = self.Location[0] * 5
        self.rect.y = self.Location[1] * 5
        self.Forms = [self.image]
        for i in range(1,2):
            self.Forms.append(pygame.transform.scale_by(pygame.image.load(f'./Art/Interactables/Objectives/Objective Stage-{i}.png'), 5))
    def Complete(self):
        pass
    def Interact(self):
        self.Activate()
        print('test')
    def Activate(self):
        pass
        #code for fading between images to add "animation"
        #Figure it out future kieran.... :)
        # def BlendSurface(image, pos, alpha):
        #     image.set_alpha(min(1.0, alpha) * 255)
        #     screen.blit(image, pos)
class Treasure(POI):
    def __init__(self, location, direction, NumEnemys, contains):
        super(Treasure, self).__init__(location, NumEnemys=NumEnemys, EnemySpawn= True)
        self.contains = contains
        self.direction = direction
    def open(self):
        pass

class Jar(pygame.sprite.Sprite):
    def __init__(self,location):
        super(Jar, self).__init__()
        self.image = pygame.Surface((10,10))
        self.image.fill((66,245,233))
        self.rect = self.image.get_rect()
        self.rect.x = location[0]*10
        self.rect.y = location[1]*10
        self.bigself = BigJar(location)
    def damage(self, damage, level):
        self.kill()
        level.UpdateChangables()
class BigJar(pygame.sprite.Sprite):
    def __init__(self, location):
        super(BigJar, self).__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((66, 245, 233))
        self.rect = self.image.get_rect()
        self.rect.x = location[0] * 50
        self.rect.y = location[1] * 50

class wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super(wall, self).__init__()
        self.image = pygame.Surface((width,height))
        self.image.fill((127,127,127))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class weapon(object):
    def __init__(self, range, damage):
        super(weapon, self).__init__()
        self.range = range
        self.damage = damage
    def attack(self, angle, startpoint, damagables,size, level):
        hit = Functions.OverlapLine(self.range, angle, startpoint, damagables,size)
        for i in hit:
            i.damage(self.damage, level)

class basicsword(weapon):
    def __init__(self):
        super(basicsword, self).__init__(50,50)


class Player(pygame.sprite.Sprite):
    def __init__(self, startloc, level):
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
        self.weilded = basicsword()
        self.level = level
    def Inventory(self):
        pass
    def Interact(self, interactables):
        for i in interactables.sprites():
            if self.rect.colliderect(i):
                i.Interact()
    def Attack(self, angle, damagables, size):
        self.weilded.attack(angle, self.rect.center, damagables, size, self.level)
    def Health(self):
        pass
    # def MoveUp(self, moveTime, screensize: tuple):
    #     if moveTime <= 50:
    #         location = (screensize[0]/2-25, screensize[1]/2 -moveTime-25)
    #     else:
    #         location = (screensize[0]/2 -25, screensize[1]/2-75)
    #     return location
    # def MoveDown(self, moveTime, screensize: tuple):
    #     if moveTime <= 50:
    #         location = (screensize[0]/2-25, screensize[1]/2+moveTime-25)
    #     else:
    #         location = (screensize[0]/2 -25, screensize[1]/2+25)
    #     return location
    # def MoveLeft(self, moveTime, screensize: tuple):
    #     if moveTime <= 50:
    #         location = (screensize[0]/2-25-moveTime, screensize[1]/2-25)
    #     else:
    #         location = (screensize[0]/2 -75, screensize[1]/2-25)
    #     return location
    # def MoveRight(self, moveTime, screensize: tuple):
    #     if moveTime <= 50:
    #         location = (screensize[0]/2-25+moveTime, screensize[1]/2-25)
    #     else:
    #         location = (screensize[0]/2 +25, screensize[1]/2-25)
    #     return location
    def Checkcollisions(self, obstructions):
        for obstruction in obstructions.sprites():
            if self.rect.colliderect(obstruction):
                self.obstruction = obstruction
                return True
        return False
    def MoveFromWall(self, speed, camera_X, camera_Y, playerLocation):
        overlaprect = self.rect.clip(self.obstruction)
        if overlaprect.width > overlaprect.height:
            if self.rect.y < self.obstruction.rect.y:
                camera_Y += speed
                playerLocation[1] -= speed/5
            else:
                camera_Y -= speed
                playerLocation[1] += speed/5
        else:
            if self.rect.x < self.obstruction.rect.x:
                camera_X += speed
                playerLocation[0] -= speed/5
            else:
                camera_X -= speed
                playerLocation[0] += speed/5
        return [camera_X,camera_Y]
