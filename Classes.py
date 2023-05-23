import math
import random
import sys

import pygame
import Functions
import ctypes

user32 = ctypes.windll.user32
ScreenLength, ScreenWidth = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

DEFAULT_IMAGE_SIZE = (1280, 720)

class Enemy(pygame.sprite.Sprite):
    def __init__(self,health, speed, attackdamage, location, moneydroprange):
        super(Enemy, self).__init__()
        print("health")
        print(health)
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
        self.weapon = gun()
        self.moneydroprange = moneydroprange
        self.points = 100
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
                    if len(collides) == 1:
                        panic = True
                    else:
                        overlapRect = self.overlaprect.clip(obstructions.sprites()[collides[1]])
                        collidetester = collides[1]
                        if overlapRect.width == overlapRect.height:
                            panic = True
                if overlapRect.width > overlapRect.height:
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
                            if math.sin(angle) > 0:
                                self.rect.y += self.speed
                            else:
                                self.rect.y -= self.speed
                        else:
                            self.rect.x += self.speed * math.cos(angle)
                            self.rect.y += self.speed * math.sin(angle)
                        if overlapRect.height > 1:
                            self.rect.x -= self.speed*3

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
            if random.randrange(1,25) == 1:
                if random.randrange(1,20) >= player.armourlevel:
                    player.damage(self.weapon.damage)
    def damage(self, damage, level):
        self.health -= damage
        if self.health < 0:
            self.kill()
            level.items.add(Coin(self.Location, random.randrange(self.moneydroprange[0], self.moneydroprange[1])))
            level.player.XP += self.points
            level.HUD.UpdateScore(level.player)



class basicenemy(Enemy):
    def __init__(self, location, diffuculty):
        super(basicenemy, self).__init__(random.randrange(1*math.ceil((diffuculty**2/10)),5*math.ceil((diffuculty**2/2))),2,1, location, [75//math.ceil(diffuculty*2/10), 175//math.ceil(diffuculty*2/10)])
        self.weapon=EnemyWeapon(math.ceil(diffuculty**2/25)*3)
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
        self.cooldown = 5000
        self.activetimes = 0
        self.count = -1
    def Spawn(self, diffuculty):
        enemys = pygame.sprite.Group()
        for i in range(self.NumberEnemys):
            enemys.add(basicenemy((random.randrange(self.Location[0]-10, self.Location[0]+20),random.randrange(self.Location[1]-10, self.Location[1]+20)), diffuculty))
        return enemys
    def CheckSpawn(self, playerlocation, diffuculty):
        if self.activetimes > 3:
            self.kill()
        if self.count != -1:
            if self.count > self.cooldown:
                self.count = -1
            else:
                self.count +=1
        else:
            distance = math.sqrt((playerlocation[0]-self.Location[0])**2 + (playerlocation[1]-self.Location[1])**2)
            if distance < 100:
                self.count = 0
                self.activetimes += 1
                enemys = self.Spawn(diffuculty)
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
        self.Forms = [pygame.transform.scale_by(pygame.image.load('./Art/Interactables/Objectives/Objective Unactive.png').convert_alpha(), 5)]
        self.image = self.Forms[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.Location[0] *5
        self.rect.y = self.Location[1] *5
        self.count = 0
        self.player = None
        self.complete = False
        self.completeimage = pygame.transform.scale_by(pygame.image.load('./Art/Interactables/Objectives/Objective Complete.png').convert_alpha(), 5)

        self.value = 5000
        for i in range(1,13):
            self.Forms.append(pygame.transform.scale_by(pygame.image.load(f'./Art/Interactables/Objectives/Objective Stage-{i}.png').convert_alpha(), 5))
    def Complete(self):
        self.complete = True
        self.Forms = None
        self.player.XP += 5000
        self.player.currentlevel.HUD.UpdateScore(self.player)
        return True
    def Interact(self, level):
        self.player = level.player
        return self.Activate()
    def Activate(self):
        if self.count <= 300:
            self.Forms[1].set_alpha(self.count/10)
            self.image.blit(self.Forms[1], (0,0))
        elif self.count <=400:
            self.Forms[2].set_alpha((self.count-300))
            self.image.blit(self.Forms[2], (0, 0))
        elif self.count <= 500:
            self.Forms[3].set_alpha((self.count - 400))
            self.image.blit(self.Forms[3], (0, 0))
        elif self.count == 600:
            self.image.blit(self.Forms[4], (0, 0))
        elif self.count == 700:
            self.image.blit(self.Forms[5], (0, 0))
        elif self.count == 800:
            self.image.blit(self.Forms[6], (0, 0))
        elif self.count == 900:
            self.image.blit(self.Forms[7], (0, 0))
        elif self.count == 1000:
            self.image.blit(self.Forms[8], (0, 0))
        elif 1100<=self.count <= 1200:
            self.Forms[9].set_alpha((self.count - 1100))
            self.image.blit(self.Forms[9], (0, 0))
        elif 1200 < self.count <= 1250:
            self.image.fill((0,0,0))
            self.image.blit(self.Forms[8], (0,0))
            self.Forms[9].set_alpha((1450 - self.count))
            self.image.blit(self.Forms[9], (0, 0))
        elif 1250 <= self.count <= 1300:
            self.Forms[9].set_alpha((self.count - 1200) / 4)
            self.image.blit(self.Forms[9], (0, 0))
        elif 1300 < self.count <= 1350:
            self.image.fill((0, 0, 0))
            self.image.blit(self.Forms[8], (0,0))
            self.Forms[9].set_alpha((1550 - self.count))
            self.image.blit(self.Forms[9], (0, 0))
        elif 1350 <= self.count <= 1400:
            self.Forms[9].set_alpha((self.count - 1300) / 4)
            self.image.blit(self.Forms[9], (0, 0))
        elif 1400 < self.count <= 1450:
            self.image.fill((0, 0, 0))
            self.image.blit(self.Forms[8], (0,0))
            self.Forms[9].set_alpha((1650 - self.count))
            self.image.blit(self.Forms[9], (0, 0))
        elif 1450 <= self.count <= 1500:
            self.Forms[9].set_alpha((self.count - 1400) / 4)
            self.image.blit(self.Forms[9], (0, 0))
        elif 1500 < self.count <= 1550:
            self.image.fill((0, 0, 0))
            self.image.blit(self.Forms[8], (0,0))
            self.Forms[9].set_alpha((1750 - self.count))
            self.image.blit(self.Forms[9], (0, 0))
        elif 1550 <= self.count <= 1650:
            self.Forms[9].set_alpha((self.count - 1500) / 4)
            self.image.blit(self.Forms[9], (0, 0))
        elif 1650 <= self.count <= 1850:
            self.Forms[10].set_alpha((self.count - 1650))
            self.image.blit(self.Forms[10], (0, 0))
        elif 1900 <= self.count <= 2000:
            self.Forms[11].set_alpha((self.count - 1900)/3)
            self.image.blit(self.Forms[11], (0, 0))
        elif 2200 <= self.count <=2400:
            self.Forms[12].set_alpha((self.count - 2200)/3)
            self.image.blit(self.Forms[12], (0, 0))
        elif 2500 <= self.count < 2600:
            self.completeimage.set_alpha((self.count -2500)/2)
            self.image.blit(self.completeimage, (0, 0))
        elif self.count == 2600 and not self.complete:
            return self.Complete()
        if self.player.bigrect.colliderect(self.rect):
            self.count+= 5
        elif not self.complete:
            self.count = 0
            self.image.fill((0,0,0))
            self.image.blit(pygame.transform.scale_by(pygame.image.load('./Art/Interactables/Objectives/Objective Unactive.png').convert_alpha(), 5), (0,0))
    def Update(self):
        if self.count > 0:
            complete = self.Activate()
            if complete:
                return True
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
        self.points = 50
    def damage(self, damage, level):
        self.kill()
        level.UpdateChangables()
        level.player.XP += self.points
        level.HUD.UpdateScore(level.player)
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

class item(pygame.sprite.Sprite):
    def __init__(self, prioritycount):
        super(item, self).__init__()
        #image max size = 250, 250 relative
        self.description = ''
        self.price = 0
        self.name = ''
        self.prereq = None
        self.purchased = False
        self.prioritycount = prioritycount
        self.ammunitioncount = None
    def Buy(self, player):
        pass

class primaryWeapon(item):
    def __init__(self, range, damage, secondaryrange, secondaryangle, secondarydamage, prioritycount):
        super(primaryWeapon, self).__init__(prioritycount)
        self.range = range
        self.damage = damage
        self.secondaryCooldown = 0
        self.secondaryrange = secondaryrange
        self.secondaryangle = secondaryangle
        self.secondarydamage = secondarydamage

    def primaryAttack(self, angle, startpoint, damagables,size, level):
        hit = Functions.OverlapLine(self.range, angle, startpoint, damagables,size)
        for i in hit:
            i.damage(self.damage, level)
    def secondaryAttack(self, angle, startpoint, damagables, level):
        hit = Functions.sweepattack(self.secondaryrange, angle, self.secondaryangle, startpoint, damagables)
        for i in hit:
            i.damage(self.damage, level)

class secondaryWeapon(item):
    def __init__(self, range, damage, prioritycount):
        super(secondaryWeapon, self).__init__(prioritycount)
        self.range = range
        self.damage = damage
        self.Active = False
        self.ammunitioncount = 10
    def attack(self, angle, location, startpoint, damagables,size, level):
        hit = Functions.OverlapLine(self.range, angle, startpoint, damagables,size)
        for i in hit:
            i.damage(self.damage, level)
        self.Activate()
        self.ammunitionref.ammunitioncount -= 1
        level.HUD.UpdateSecondaryWeapon(level.player)
    def Activate(self):
        if self.ammunitionref.ammunitioncount != 0:
            if self.Active:
                self.image = self.regularimage
                self.Active = False
            else:
                self.image = self.ActiveImage
                self.Active = True
            return True
        else:
            return False
    def Buy(self, player, playernoexist = False):
        self.ammunitionref = ammunition()
        self.ammunitionref = self.ammunitionref.Buy(player, playernoexist)
class consumable(item):
    def __init__(self, prioritycount):
        super(consumable, self).__init__(prioritycount)
        self.ammunitioncount = 1
        self.Maxamount = 100000

class HealthPotion(consumable):
    def __init__(self):
        super(HealthPotion, self).__init__(10)
        self.healthhealed = 30
        self.cooldown = 100
        self.image = pygame.transform.scale(pygame.image.load('./Art/Items/Health Potion.png').convert_alpha(), (250,250))
        self.description = 'This Potion is the color of blood \n a label says\n drink me to regain 30 health'
        self.name = 'Potion'
        self.price = 200
        self.prereq = None
        self.Maxamount = 5
    def drink(self, player):
        if self.ammunitioncount >0:
            player.health += self.healthhealed
            player.currentlevel.HUD.heal()
            if player.health > 100:
                player.health =100
            self.ammunitioncount -= 1
    def Buy(self, player):
        if self.name not in [i.name for i in player.items]:
            player.items.append(self)
            player.equippedConsumable = self
        else:
            player.items[[i.name for i in player.items].index(self.name)].ammunitioncount +=1
class ammunition(consumable):
    def __init__(self):
        super(ammunition, self).__init__(1)
        self.healthhealed = 30
        self.cooldown = 100
        self.image = pygame.surface.Surface((250, 250))
        self.image.fill((216, 84, 84))
        self.description = 'These arrows are labled multiuse\n for any ranged weapon you can find \n EVEN A GUN?????'
        self.name = 'Arrows'
        self.price = 200
        self.prereq = Bow
        self.ammunitioncount = 10
        self.Maxamount = 25
    def Buy(self, player, playernoexist = False):
        if playernoexist:
            if self.name not in [i.name for i in player]:
                player.append(self)
                return self
            else:
                return player[[i.name for i in player].index(self.name)]
        else:
            if self.name not in [i.name for i in player.items]:
                player.items.append(self)
                return self
            else:
                player.items[[i.name for i in player.items].index(self.name)].ammunitioncount += 5
                return player.items[[i.name for i in player.items].index(self.name)]

class EnemyWeapon(primaryWeapon):
    def __init__(self, damage):
        super(EnemyWeapon, self).__init__(20, damage, 0, 0, 0, 0)
        self.image = pygame.surface.Surface((250, 250))
        # self.image = pygame.transform.scale(pygame.image.load('./Art/Items/Coin.png').convert_alpha(), ((ScreenLength / DEFAULT_IMAGE_SIZE[0] * 250, ScreenWidth / DEFAULT_IMAGE_SIZE[1] * 92)))
        self.image.fill((130, 24, 235))
        self.rect = self.image.get_rect()
        self.description = 'Null'
        self.name = 'enemyweapon'
        self.price = -1
        self.prereq = None
        self.secondaryCooldown = 0

class gun(primaryWeapon):
    def __init__(self):
        super(gun, self).__init__(50,10, 200, 100, 200, 100)
        self.image = pygame.surface.Surface((250, 250))
        #self.image = pygame.transform.scale(pygame.image.load('./Art/Items/Coin.png').convert_alpha(), ((ScreenLength / DEFAULT_IMAGE_SIZE[0] * 250, ScreenWidth / DEFAULT_IMAGE_SIZE[1] * 92)))
        self.image.fill((130,24,235))
        self.rect = self.image.get_rect()
        self.description = 'This is a basic "sword"... \n it acts as a gun....\n also it can kill everything :)'
        self.name = 'GUN'
        self.price = 50000
        self.prereq =None
        self.secondaryCooldown = 50

class basicSword(primaryWeapon):
    def __init__(self):
        super(basicSword, self).__init__(20,10, 20, 45, 5, 0)
        self.image = pygame.transform.scale(pygame.image.load('./Art/Items/Basic Sword.png').convert_alpha(), (250,250))
        self.rect = self.image.get_rect()
        self.description = 'This is a basic "sword"... \n its not very good...\n why am i writing this it will never be seen :('
        self.name = 'basic sword'
        self.price = 0
        self.prereq = None
        self.secondaryCooldown = 15

class LightSword(primaryWeapon):
    def __init__(self):
        super(LightSword, self).__init__(10,30, 10, 90, 45, 10)
        self.image = pygame.transform.scale(pygame.image.load('./Art/Items/Light Sword.png').convert_alpha(), (250,250))
        self.rect = self.image.get_rect()
        self.description = 'This is a sword made of light from the future \n it is very good... at a very short range\n so unfortunatly not that good'
        self.name = 'Light Sword'
        self.price = 5000
        self.prereq = None
        self.secondaryCooldown = 100

class FireSword(primaryWeapon):
    def __init__(self):
        super(FireSword, self).__init__(35,100, 35, 100, 75, 20)
        self.image = pygame.surface.Surface((250, 250))
        # self.image = pygame.transform.scale(pygame.image.load('./Art/Items/Coin.png').convert_alpha(), ((ScreenLength / DEFAULT_IMAGE_SIZE[0] * 250, ScreenWidth / DEFAULT_IMAGE_SIZE[1] * 92)))
        self.image.fill((15, 220, 235))
        self.rect = self.image.get_rect()
        self.description = 'The final form of the SWORD \n it will create massive damage in armys\n it also may light user on fire'
        self.name = 'Fire Sword'
        self.price = 20000
        self.prereq = LightSword
        self.secondaryCooldown = 50

class Bow(secondaryWeapon):
    def __init__(self):
        super(Bow, self).__init__(150, 15, 1)
        self.image = pygame.transform.scale(pygame.image.load('./Art/Items/Bow unstrung.png').convert_alpha(), (250,250))
        self.ActiveImage = pygame.transform.scale(pygame.image.load('./Art/Items/Bow Strung.png').convert_alpha(), (250,250))
        self.regularimage = self.image.copy()
        self.rect = self.image.get_rect()
        self.description = 'This bow was created by the gods... \n but in reality it is just a rotting wood stick \n with some string attached :)'
        self.name = 'Bow'
        self.price = 2000
        self.prereq = None
        self.size = (10,10)

    def attack(self, angle, location, startpoint, damagables, size,level):
        hit = Functions.overlapSpot(location, self.size, self.range, damagables, startpoint)
        print(hit)
        if hit != False:
            for i in hit:
                i.damage(self.damage, level)
            self.Activate()
            self.ammunitionref.ammunitioncount-=1
            level.HUD.UpdateSecondaryWeapon(level.player)
class Crossbow(secondaryWeapon):
    def __init__(self):
        super(Crossbow, self).__init__(100, 30, 2)
        self.image = pygame.surface.Surface((250, 250))
        self.image.fill((58, 27, 216))
        self.ActiveImage = self.image.copy()
        self.ActiveImage.fill((0, 94, 200))
        self.regularimage = self.image.copy()
        self.rect = self.image.get_rect()
        self.description = 'This is a crossbow.... \n in the past people believed that it was made \n when you combined a cross and a bow\n They were right... what are you thinking'
        self.name = 'Crossbow'
        self.price = 13000
        self.prereq = Bow



itemreference = {"GUN": gun, "Bow": Bow, 'basic sword': basicSword, 'Potion':HealthPotion, 'Arrows':ammunition, 'Crossbow':Crossbow, 'Light Sword':LightSword, 'Fire Sword':FireSword}

class Endpoint(pygame.sprite.Sprite):
    def __init__(self, location, room):
        super(Endpoint, self).__init__()
        self.image = pygame.image.load('./Art/Interactables/Exit_Portal.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (location[0]*5, location[1]*5))
        self.room = room
    def Interact(self, level):
        print('ENDPOINT REACHED')
        if level.objectivesRemaining <= 0:
            level.EndGame()

class Coin(pygame.sprite.Sprite):
    def __init__(self, location, value):
        super(Coin, self).__init__()
        self.image = pygame.transform.scale_by(pygame.image.load('./Art/Items/Coin.png').convert_alpha(), 1/2)
        self.rect = self.image.get_rect()
        self.rect.x = location[0]
        self.rect.y = location[1]
        self.smallrect = self.rect.copy()
        self.smallrect.width /=5
        self.smallrect.height /=5
        self.smallrect.x /= 5
        self.smallrect.y /=5
        self.monataryvalue = value
    def Update(self, player):
        if self.smallrect.colliderect(player.rect):
            self.kill()
            player.money += self.monataryvalue
            player.currentlevel.HUD.UpdateCoins()

class Player(pygame.sprite.Sprite):
    def __init__(self, name, seed, coins = 0, levelnum = 1, score = 0, items = None, health = 100):
        super(Player, self).__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill((210, 75, 222))
        self.tinyimage = pygame.Surface((5,5))
        self.tinyimage.fill((210,75,222))
        self.rect = self.tinyimage.get_rect()
        self.rect.x = 0 #startloc[0]
        self.rect.y = 0 #startloc[1]
        self.bigrect = self.image.get_rect()
        self.bigrect.x = self.rect.x *5
        self.bigrect.y = self.rect.y *5
        self.speed = 2
        self.obstruction = None
        self.primaryWeapon = None
        self.secondaryWeapon = None
        self.equippedConsumable = None
        self.equppedSpellbook = None

        self.currentlevel = None #level
        self.health = health
        self.armourlevel = 5

        self.AttackWithSecondary = False

        self.money = coins
        self.XP = score
        self.levelnum = levelnum
        self.name = name
        self.seed = seed

        if items == None:
            items = [basicSword()]
            self.primaryWeapon = items[0]
        else:
            for i in items:
                if issubclass(type(i), primaryWeapon):
                    if self.primaryWeapon:
                        if i.prioritycount > self.primaryWeapon.prioritycount:
                            self.primaryWeapon = i
                    else:
                        self.primaryWeapon = i
                elif issubclass(type(i), secondaryWeapon):
                    if self.secondaryWeapon:
                        if i.prioritycount > self.secondaryWeapon.prioritycount:
                            self.secondaryWeapon = i
                    else:
                        self.secondaryWeapon = i
                elif issubclass(type(i), consumable):
                    if type(i) != ammunition:
                        if self.equippedConsumable:
                            if i.prioritycount > self.equippedConsumable.prioritycount:
                                self.equippedConsumable = i
                        else:
                            self.equippedConsumable = i

        self.items = items
    def Inventory(self):
        pass
    def Interact(self, interactables, level):
        for i in interactables.sprites():
            if self.bigrect.colliderect(i):
                i.Interact(level)
    def Attack(self, angle, location, damagables, size):
        if self.AttackWithSecondary:
            print(location)
            self.secondaryWeapon.attack(angle, location, self.rect.center, damagables, size, self.currentlevel)
            self.AttackWithSecondary = False
        else:
            self.primaryWeapon.primaryAttack(angle, self.rect.center, damagables, size, self.currentlevel)
    def SecondaryAttack(self, angle, damagables):
        self.primaryWeapon.secondaryAttack(angle, self.rect.center, damagables, self.currentlevel)
    def damage(self, amount):
        print('hit')
        print(self.health)
        self.health -= amount
        if self.health <= 0:
            self.currentlevel.GameOver()
        self.currentlevel.HUD.damage(self)
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
        self.InRange = pygame.image.load('./Art/Mouse/Mouse InRange.png').convert_alpha()
        self.OutRange = pygame.image.load('./Art/Mouse/Mouse OutRange.png').convert_alpha()
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
