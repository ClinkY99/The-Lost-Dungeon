import pygame
import Functions
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class Enemy(pygame.sprite.Sprite):
    def __init__(self,health, speed, attackdamage, location):
        super(Enemy, self).__init__()
        self.speed=speed
        self.health=health
        self.attackdamage=attackdamage
        self.enemylocation = location
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

    def pathfinding(self, playerlocation):
        matrix = [
            [1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1]]

        # 1. create the grid with the nodes
        field = Grid(matrix=matrix)

        # 2. get start and end point

        start = field.node(3, 3)
        end = field.node(7, 3)

        # 3. create a finder with the movement style
        finder = AStarFinder()

        # 4. returns a list with the path and the amount of times the finder had to run to get the path
        path, runs = finder.find_path(start, end, grid)

        # 5. print result
        print(path)
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
class EnemySpawn():
    def __init__(self, NumberEnemys, Location):
        self.NumberEnemys= NumberEnemys
        self.Location = Location

    def Spawn(self):
        enemysspawned = pygame.sprite.Group()
        for i in range(self.NumberEnemys):
            enemysspawned.add(basicenemy(self.Location))
        return enemysspawned
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

class Jar(pygame.sprite.Sprite):
    def __init__(self,location):
        super(Jar, self).__init__()
        self.image = pygame.Surface((10,10))
        self.image.fill((66,245,233))
        self.rect = self.image.get_rect()
        self.rect.x = location[0]*10
        self.rect.y = location[1]*10
    def damage(self, damage, level):
        self.kill()
        level.UpdateChangables()


class wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super(wall, self).__init__()
        self.image = pygame.Surface((width,height))
        self.image.fill((127,127,127))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class enemy(pygame.sprite.Sprite):
    def __init__(self, ):
        pass

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
    def Sprint(self):
        pass
    def Checkcollisions(self, obstructions):
        for obstruction in obstructions.sprites():
            if self.rect.colliderect(obstruction):
                self.obstruction = obstruction
                return True
        return False
    def MoveFromWall(self, speed, camera_X, camera_Y, playerLocation):
        overlaprect = self.rect.clip(self.obstruction)

        if overlaprect.width > overlaprect.height:
            if playerLocation[1] < self.obstruction.rect.y:
                camera_Y += speed
                playerLocation[1] -= speed/5
            else:
                camera_Y -= speed
                playerLocation[1] += speed/5
        else:
            if playerLocation[0] < self.obstruction.rect.x:
                camera_X += speed
                playerLocation[0] -= speed/5
            else:
                camera_X -= speed
                playerLocation[0] += speed/5
        return [camera_X,camera_Y]

class enemymap():
    def __init__(self):

        enemies.draw(enemyoverlay)
        enemyoverlay.set_colorkey((0, 0, 0))
        enemiesoverlayBIG = pygame.transform.scale(enemyoverlay, newsize)