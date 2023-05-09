import math
import random
import sys

import pygame
import Functions
class Enemy(pygame.sprite.Sprite):
    def __init__(self,health, speed, attackdamage, location):
        super(Enemy, self).__init__()
        self.speed=speed
        self.health=health
        self.attackdamage=attackdamage
        self.Location = location
        self.smallLocation = (location[0]/5, location[1]/5)
        self.image = pygame.Surface((15,15))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = location[0] * 5
        self.rect.y = location[1] *5
        self.smallimage = pygame.Surface((3,3))
        self.overlaprect = self.smallimage.get_rect()
        self.overlaprect.x = location[0]
        self.overlaprect.y = location[1]
        self.weapon = basicsword()
        self.weapon = 0
        self.weapon = basicsword()
    def moveToPlayer(self, playerlocation, obstructions):
        self.Location = (self.rect.x, self.rect.y)
        self.smallLocation = (self.Location[0] / 5, self.Location[1] / 5)
        self.overlaprect.x = self.smallLocation[0]
        self.overlaprect.y = self.smallLocation[1]
        distance = math.sqrt((playerlocation[0]-(self.smallLocation[0]))**2 + (playerlocation[1]-(self.smallLocation[1]))**2)
        if distance < 150 and not -5<distance < 5:
            angle = math.atan2((playerlocation[1] - (self.smallLocation[1])), (playerlocation[0] - (self.smallLocation[0])))
            collides = self.overlaprect.collidelistall(obstructions.sprites())
            if collides != []:
                overlapRect = self.overlaprect.clip(obstructions.sprites()[collides[0]])
                collidetester = collides[0]
                panic = False
                if overlapRect.width == overlapRect.height:
                    print('i hate bug fixing')
                    if len(collides) == 1:
                        panic = True
                    else:
                        overlapRect = self.overlaprect.clip(obstructions.sprites()[collides[1]])
                        collidetester = collides[1]
                        if overlapRect.width == overlapRect.height:
                            panic = True
                print(overlapRect.width, overlapRect.height)
                print(panic)
                if overlapRect.width > overlapRect.height:
                    print('wtf')
                    if obstructions.sprites()[collides[0]].rect.collidepoint(self.Location[0]/5,self.Location[1]/5) or obstructions.sprites()[collidetester].rect.collidepoint(self.Location[0]/5,self.Location[1]/5):
                        if math.sin(angle) < 0:
                            if math.cos(angle) > 0:
                                self.rect.x += self.speed
                            else:
                                self.rect.x -= self.speed
                        else:
                            self.rect.x += self.speed * math.cos(angle)
                            self.rect.y += self.speed * math.sin(angle)
                        if overlapRect.height > 1:
                            self.rect.y += self.speed*3

                    else:
                        if math.sin(angle) > 0:
                            if math.cos(angle) > 0:
                                self.rect.x += self.speed
                            else:
                                self.rect.x -= self.speed
                        else:
                            self.rect.x += self.speed * math.cos(angle)
                            self.rect.y += self.speed * math.sin(angle)
                        if overlapRect.height > 1:
                            self.rect.y -= self.speed*3
                else:
                    if obstructions.sprites()[collides[0]].rect.collidepoint(self.Location[0]/5,self.Location[1]/5) or obstructions.sprites()[collidetester].rect.collidepoint(self.Location[0]/5,self.Location[1]/5):
                        print('test 1')
                        if math.cos(angle) < 0:
                            if math.sin(angle) > 0:
                                self.rect.y += self.speed
                            else:
                                self.rect.y -= self.speed
                        else:
                            self.rect.x += self.speed * math.cos(angle)
                            self.rect.y += self.speed * math.sin(angle)
                        if overlapRect.width > 1:
                            self.rect.x += self.speed*3
                    else:
                        if math.cos(angle) > 0:
                            print('test 2')
                            if math.sin(angle) > 0:
                                self.rect.y += self.speed
                            else:
                                self.rect.y -= self.speed
                        else:
                            self.rect.x += self.speed * math.cos(angle)
                            self.rect.y += self.speed * math.sin(angle)
                        if overlapRect.height > 1:
                            self.rect.x -= self.speed*3
                print('break')

            else:
                # if angle < 0:
                #     self.rect.x -= self.speed * math.cos(angle)
                #     self.rect.y -= self.speed * math.sin(angle)
                # else:
                self.rect.x += self.speed * math.cos(angle)
                self.rect.y += self.speed * math.sin(angle)
    def Update(self, playerlocation, obstructions, player):
        self.moveToPlayer(playerlocation,obstructions)
        self.Attack(player, playerlocation)
    def Attack(self, player, playerlocation):
        distance = math.sqrt((playerlocation[0]-(self.smallLocation[0]))**2 + (playerlocation[1]-(self.smallLocation[1]))**2)
        if distance <= self.weapon.range:
            if random.randrange(1,50) == 1:
                if random.randrange(1,20) >= player.armourlevel:
                    player.damage(self.weapon.damage)



    def damage(self, damage, level):
        self.health -= damage
        if self.health < 0:
            self.kill()



class basicenemy(Enemy):
    def __init__(self, location):
        super(basicenemy, self).__init__(1,1.5,1, location)
        self.weapon=basicsword()
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
    def Spawn(self):
        enemys = pygame.sprite.Group()
        for i in range(self.NumberEnemys):
            enemys.add(basicenemy((random.randrange(self.Location[0]-10, self.Location[0]+20),random.randrange(self.Location[1]-10, self.Location[1]+20))))
        self.kill()
        return enemys
    def CheckSpawn(self, playerlocation):
        distance = math.sqrt((playerlocation[0]-self.Location[0])**2 + (playerlocation[1]-self.Location[1])**2)
        if distance < 100:
            enemys = self.Spawn()
            return enemys
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
        self.overlaprect = self.rect
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
        self.armourlevel = 0
    def Inventory(self):
        pass
    def Interact(self, interactables):
        for i in interactables.sprites():
            if self.rect.colliderect(i):
                i.Interact()
    def Attack(self, angle, damagables, size):
        self.weilded.attack(angle, self.rect.center, damagables, size, self.level)
    def damage(self, amount):
        print('hit')
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

class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super(Mouse, self).__init__()
        self.InRange = pygame.image.load('./Art/Mouse/Mouse InRange.png').convert()
        self.InRange.set_colorkey((0,0,0))
        self.OutRange = pygame.image.load('./Art/Mouse/Mouse OutRange.png').convert()
        self.OutRange.set_colorkey((0,0,0))
        self.image = self.OutRange
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()
    def Update(self, range, centerofscreen):
            distance = math.sqrt((centerofscreen[0]/5 - self.rect.x/5) ** 2 + (centerofscreen[1]/5 - self.rect.y/5) ** 2)
            self.rect.center = pygame.mouse.get_pos()
            if distance > range:
                self.image = self.OutRange
            else:
                self.image = self.InRange
