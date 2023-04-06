import pygame
from pygame import mixer
import math
from Procedural_Generator import ProceduralGenerator
from Classes import Player
import Classes


class game(object):
    def __init__(self):
        # sets up pygame and mixer


        pygame.init()
        mixer.init()

        # sets up temp background music
        mixer.music.load('Music/Character_Menu.mp3')
        mixer.music.play(-1)
        mixer.music.set_volume(0.10)


        self.ScreenLength= 1870
        self.ScreenWidth = 1030

        #sets up the generator class with tile size
        self.generator = ProceduralGenerator(int(self.ScreenLength / 10), int(self.ScreenWidth / 10), 50)

        # Set up the drawing window
        self.screen = pygame.display.set_mode([self.ScreenLength, self.ScreenWidth])
        self.StaticMap = pygame.Surface((self.ScreenLength, self.ScreenWidth))
        self.changeblesoverlay = pygame.Surface((self.ScreenLength, self.ScreenWidth))
        self.map = pygame.Surface((self.ScreenLength, self.ScreenWidth))

        pygame.display.set_caption('The Lost Dungeon')

        self.screen.fill((0, 0, 0))

        # hides mouse
        pygame.mouse.set_visible(False)

        # loads image
        self.direction_indicator = pygame.transform.scale_by(pygame.image.load("Art/Character/Direction-Temp.png"), 1 / 6).convert()
        self.direction_indicator.set_colorkey((255, 255, 255))
        self.direction_indicator_rect = self.direction_indicator.get_rect(center=(self.ScreenLength / 2, self.ScreenWidth / 2))

        self.damagables = None
        self.skipmousecheck = None
        self.angle = None
        self.updateScreen = None
        self.playerLocation = None
        self.maptriggered = None
        self.moveTime = None
        self.mapopen = None
        self.BIGmap = None
        self.BIGStaticMap = None
        self.mapsize = None
        self.cameraSpeed = None
        self.camera_Y = None
        self.camera_X = None
        self.running = None
        self.player = None
        self.obstructions = None
        self.newsize = None


        #init
        self.Generatelevel()
        self.SetupGame()
        self.Gameloop()
    def Generatelevel(self):
        # generates map
        self.generator.Generate(5, 10, 30, 5, True, 50, 10, 2, None, 1, 2, 5, 25)
        # inits player
        self.player = Player((self.generator.startloc[0][0], self.generator.startloc[0][1]), self)
        # draws map
        self.StaticMap, self.obstructions = self.generator.DrawMap(self.StaticMap)
        self.changeblesoverlay = self.generator.DrawChangebles(self.changeblesoverlay)
        self.map.blit(self.StaticMap, (0, 0))
        self.map.blit(self.changeblesoverlay, (0, 0))

    def SetupGame(self):
        self.running = True
        # sets up main verables
        self.camera_X = 0 - self.generator.startloc[0][0] * 5 + self.ScreenLength / 2 - 10
        self.camera_Y = 0 - self.generator.startloc[0][1] * 5 + self.ScreenWidth / 2 - 10
        self.cameraSpeed = .5
        self.mapsize = self.map.get_size()
        self.newsize = (self.mapsize[0] * 5, self.mapsize[1] * 5)
        self.BIGStaticMap = pygame.transform.scale(self.StaticMap, self.newsize)
        self.BIGmap = pygame.transform.scale(self.map, self.newsize)
        self.mapopen = False
        self.screen.blit(self.BIGmap, (self.camera_X, self.camera_Y))
        self.moveTime = 1
        self.maptriggered = False
        self.playerLocation = [self.generator.startloc[0][0], self.generator.startloc[0][1]]
        self.updateScreen = True
        self.angle = 0
        self.skipmousecheck = False
        self.damagables = pygame.sprite.Group()
        self.damagables.add(self.generator.jars.sprites())
    def Gameloop(self):
        while self.running:
            self.eventcheck()
            self.Movement()
            self.interactioncheck()
            self.update()

    def eventcheck(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # if key goes up
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_m:
                    self.maptriggered = False
                elif event.key == pygame.K_LSHIFT:
                    self.cameraSpeed = .5
            elif event.type == pygame.KEYDOWN:
                # if user presses M open map
                if event.key == pygame.K_m:
                    if self.mapopen and not self.maptriggered:
                        self.mapopen = False
                    elif not self.mapopen:
                        self.mapopen = True
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.player.Attack(self.angle, self.damagables, (self.ScreenLength, self.ScreenWidth))
                elif event.key == pygame.K_LSHIFT:
                    print('test')
                    self.cameraSpeed = 1



            # # if player moves the mouse calculate new angle for the direction indicator
            # elif event.type == pygame.MOUSEMOTION and not self.skipmousecheck:
            #     mouse_x, mouse_y = event.pos
            #     mouse_rel_x, mouse_rel_y = event.rel
            #     if abs(mouse_rel_x) > abs(mouse_rel_y):
            #         self.angle += math.ceil(mouse_rel_x / 5)
            #
            #     else:
            #         self.angle += math.ceil(mouse_rel_y / 5)
    def Movement(self):
        # gets all keys and does movment for the player.
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if not self.player.Checkcollisions(self.obstructions):
                self.camera_X += self.cameraSpeed * math.cos(math.radians(self.angle -45))
                self.camera_Y += self.cameraSpeed * math.sin(math.radians(self.angle -45))
                self.playerLocation[0] += self.cameraSpeed * math.cos(math.radians(self.angle - 225)) / 5
                self.playerLocation[1] += self.cameraSpeed * math.sin(math.radians(self.angle - 225)) / 5
            else:
                movement = self.player.MoveFromWall(self.cameraSpeed, self.camera_X, self.camera_Y, self.playerLocation)
                self.camera_X = movement[0]
                self.camera_Y = movement[1]
            # playerLocation = player.MoveLeft(moveTime, (ScreenLength,ScreenWidth))
            # moveTime +=1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if not self.player.Checkcollisions(self.obstructions):
                self.camera_X += self.cameraSpeed * math.cos(math.radians(self.angle + 135))
                self.camera_Y += self.cameraSpeed * math.sin(math.radians(self.angle + 135))
                self.playerLocation[0] += self.cameraSpeed * math.cos(math.radians(self.angle - 45)) / 5
                self.playerLocation[1] += self.cameraSpeed * math.sin(math.radians(self.angle - 45)) / 5
            else:
                movement = self.player.MoveFromWall(self.cameraSpeed, self.camera_X, self.camera_Y, self.playerLocation)
                self.camera_X = movement[0]
                self.camera_Y = movement[1]

            # playerLocation = player.MoveRight(moveTime, (ScreenLength, ScreenWidth))
            # moveTime += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            # if not self.player.Checkcollisions(self.obstructions):
            #     self.camera_Y += self.cameraSpeed
            #     self.playerLocation[1] -= self.cameraSpeed / 5
            # else:
            #     movement = self.player.MoveFromWall(self.cameraSpeed, self.camera_X, self.camera_Y, self.playerLocation)
            #     self.camera_X = movement[0]
            #     self.camera_Y = movement[1]

            # playerLocation = player.MoveUp(moveTime, (ScreenLength, ScreenWidth))
            # moveTime += 1
            if not self.player.Checkcollisions(self.obstructions):
                self.camera_X += self.cameraSpeed * math.cos(math.radians(self.angle+45))
                self.camera_Y += self.cameraSpeed * math.sin(math.radians(self.angle+45))
                self.playerLocation[0] += self.cameraSpeed * math.cos(math.radians(self.angle-135))/5
                self.playerLocation[1] += self.cameraSpeed * math.sin(math.radians(self.angle-135))/5
            else:
                movement = self.player.MoveFromWall(self.cameraSpeed, self.camera_X, self.camera_Y, self.playerLocation)
                self.camera_X = movement[0]
                self.camera_Y = movement[1]


        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if not self.player.Checkcollisions(self.obstructions):
                self.camera_X += self.cameraSpeed * math.cos(math.radians(self.angle + 225))
                self.camera_Y += self.cameraSpeed * math.sin(math.radians(self.angle + 225))
                self.playerLocation[0] += self.cameraSpeed * math.cos(math.radians(self.angle - 315)) / 5
                self.playerLocation[1] += self.cameraSpeed * math.sin(math.radians(self.angle - 315)) / 5
            else:
                self.movement = self.player.MoveFromWall(self.cameraSpeed, self.camera_X, self.camera_Y, self.playerLocation)
                self.camera_X = self.movement[0]
                self.camera_Y = self.movement[1]

            # playerLocation = player.MoveDown(moveTime, (ScreenLength, ScreenWidth))
            # moveTime += 1
            # print(moveTime)
            # print(playerLocation)
        if keys[pygame.K_q]:
            self.angle -=1
        if keys[pygame.K_e]:
            self.angle += 1
        if self.playerLocation == (self.ScreenLength / 2 - 25, self.ScreenWidth / 2 - 25):
            moveTime = 1
    def interactioncheck(self):
        for i in self.generator.enemys.sprites():
            i.CheckSpawn(self.playerLocation)

    def update(self):
        # rotates direction indicator based off angle
        direction_indicator_rotated = pygame.transform.rotate(self.direction_indicator, -self.angle)
        rect = direction_indicator_rotated.get_rect(center=self.direction_indicator_rect.center)

        # Fill the background with white
        self.screen.fill((0, 0, 0))
        # if map is closed draw game window to screen
        if not self.mapopen:
            self.screen.blit(self.BIGmap, (self.camera_X, self.camera_Y))
            self.screen.blit(self.player.image, (self.ScreenLength / 2 - 10, self.ScreenWidth / 2 - 10))
            self.screen.blit(direction_indicator_rotated, rect)

        # otherwise draw map
        else:
            self.screen.blit(self.map, (0, 0))
            self.screen.blit(self.player.tinyimage, self.playerLocation)

        # updates playerlocation
        self.player.rect.x = self.playerLocation[0]
        self.player.rect.y = self.playerLocation[1]
        # Flip the display
        pygame.display.flip()
        # if mouse leaves screen teleport it back to center
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x < 100 or mouse_x > self.ScreenLength - 100 or mouse_y < 100 or mouse_y > self.ScreenWidth - 100:
            skipmousecheck = True
            pygame.mouse.set_pos(self.ScreenLength / 2, self.ScreenWidth / 2)
        else:
            skipmousecheck = False
    def UpdateChangables(self):
        print('test')
        self.changeblesoverlay.fill((0,0,0))
        self.changeblesoverlay = self.generator.DrawChangebles(self.changeblesoverlay)
        BigChangablesoverlay = pygame.transform.scale(self.changeblesoverlay, self.newsize)
        self.BIGmap.fill((0,0,0))
        self.BIGmap.blit(self.BIGStaticMap, (0, 0))
        self.BIGmap.blit(BigChangablesoverlay, (0, 0))
        self.map.fill((0,0,0))
        self.map.blit(self.StaticMap, (0, 0))
        self.map.blit(self.changeblesoverlay, (0, 0))

gameinstance = game()








# Done! Time to quit.
pygame.quit()
