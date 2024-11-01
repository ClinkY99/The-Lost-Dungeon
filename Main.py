import sys

import pygame
from pygame import mixer
import math, os

import Functions
from Procedural_Generator import ProceduralGenerator
from Classes import Player
import Classes
from Shop import Shop
from PauseMenu import Pause_menu

import deathscreen, Endscreen

DEFAULT_IMAGE_SIZE = (1280, 720)

class HUD(pygame.sprite.Sprite):
    def __init__(self, ScreenLength, ScreenWidth, player, level):
        #sets up screen length variables and gets reference to player
        self.ScreenLength = ScreenLength
        self.ScreenWidth = ScreenWidth

        self.EnlargmentFactor = self.ScreenLength / DEFAULT_IMAGE_SIZE[0], self.ScreenWidth / DEFAULT_IMAGE_SIZE[1]
        self.player = player


        #sets up background image
        self.image = pygame.transform.scale(pygame.image.load('Art/HUD/HUD Background.png').convert_alpha(),
                                          (self.ScreenLength, self.ScreenWidth))
        self.image.set_alpha(200)

        self.rect = self.image.get_rect()

        #sets up item HUD
        self.Item = pygame.transform.scale(pygame.image.load('Art/HUD/Items HUD.png').convert_alpha(), (
        self.ScreenLength / DEFAULT_IMAGE_SIZE[0] * 250, self.ScreenWidth / DEFAULT_IMAGE_SIZE[1] * 250))
        self.ItemDisplay = self.Item.copy()
        self.ItemDisplayRect = self.ItemDisplay.get_rect(center=(
        self.ScreenLength - self.ItemDisplay.get_size()[0] / 2, self.ScreenWidth - self.ItemDisplay.get_size()[1] / 2))
        self.ItemDisplay.set_colorkey((255,255,255))

        self.KeybuttonOverlay = pygame.transform.scale(pygame.image.load('Art/HUD/KeyButtons Overlay.png').convert_alpha(), (
        self.ScreenLength / DEFAULT_IMAGE_SIZE[0] * 250, self.ScreenWidth / DEFAULT_IMAGE_SIZE[1] * 250))

        self.HUD = pygame.transform.scale(pygame.image.load('Art/HUD/HUD Background.png').convert_alpha(),
                                          (self.ScreenLength, self.ScreenWidth))


        #sets up main weapon display
        self.MainWeaponsDisplay = pygame.Surface(
            (self.ScreenLength / DEFAULT_IMAGE_SIZE[0] * 92, self.ScreenWidth / DEFAULT_IMAGE_SIZE[1] * 92))
        self.MainWeaponsDisplayRect = self.MainWeaponsDisplay.get_rect()
        self.MainWeaponsDisplayRect.x = 129 * self.ScreenLength / DEFAULT_IMAGE_SIZE[0]
        self.MainWeaponsDisplayRect.y = 129 * self.ScreenWidth / DEFAULT_IMAGE_SIZE[1]
        self.MainWeaponsDisplay.set_colorkey((255,255,255))
        if player.primaryWeapon != None:
            self.MainWeaponImage = pygame.transform.scale(player.primaryWeapon.image, self.MainWeaponsDisplay.get_size())

        #sets up blocking display
        self.BlockingDisplay = self.MainWeaponsDisplay.copy()
        self.BlockingDisplay.fill((70,70,70))
        self.BlockingDisplay.set_alpha(100)
        self.BlockingDisplayRect = self.MainWeaponsDisplayRect.copy()


        #sets up Secondary Weapon Display
        self.SecondaryWeaponsDisplay = pygame.Surface(
            (self.ScreenLength / DEFAULT_IMAGE_SIZE[0] * 69, self.ScreenWidth / DEFAULT_IMAGE_SIZE[1] * 69))
        self.SecondaryWeaponsDisplayRect = self.SecondaryWeaponsDisplay.get_rect()
        self.SecondaryWeaponsDisplayRect.x = 33 * self.ScreenLength / DEFAULT_IMAGE_SIZE[0]
        self.SecondaryWeaponsDisplayRect.y = 33 * self.ScreenWidth / DEFAULT_IMAGE_SIZE[1]
        self.SecondaryWeaponsDisplay.set_colorkey((255, 255, 255))
        if player.secondaryWeapon != None:
            self.SecondaryWeaponsImage = pygame.transform.scale(player.secondaryWeapon.image, self.SecondaryWeaponsDisplay.get_size())
            self.amunitioncount = Functions.get_font(int(10*self.EnlargmentFactor[0])).render(f'{player.secondaryWeapon.ammunitionref.ammunitioncount}', False, (254,255,255))

        #sets up consumable display
        self.ConsumablesDisplay = self.SecondaryWeaponsDisplay.copy()
        self.ConsumablesDisplayRect = self.SecondaryWeaponsDisplay.get_rect()
        self.ConsumablesDisplayRect.x = 13 * self.ScreenLength / DEFAULT_IMAGE_SIZE[0]
        self.ConsumablesDisplayRect.y = 153 * self.ScreenWidth / DEFAULT_IMAGE_SIZE[1]
        self.ConsumablesDisplay.set_colorkey((255, 255, 255))

        if player.equippedConsumable != None:
            self.ConsumablesImage = pygame.transform.scale(player.equippedConsumable.image, self.ConsumablesDisplay.get_size())
            self.ConsumableCount = Functions.get_font(int(10 * self.EnlargmentFactor[0])).render(
                f'{int(player.equippedConsumable.ammunitioncount)}', False, (254, 255, 255))


        #sets up magic display, not used
        self.MagicDisplay = self.SecondaryWeaponsDisplay.copy()
        self.MagicDisplayRect = self.SecondaryWeaponsDisplay.get_rect()
        self.MagicDisplayRect.x = 153 * self.ScreenLength / DEFAULT_IMAGE_SIZE[0]
        self.MagicDisplayRect.y = 13 * self.ScreenWidth / DEFAULT_IMAGE_SIZE[1]
        self.MagicDisplay.set_colorkey((255, 255, 255))

        if player.equppedSpellbook != None:
            self.MagicDisplayImage = pygame.transform.scale(player.equppedSpellbook.image, self.MagicDisplay.get_size())


        self.countPA = 0
        self.countSA = 0
        self.countSU = 0
        self.countCU = 0
        self.countSC = 0

        #sets up healthbar
        self.healthbarimage =  pygame.transform.scale(pygame.image.load('Art/HUD/Health bar Temp.png').convert_alpha(), (
        self.ScreenLength / DEFAULT_IMAGE_SIZE[0] * 200, self.ScreenWidth / DEFAULT_IMAGE_SIZE[1] * 40))
        self.healthbar = self.healthbarimage.copy()
        self.healthbar.set_colorkey((0,0,0))
        self.healthbarrect = self.healthbar.get_rect()
        self.healthbarrect.x = 25
        self.healthbarrect.y = 25

        self.healthbarlevel = pygame.Surface((
        self.ScreenLength / DEFAULT_IMAGE_SIZE[0] * (200/5)*4, self.ScreenWidth / DEFAULT_IMAGE_SIZE[1] * (28/5)*4))
        self.healthbarlevelrect = self.healthbarlevel.get_rect()
        self.healthbarlevelrect.x = (39/5) * 4 *self.ScreenLength / DEFAULT_IMAGE_SIZE[0]
        self.healthbarlevelrect.y = self.ScreenWidth / DEFAULT_IMAGE_SIZE[1] * (12/5) * 4
        self.healthbarlevel.set_colorkey((0,0,0))

        self.healthIndicator = self.healthbarlevel.copy()
        self.healthIndicator.fill((211, 28, 28))

        self.healthbarlevel.blit(self.healthIndicator, (((player.health - 100) / 5) * 8 * self.ScreenLength / DEFAULT_IMAGE_SIZE[0], 0))

        self.healthbar.fill((0, 0, 0))
        self.healthbar.blit(self.healthbarlevel, self.healthbarlevelrect)
        self.healthbar.blit(self.healthbarimage, (0, 0))

        self.damaged = -1
        self.health = -1

        #sets up hud information, Coins, Score, Level, And objectives
        self.Coins = Functions.get_font(int(self.EnlargmentFactor[0]*25)).render(f'{player.money}', False, (255,239,0))
        self.Coinsimage = pygame.transform.scale_by(pygame.image.load('./Art/Items/Money_Bag.png').convert_alpha(), self.EnlargmentFactor[0])

        self.level = Functions.get_font(int(self.EnlargmentFactor[0]*25)).render(f'Level {player.levelnum}', False, (255,255,255))

        self.Score = Functions.get_font(int(self.EnlargmentFactor[0]*25)).render(f'Score:{player.XP}', False, (255,255,255))

        self.ObjectivesRemaining = Functions.get_font(int(self.EnlargmentFactor[0]*25)).render(f'Objectives Remaining: {level.objectivesRemaining}', True, (0,166,60))

        self.ObjectivesRemainingRect = self.ObjectivesRemaining.get_rect(center= (ScreenLength/2, 25))
        self.ObjectivesRemainingRect = self.ObjectivesRemaining.get_rect(center=(ScreenLength / 2, 25))

    def Update(self,player):
        #clears screen
        self.image.fill((1,1,1))

        self.ItemDisplay.fill((255,255,255))

        #blits items to the item display
        self.ItemDisplay.blit(self.Item, (0,0))

        self.MainWeaponsDisplay.fill((255, 255, 255))
        self.SecondaryWeaponsDisplay.fill((255, 255, 255))
        self.ConsumablesDisplay.fill((255, 255, 255))
        self.MagicDisplay.fill((255, 255, 255))


        #does animation logic for all items
        if self.countPA > 0:
            self.PrimaryAttack(player)
        elif player.primaryWeapon != None:
            self.MainWeaponsDisplay.blit(self.MainWeaponImage, (0,0))
        if self.countSA > 0:
            self.SecondaryAttack(player)
        if player.secondaryWeapon != None:
            self.SecondaryWeaponsDisplay.blit(self.SecondaryWeaponsImage, (0,0))
            self.SecondaryWeaponsDisplay.blit(self.amunitioncount, (self.SecondaryWeaponsDisplay.get_size()[0]-self.amunitioncount.get_size()[0], self.SecondaryWeaponsDisplay.get_size()[1]-self.amunitioncount.get_size()[1]))
        if self.countCU >0:
            self.ConsumableUsed(player)
        elif player.equippedConsumable != None:
            self.ConsumablesDisplay.blit(self.ConsumablesImage, (0,0))
            self.ConsumablesDisplay.blit(self.ConsumableCount, (
            self.ConsumablesDisplay.get_size()[0] - self.ConsumableCount.get_size()[0],
            self.ConsumablesDisplay.get_size()[1] - self.ConsumableCount.get_size()[1]))
        if self.countSC > 0:
            self.SpellCast(player)
        elif player.equppedSpellbook != None:
            self.MagicDisplay.blit(self.MagicDisplayImage, (0,0))

        #does health bar logic, stops health bar from refreshing unless it is needed
        if self.damaged > 0:
            self.healthbar.fill((0, 0, 0))
            self.healthbarlevel.fill((0, 0, 0))
            self.healthIndicator.fill((255, 255, 255))
            self.damaged-=1
            self.healthbarlevel.blit(self.healthIndicator,
                                     (((player.health - 100) / 5) * 8 * self.ScreenLength / DEFAULT_IMAGE_SIZE[0], 0))
            self.healthbar.blit(self.healthbarlevel, self.healthbarlevelrect)
            self.healthbar.blit(self.healthbarimage, (0, 0))
        elif self.damaged == 0:
            self.healthbar.fill((0, 0, 0))
            self.healthbarlevel.fill((0, 0, 0))
            self.healthIndicator.fill((211,28,28))
            self.damaged-=1
            self.healthbarlevel.blit(self.healthIndicator,
                                     (((player.health - 100) / 5) * 8 * self.ScreenLength / DEFAULT_IMAGE_SIZE[0], 0))
            self.healthbar.blit(self.healthbarlevel, self.healthbarlevelrect)
            self.healthbar.blit(self.healthbarimage, (0, 0))
        if self.health > 0:
            self.healthbar.fill((0, 0, 0))
            self.healthbarlevel.fill((0, 0, 0))
            self.healthIndicator.fill((32, 148, 51))
            self.health-=1
            self.healthbarlevel.blit(self.healthIndicator,
                                     (((player.health - 100) / 5) * 8 * self.ScreenLength / DEFAULT_IMAGE_SIZE[0], 0))
            self.healthbar.blit(self.healthbarlevel, self.healthbarlevelrect)
            self.healthbar.blit(self.healthbarimage, (0, 0))
        elif self.health == 0:
            self.healthbar.fill((0, 0, 0))
            self.healthbarlevel.fill((0, 0, 0))
            self.healthIndicator.fill((211,28,28))
            self.health-=1
            self.healthbarlevel.blit(self.healthIndicator,
                                     (((player.health - 100) / 5) * 8 * self.ScreenLength / DEFAULT_IMAGE_SIZE[0], 0))
            self.healthbar.blit(self.healthbarlevel, self.healthbarlevelrect)
            self.healthbar.blit(self.healthbarimage, (0, 0))


        #blits everything to screen
        self.ItemDisplay.blit(self.MainWeaponsDisplay, self.MainWeaponsDisplayRect)
        self.ItemDisplay.blit(self.SecondaryWeaponsDisplay, self.SecondaryWeaponsDisplayRect)
        self.ItemDisplay.blit(self.ConsumablesDisplay, self.ConsumablesDisplayRect)
        self.ItemDisplay.blit(self.MagicDisplay, self.MagicDisplayRect)
        self.ItemDisplay.blit(self.KeybuttonOverlay, (0,0))

        self.image.blit(self.HUD, (0,0))
        self.image.blit(self.healthbar, self.healthbarrect)
        self.image.blit(self.Coins, (15, self.healthbarrect.height+50))
        self.image.blit(self.Coinsimage, (15 + self.Coins.get_size()[0],self.healthbarrect.height+30 ))
        self.image.blit(self.level, (15, self.healthbarrect.height + self.Coins.get_size()[1]+75))
        self.image.blit(self.Score, (15, self.healthbarrect.height + self.Coins.get_size()[1] + self.level.get_size()[1] + 100))
        self.image.blit(self.ObjectivesRemaining, self.ObjectivesRemainingRect)
        self.image.blit(self.ItemDisplay, self.ItemDisplayRect)
        self.image.set_colorkey((1,1,1))
        self.healthIndicator.fill((211,28,28))


    def PrimaryAttack(self, player):
        #makes weapon pulse when attack
        weapon = self.MainWeaponImage.copy()
        weapon = pygame.transform.scale_by(weapon, ((-1/2)*((1/4)*self.countPA -1)**2 +1.5))
        rect = weapon.get_rect(center= (self.MainWeaponsDisplay.get_size()[0]/2, self.MainWeaponsDisplay.get_size()[1]/2))
        self.MainWeaponsDisplay.blit(weapon, rect)
        self.countPA += 1
        if self.countPA >= 8:
            self.countPA = 0

    def SecondaryAttack(self,player):
        #makes cooldown for secondary attack
        self.MainWeaponsDisplay.blit(self.BlockingDisplay,(0, self.BlockingDisplay.get_size()[1]*(self.countSA/player.primaryWeapon.secondaryCooldown)))
        self.countSA+=1
        if self.countSA >= player.primaryWeapon.secondaryCooldown:
            self.countSA = 0
    def damage(self, player):
        #sets up damaged animation
        self.damaged = 2
    def heal(self):
        #sets up health animation
        self.health = 7

    def UpdateCoins(self):
        #updates coind
        self.Coins = Functions.get_font(int(self.EnlargmentFactor[0] * 25)).render(f'{self.player.money}', False,
                                                                                   (255,239,0))
    def UpdateScore(self,player):
        #updates score
        self.Score = Functions.get_font(int(self.EnlargmentFactor[0]*25)).render(f'Score:{player.XP}', False, (255,255,255))
    def UpdateObjectiveCount(self, level):
        #updates objectives infor
        if level.objectivesRemaining > 0:
            self.ObjectivesRemaining = Functions.get_font(int(self.EnlargmentFactor[0] * 25)).render(
                f'Objectives Remaining: {level.objectivesRemaining}', True, (0, 166, 60))
        else:
            self.ObjectivesRemaining = Functions.get_font(int(self.EnlargmentFactor[0] * 25)).render(
                f'Find The Exit', True, (0, 166, 60))
        self.ObjectivesRemainingRect = self.ObjectivesRemaining.get_rect(center=(self.ScreenLength / 2, 25))
    def UpdateSecondaryWeapon(self, player):
        #updates secondary weapon image
        if player.secondaryWeapon != None:
            self.SecondaryWeaponsImage = pygame.transform.scale(player.secondaryWeapon.image,
                                                                self.SecondaryWeaponsDisplay.get_size())
            self.amunitioncount = Functions.get_font(int(10*self.EnlargmentFactor[0])).render(f'{player.secondaryWeapon.ammunitionref.ammunitioncount}', False, (254,255,255))
    def UpdateConsumable(self, player):
        #sets up Consumable image
        if player.equippedConsumable != None:
            self.ConsumablesImage = pygame.transform.scale(player.equippedConsumable.image, self.ConsumablesDisplay.get_size())
            self.ConsumableCount = Functions.get_font(int(10 * self.EnlargmentFactor[0])).render(
                f'{int(player.equippedConsumable.ammunitioncount)}', False, (254, 255, 255))







class game(object):
    def __init__(self, tutorial, player, levelnum, seed, screen, screensize):
        # sets up pygame and mixer


        pygame.init()
        mixer.init()

        # sets up temp background music
        mixer.music.load('Music/Game_Theme1.mp3')
        mixer.music.play(-1)
        mixer.music.set_volume(0.10)

        print(player)

        self.player = player
        self.player.currentlevel = self

        self.tutorial = tutorial
        self.levelnum = levelnum

        self.ScreenLength= screensize[0]
        self.ScreenWidth = screensize[1]

        #sets up the generator class with tile size
        self.generator = ProceduralGenerator(2*levelnum+75,2*levelnum+75, seed+levelnum)

        # Set up the drawing window
        self.screen = screen
        self.StaticMap = pygame.Surface((self.ScreenLength, self.ScreenWidth))
        self.changeblesoverlay = pygame.Surface((self.ScreenLength*5, self.ScreenWidth*5))
        self.enemysOverlay = pygame.Surface((self.ScreenLength*5, self.ScreenWidth*5))
        self.map = pygame.Surface((self.ScreenLength, self.ScreenWidth))
        self.mouse = Classes.Mouse()
        self.itemOverlay = self.enemysOverlay.copy()





        self.items = pygame.sprite.Group()

        self.enemys = pygame.sprite.Group()


        pygame.display.set_caption('The Lost Dungeon')

        self.screen.fill((0, 0, 0))

        # hides mouse
        pygame.mouse.set_visible(False)

        # loads image
        self.direction_indicator = pygame.transform.scale_by(pygame.image.load("Art/Character/Direction-Temp.png").convert_alpha(), 1 / 6).convert()
        self.direction_indicator.set_colorkey((255, 255, 255))
        self.direction_indicator_rect = self.direction_indicator.get_rect(center=(self.ScreenLength / 2, self.ScreenWidth / 2))

        self.clock = pygame.time.Clock()

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
        self.obstructions = None
        self.newsize = None
        self.smallchangeblesoverlay = None
        self.matrix = None
        self.objectivesRemaining = None
        self.interactables = pygame.sprite.Group()
        self.Objectives = pygame.sprite.Group()
        self.paused = False

        self.Tutorialcount = 0
        self.tutorialimages = []
        self.tutorialscreen = None

        if tutorial:
            self.Tutorial()

        #init
        self.Generatelevel()
        self.SetupGame()
        self.Gameloop()

    def Generatelevel(self):
        # generates map
        self.generator.Generate(math.ceil((1/2)*self.levelnum+3), 8 ,math.ceil((1/6)*self.levelnum+15) , 5, True, 25, 10, math.ceil((1/5) * self.levelnum+2), None, math.ceil(self.levelnum/2), math.ceil(self.levelnum/5), 5, math.ceil(self.levelnum/2)+5)
        self.matrix = self.generator.matrix
        # inits player
        self.player.rect.x = self.generator.startloc[0][0]
        self.player.rect.y = self.generator.startloc[0][1]


        # draws map
        self.StaticMap, self.obstructions = self.generator.DrawMap(self.StaticMap)
        self.changeblesoverlay = self.generator.DrawChangebles(self.changeblesoverlay)
        self.smallchangeblesoverlay = pygame.transform.scale_by(self.changeblesoverlay, 1/5)
        self.map.blit(self.StaticMap, (0, 0))
        self.map.blit(self.smallchangeblesoverlay, (0,0))

    def SetupGame(self):
        self.running = True
        # sets up main verables
        self.camera_X = 0 - self.generator.startloc[0][0] * 5 + self.ScreenLength / 2 - 10
        self.camera_Y = 0 - self.generator.startloc[0][1] * 5 + self.ScreenWidth / 2 - 10
        self.cameraSpeed = 1.5
        self.mapsize = self.map.get_size()
        self.newsize = (self.mapsize[0] * 5, self.mapsize[1] * 5)
        self.BIGStaticMap = pygame.transform.scale(self.StaticMap, self.newsize)
        start = pygame.image.load('./Art/Interactables/Entrance_Portal.png').convert_alpha()
        startrect = start.get_rect(center= (self.generator.startloc[0][0]*5, self.generator.startloc[0][1]*5))
        self.BIGStaticMap.blit(start, startrect)
        self.BIGStaticMap.blit(self.generator.endpoint.image, self.generator.endpoint.rect)
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
        self.interactables.add(self.generator.Treasure.sprites(), self.generator.Objectives.sprites(), self.generator.endpoint)
        self.Objectives.add(self.generator.Objectives.sprites())
        self.objectivesRemaining = self.generator.Objectivesnum
        self.HUD = HUD(self.ScreenLength, self.ScreenWidth, self.player, self)
    def Gameloop(self):
        #Ticks the clock to get fps to set up walking speed
        self.clock.tick(120)
        try:
            self.cameraSpeed = 30 / self.clock.get_fps() * 1.5
        except:
            self.cameraSpeed = 1.5
        while self.running:
            #runs event checks unless the game is paused
            self.eventcheck()
            if not self.paused:
                self.Movement()
                self.interactioncheck()
                self.UpdateHostiles()
                self.UpdateItems()
                self.HUD.Update(self.player)
            self.update()
            self.clock.tick(120)
            #print(self.clock.get_fps())

    def eventcheck(self):
        #gets mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        #handles keybinds and alt f4ing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            # if key goes up
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_m:
                    self.maptriggered = False
                elif event.key == pygame.K_LSHIFT:
                    try:
                        self.cameraSpeed = 30 / self.clock.get_fps() * 1.5
                    except:
                        self.cameraSpeed = 1.5
            elif event.type == pygame.KEYDOWN:
                # if user presses M open map
                if event.key == pygame.K_f:
                    print(self.objectivesRemaining)
                    self.player.Interact(self.interactables, self)
                elif event.key == pygame.K_LSHIFT:
                    try:
                        self.cameraSpeed = 30 / self.clock.get_fps() * 3
                    except:
                        self.cameraSpeed = 3
                    if self.Tutorialcount == 1:
                        self.Tutorial()
                elif event.key == pygame.K_ESCAPE:
                    Pause_menu(self.screen, self.screen.get_size(), self.player)
                elif event.key == pygame.K_e:
                    if self.player.secondaryWeapon:
                        if self.player.secondaryWeapon.Activate():
                            self.player.AttackWithSecondary = self.player.secondaryWeapon.Active
                            self.HUD.UpdateSecondaryWeapon(self.player)
                elif event.key == pygame.K_q:
                    if self.player.equippedConsumable:
                        self.player.equippedConsumable.drink(self.player)
                        self.HUD.UpdateConsumable(self.player)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.player.Attack(self.angle, (self.playerLocation[0]+(mouse_x-self.ScreenLength/2)/5, self.playerLocation[1]+(mouse_y-self.ScreenWidth/2)/5) ,self.damagables, (self.ScreenLength, self.ScreenWidth))
                    if self.Tutorialcount == 2:
                        self.Tutorial()
                    self.HUD.countPA += 1
                if event.button == 3 and self.HUD.countSA == 0:
                    self.player.SecondaryAttack(self.angle, self.damagables)
                    self.HUD.countSA +=1

            self.angle = math.degrees(math.atan2((mouse_y - self.ScreenWidth / 2), (mouse_x - self.ScreenLength / 2))) +135

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
        #move left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if not self.player.Checkcollisions(self.obstructions):
                self.camera_X += self.cameraSpeed
                self.playerLocation[0] -= self.cameraSpeed/5
            else:
                movement = self.player.MoveFromWall(self.cameraSpeed, self.camera_X, self.camera_Y, self.playerLocation)
                self.camera_X = movement[0]
                self.camera_Y = movement[1]
            # playerLocation = player.MoveLeft(moveTime, (ScreenLength,ScreenWidth))
            # moveTime +=1
        #move right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if not self.player.Checkcollisions(self.obstructions):
                self.camera_X -= self.cameraSpeed
                self.playerLocation[0] += self.cameraSpeed/5
            else:
                movement = self.player.MoveFromWall(self.cameraSpeed, self.camera_X, self.camera_Y, self.playerLocation)
                self.camera_X = movement[0]
                self.camera_Y = movement[1]

            # playerLocation = player.MoveRight(moveTime, (ScreenLength, ScreenWidth))
            # moveTime += 1
        #move up
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            # playerLocation = player.MoveUp(moveTime, (ScreenLength, ScreenWidth))
            # moveTime += 1
            if not self.player.Checkcollisions(self.obstructions):
                self.camera_Y += self.cameraSpeed
                self.playerLocation[1] -= self.cameraSpeed/5
            else:
                movement = self.player.MoveFromWall(self.cameraSpeed, self.camera_X, self.camera_Y, self.playerLocation)
                self.camera_X = movement[0]
                self.camera_Y = movement[1]

        #move down
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if not self.player.Checkcollisions(self.obstructions):
                self.camera_Y -= self.cameraSpeed
                self.playerLocation[1] += self.cameraSpeed/5
            else:
                self.movement = self.player.MoveFromWall(self.cameraSpeed, self.camera_X, self.camera_Y, self.playerLocation)
                self.camera_X = self.movement[0]
                self.camera_Y = self.movement[1]

            # playerLocation = player.MoveDown(moveTime, (ScreenLength, ScreenWidth))
            # moveTime += 1
            # print(moveTime)
            # print(playerLocation)
        if self.playerLocation == (self.ScreenLength / 2 - 25, self.ScreenWidth / 2 - 25):
            moveTime = 1
    def interactioncheck(self):
        #checks for interactions, runs enemys script, updates objectives
        for i in self.generator.enemys.sprites():
            enemys = i.CheckSpawn(self.playerLocation, math.ceil(self.levelnum/2))
            if enemys:
                self.enemys.add(enemys)
                self.damagables.add(self.enemys)
        for i in self.Objectives.sprites():
            if i.Interact(self):

                self.objectivesRemaining -= 1
                if self.Tutorialcount == 3:
                    self.Tutorial()
                self.HUD.UpdateObjectiveCount(self)


    def UpdateHostiles(self):
        #updates enemies pathfinding
        for i in self.enemys.sprites():
            i.Update(self.playerLocation, self.obstructions, self.player)
        self.enemysOverlay.fill((0,0,0))
        self.enemys.draw(self.enemysOverlay)
        self.enemysOverlay.set_colorkey((0,0,0))
    def UpdateItems(self):
        #updates dropped items
        for i in self.items.sprites():
            i.Update(self.player)
        self.itemOverlay.fill((0,0,0))
        self.items.draw(self.itemOverlay)
        self.itemOverlay.set_colorkey((0,0,0))
    def update(self):
        # rotates direction indicator based off angle
        self.player.update(self.angle)

        # Fill the background with white
        self.screen.fill((0, 0, 0))
        # if map is closed draw game window to screen
        self.Objectives.draw(self.changeblesoverlay)


        self.screen.blit(self.BIGStaticMap, (self.camera_X, self.camera_Y))
        self.screen.blit(self.changeblesoverlay, (self.camera_X, self.camera_Y))
        self.screen.blit(self.enemysOverlay, (self.camera_X, self.camera_Y))
        self.screen.blit(self.itemOverlay, (self.camera_X, self.camera_Y))
        self.screen.blit(self.player.image, (self.ScreenLength / 2 - 10, self.ScreenWidth / 2 - 10))

        if self.player.AttackWithSecondary:
            self.mouse.Update(self.player.secondaryWeapon.range, (self.ScreenLength / 2, self.ScreenWidth / 2))
        else:
            self.mouse.Update(self.player.primaryWeapon.range,(self.ScreenLength / 2, self.ScreenWidth / 2))
        self.screen.blit(self.mouse.image, self.mouse.rect)
        self.screen.blit(self.HUD.image, (0,0))
        if self.tutorialscreen:
            self.screen.blit(self.tutorialscreen, (self.ScreenLength-self.tutorialscreen.get_size()[0], self.ScreenWidth/20))

        # updates playerlocation
        self.player.rect.x = self.playerLocation[0]
        self.player.rect.y = self.playerLocation[1]
        self.player.bigrect.x = self.playerLocation[0]*5
        self.player.bigrect.y = self.playerLocation[1]*5

        # Flip the display
        pygame.display.flip()
    def UpdateChangables(self):
        print('test')
        #updates changables screen(jars)
        self.changeblesoverlay.fill((0,0,0))
        self.changeblesoverlay = self.generator.DrawChangebles(self.changeblesoverlay)
        BigChangablesoverlay = pygame.transform.scale(self.changeblesoverlay, self.newsize)
        self.BIGmap.fill((0,0,0))
        self.BIGmap.blit(self.BIGStaticMap, (0, 0))
        self.BIGmap.blit(BigChangablesoverlay, (0, 0))
        self.map.fill((0,0,0))
        self.map.blit(self.StaticMap, (0, 0))
        self.map.blit(self.changeblesoverlay, (0, 0))

    def EndGame(self):
        # print('complete')
        # pygame.quit()
        # sys.exit(-1)
        #Ends Game
        if self.Tutorialcount == 4:
            self.Tutorial()
        Functions.FTB(self.screen, 200)
        #continues to end screen
        Endscreen.end_screen(self.screen,self.screen.get_size(), (self.ScreenLength/DEFAULT_IMAGE_SIZE[0], self.ScreenWidth/DEFAULT_IMAGE_SIZE[1]), self.player)

    def GameOver(self):
        print('Game Over')
        #continues to death screen
        deathscreen.Death_screen(self.screen,self.screen.get_size(), (self.ScreenLength/DEFAULT_IMAGE_SIZE[0], self.ScreenWidth/DEFAULT_IMAGE_SIZE[1]), self.player)

    def Tutorial(self):
        #sets up tutorial
        if self.Tutorialcount == 0:
            for file in os.listdir('./Art/Tutorial'):
                filename = os.fsdecode(file)
                self.tutorialimages.append(pygame.transform.scale_by(pygame.image.load((os.path.join('./Art/Tutorial', filename))).convert_alpha(),self.ScreenLength/DEFAULT_IMAGE_SIZE[0]*1.25))
            self.tutorialscreen = self.tutorialimages[self.Tutorialcount]
        elif self.Tutorialcount == 4:
            #ends tutorial
            self.tutorialscreen = None
        else:
            #sets up the new tutorial image
            self.tutorialscreen = self.tutorialimages[self.Tutorialcount]
        self.Tutorialcount+=1







# Done! Time to quit.
pygame.quit()
