import pygame, sys
from pygame import mixer

import Main
from Interactables import Button, ImageButton
import Functions, Classes
import mainmenu

DEFAULT_IMAGE_SIZE = (1280, 720)

#screen = pygame.display.set_mode((1920,1080), pygame.FULLSCREEN)
class Shop(object):
    def __init__(self, player, screen, size):
        pygame.init()
        mixer.init()

        mixer.music.load('Music/game_thingie_shop.mp3')
        mixer.music.play(-1)
        mixer.music.set_volume(0.90)

        self.ScreenLength = size[0]
        self.ScreenWidth = size[1]

        self.enlargmentfactor = self.ScreenLength/DEFAULT_IMAGE_SIZE[0], self.ScreenWidth/DEFAULT_IMAGE_SIZE[1]

        self.screen = screen

        self.player = player

        self.shopopen = True
        pygame.mouse.set_visible(True)

        self.items = [Classes.gun(), Classes.Bow(), Classes.Crossbow(), Classes.FireSword(), Classes.LightSword(), Classes.LeatherArmour(), Classes.PlateArmour(), Classes.FrostWelmArmour()]

        self.onsale = []

        self.consumables = [Classes.HealthPotion(), Classes.ammunition()]

        self.onsaleconsumables = []

        self.currentindex = 0
        self.SelectedItem = None

        self.background = pygame.Surface((self.ScreenLength, self.ScreenWidth))
        self.background.fill((175, 175, 175))
        self.BuyablesArea = pygame.Surface((self.ScreenLength, self.ScreenWidth/2))
        self.BuyablesArea.fill((77,77,77))
        self.Itemdisplay = pygame.Surface((400, self.ScreenWidth//2.5))
        self.Itemdisplay.fill((142,142,142))
        self.obscuringLayer = pygame.Surface((400, self.ScreenWidth//2.5))
        self.obscuringLayer.fill((75,75,75))
        self.obscuringLayer.set_alpha(75)
        self.Description = pygame.Surface((self.ScreenLength/2, self.ScreenWidth/5))
        Rect = pygame.Rect((0,0), self.Description.get_size())
        Rect.center = (self.Description.get_size()[0]/2, self.Description.get_size()[1]/2)
        pygame.draw.rect(self.Description, (107,107,107),Rect, border_radius=25)
        self.Description.set_colorkey((0,0,0))
        self.PurchasedScreen = pygame.transform.scale(pygame.image.load('./Art/Shop/Sold Screen.png').convert_alpha(), (400, self.ScreenWidth//2.5))

        self.coin = pygame.image.load('Art/Items/Coin.png').convert_alpha()

        self.imagedrawrect = pygame.rect.Rect(0,0,260,260)
        self.imagedrawrect.center = (self.Itemdisplay.get_size()[0]//2, self.Itemdisplay.get_size()[1]//2-25)

        self.Itemdisplay.blit(self.coin, (350, self.Itemdisplay.get_size()[1]-50))

        pygame.draw.rect(self.Itemdisplay, (94,94,94),self.imagedrawrect , 1)


        self.MENUtext = Functions.get_font(100).render("Shop", True, "#b68f40")
        self.MENUrect = self.MENUtext.get_rect(center=(self.ScreenLength/2, 100))


        self.walletImage = pygame.transform.scale_by(pygame.image.load('./Art/Items/Money_Bag.png').convert_alpha(), self.enlargmentfactor[0])
        self.walletImagerect = self.walletImage.get_rect(topright = (self.ScreenLength-50, 160))
        self.wallet = Functions.get_font(50).render(f'{self.player.money}', True, (255,239,0))
        self.walletRect = self.wallet.get_rect(center= (self.ScreenLength-self.wallet.get_size()[0], 200))


        self.PurchaseButton = Button(image=pygame.image.load("assets/Play Rect.png").set_alpha(0), pos=(self.ScreenLength-200, self.ScreenWidth-75),
                        text_input="Purchase", font=Functions.get_font(40), base_color="#d7fcd4", hovering_color="White", sound= './SFX/Shop/purchase.mp3')
        self.ExitToMenuButton = Button(image=pygame.image.load("assets/Quit Rect.png").set_alpha(0), pos=(275, 50),
                        text_input="Exit to Menu", font=Functions.get_font(40), base_color="#d7fcd4", hovering_color="White")
        self.ContinueButton = Button(image=pygame.image.load("assets/Play Rect.png").set_alpha(0), pos=(self.ScreenLength-200, 50),
                            text_input="Continue", font=Functions.get_font(40), base_color="#d7fcd4", hovering_color="White")

        self.LeftButton = ImageButton(image=pygame.image.load('Art/Shop/Arrow.png'), Hoverimage= pygame.image.load('Art/Shop/Hover Arrow.png'),
                                      pos=(100, self.ScreenWidth/4*2))

        self.RightButton = ImageButton(image=pygame.transform.rotate(pygame.image.load('Art/Shop/Arrow.png'),180), Hoverimage= pygame.transform.rotate(pygame.image.load('Art/Shop/Hover Arrow.png'),180),
                                      pos=(self.ScreenLength-100, self.ScreenWidth/4*2-20))

        self.EquippablesButton = ImageButton(
            image=pygame.transform.scale_by(pygame.image.load('./Art/Shop/Equipment_unclicked.png').convert_alpha(),
                                            self.enlargmentfactor[0]),
            Hoverimage=pygame.transform.scale_by(pygame.image.load('./Art/Shop/Equipment_clicked.png').convert_alpha(),
                                                 self.enlargmentfactor[0]),
            pos=(100 * self.enlargmentfactor[0], 200 * self.enlargmentfactor[1]), stayclicked=True)
        self.ConsumablesButton = ImageButton(image=pygame.transform.scale_by(pygame.image.load('./Art/Shop/Consumables_unclicked.png').convert_alpha(), self.enlargmentfactor[0]), Hoverimage= pygame.transform.scale_by(pygame.image.load('./Art/Shop/Consumables_clicked.png').convert_alpha(),self.enlargmentfactor[0]),
                                      pos=(125*self.enlargmentfactor[0] + self.EquippablesButton.image.get_size()[0], 200*self.enlargmentfactor[1]), stayclicked= True)

        self.EquippablesButton.clicked = True
        self.EquippablesButton.image = self.EquippablesButton.Hoverimage


        self.NumOwnedText = Functions.get_font(int(25 *self.enlargmentfactor[0])).render(f'Owned: 0', False, (255,255,255))
        self.NumOwnedRect = self.NumOwnedText.get_rect(topright= (self.ScreenLength+25*self.enlargmentfactor[0], self.ScreenWidth/5*4))

        self.Shop()

    def GetItems(self):
        self.onsale = []
        for item in self.items:
            if (item.name not in [i.name for i in self.player.items] and (item.prereq in [type(i) for i in self.player.items] or item.prereq == None)) or item.purchased:

                itemdisplay = self.Itemdisplay.copy()
                itemdisplay.blit(item.image, item.image.get_rect(center=  (self.Itemdisplay.get_size()[0]//2, self.Itemdisplay.get_size()[1]//2-25)))
                Price = Functions.get_font(20).render(f'{item.price}', True, (255,255,255))
                itemdisplay.blit(Price, (itemdisplay.get_size()[0]-Price.get_size()[0]-50, itemdisplay.get_size()[1]-Price.get_size()[1]-10))
                Title = Functions.get_font(30).render(f'{item.name}', True, (255,255,255))
                itemdisplay.blit(Title, Title.get_rect(center= (itemdisplay.get_size()[0]/2, 25)))
                descriptionDisplay = self.Description.copy()
                description = item.description.split('\n')
                for index,text in enumerate(description):
                    indexnumber = (len(description)-1)/2
                    if len(description) %2 == 0:
                        if index < indexnumber:
                            indexnumber = index - indexnumber -.5
                        else:
                            indexnumber = index-.5
                    else:
                        if index < indexnumber:
                            indexnumber = index - indexnumber-.5
                        elif index == indexnumber:
                            indexnumber = 0
                        else:
                            indexnumber = index-.5
                    Description = Functions.get_font(15).render(f'{text}', True, (255,255,255))
                    descriptionDisplay.blit(Description, Description.get_rect(center= (descriptionDisplay.get_size()[0]/2, descriptionDisplay.get_size()[1]/2 + (Description.get_size()[1]+10) * indexnumber)))
                if item.purchased:
                    itemdisplay.blit(self.PurchasedScreen, (0, 0))

                self.onsale.append([itemdisplay,itemdisplay.get_bounding_rect(),item, itemdisplay.copy(),descriptionDisplay])
        self.onsaleconsumables = []
        for item in self.consumables:
            if (item.prereq in [type(i) for i in self.player.items] or item.prereq == None):
                itemdisplay = self.Itemdisplay.copy()
                itemdisplay.blit(item.image, item.image.get_rect(
                    center=(self.Itemdisplay.get_size()[0] // 2, self.Itemdisplay.get_size()[1] // 2 - 25)))
                Price = Functions.get_font(20).render(f'{item.price}', True, (255, 255, 255))
                itemdisplay.blit(Price, (itemdisplay.get_size()[0] - Price.get_size()[0] - 50,
                                         itemdisplay.get_size()[1] - Price.get_size()[1] - 10))
                Title = Functions.get_font(45).render(f'{item.name}', True, (255, 255, 255))
                itemdisplay.blit(Title, Title.get_rect(center=(itemdisplay.get_size()[0] / 2, 25)))
                descriptionDisplay = self.Description.copy()
                description = item.description.split('\n')
                for index, text in enumerate(description):
                    indexnumber = (len(description) - 1) / 2
                    if len(description) % 2 == 0:
                        if index < indexnumber:
                            indexnumber = index - indexnumber - .5
                        else:
                            indexnumber = index - .5
                    else:
                        if index < indexnumber:
                            indexnumber = index - indexnumber - .5
                        elif index == indexnumber:
                            indexnumber = 0
                        else:
                            indexnumber = index - .5
                    Description = Functions.get_font(15).render(f'{text}', True, (255, 255, 255))
                    descriptionDisplay.blit(Description, Description.get_rect(center=(
                    descriptionDisplay.get_size()[0] / 2,
                    descriptionDisplay.get_size()[1] / 2 + (Description.get_size()[1] + 10) * indexnumber)))

                self.onsaleconsumables.append(
                    [itemdisplay, itemdisplay.get_bounding_rect(), item, itemdisplay.copy(), descriptionDisplay])



    def DrawItems(self,itemindex):
        for index, item in enumerate(self.onsale):
            item[0] = pygame.transform.scale_by(item[3], (8-abs(index-itemindex))/8)
            item[1] = item[0].get_bounding_rect()
            item[1].center = (self.BuyablesArea.get_size()[0]/2 + (item[1].width+50)*(index-itemindex), self.BuyablesArea.get_size()[1]/2)
            if index-itemindex != 0:
                item[0].blit(self.obscuringLayer, (0,0))
            else:
                item[0].blit(item[3], (0,0))
                self.SelectedItem = item

        self.currentindex = itemindex
    def DrawConsumables(self, itemindex):
        for index, item in enumerate(self.onsaleconsumables):
            item[0] = pygame.transform.scale_by(item[3], (8-abs(index-itemindex))/8)
            item[1] = item[0].get_bounding_rect()
            item[1].center = (self.BuyablesArea.get_size()[0]/2 + (item[1].width+50)*(index-itemindex), self.BuyablesArea.get_size()[1]/2)
            if index-itemindex != 0:
                item[0].blit(self.obscuringLayer, (0,0))
            else:
                item[0].blit(item[3], (0,0))
                self.SelectedItem = item

        self.currentindex = itemindex

    def IncrementItems(self, direction):
        if self.EquippablesButton.clicked:
            self.DrawItems(self.currentindex + direction)
        else:
            print('test')
            self.DrawConsumables(self.currentindex + direction)


    def Purchase(self):
        self.SelectedItem[2].Buy(self.player)

        self.player.money -= self.SelectedItem[2].price

        if self.EquippablesButton.clicked:
            self.SelectedItem[3].blit(self.PurchasedScreen, (0, 0))
            self.SelectedItem[2].purchased = True
            self.DrawItems(self.currentindex)
            self.player.items.append(self.SelectedItem[2])
            for i in self.player.items:
                if issubclass(type(i), Classes.primaryWeapon):
                    if self.player.primaryWeapon:
                        if i.prioritycount > self.player.primaryWeapon.prioritycount:
                            self.player.primaryWeapon = i
                    else:
                        self.player.primaryWeapon = i
                elif issubclass(type(i), Classes.secondaryWeapon):
                    if self.player.secondaryWeapon:
                        if i.prioritycount > self.player.secondaryWeapon.prioritycount:
                            self.player.secondaryWeapon = i
                    else:
                        self.player.secondaryWeapon = i
        else:
            self.DrawConsumables(self.currentindex)
            for i in self.player.items:
                if issubclass(type(i), Classes.primaryWeapon):
                    if self.player.primaryWeapon:
                        if i.prioritycount > self.player.primaryWeapon.prioritycount:
                            self.player.primaryWeapon = i
                    else:
                        self.player.primaryWeapon = i
                elif issubclass(type(i), Classes.secondaryWeapon):
                    if self.player.secondaryWeapon:
                        if i.prioritycount > self.player.secondaryWeapon.prioritycount:
                            self.player.secondaryWeapon = i
                    else:
                        self.player.secondaryWeapon = i

        self.wallet = Functions.get_font(50).render(f'{self.player.money}', True, (255,239,0))
        self.walletRect = self.wallet.get_rect(center= (self.ScreenLength-self.wallet.get_size()[0], 200))
        self.GetItems()


    def Continue(self):
        Functions.SaveGame(self.player)
        Main.game(False, self.player, self.player.levelnum, self.player.seed, self.screen, self.screen.get_size())

    def Shop(self):
        self.GetItems()
        self.DrawItems(self.currentindex)
        while self.shopopen:
            if self.EquippablesButton.clicked:
                self.DrawItems(self.currentindex )
            else:
                self.DrawConsumables(self.currentindex)
            self.screen.fill((0,0,0))
            menumouseposition = pygame.mouse.get_pos()
            self.screen.blit(self.background, (0,0))

            self.BuyablesArea.fill((77,77,77))

            if self.SelectedItem:
                if self.EquippablesButton.clicked:
                    for itemonsale in self.onsale:
                        self.BuyablesArea.blit(itemonsale[0], itemonsale[1])
                else:
                    for itemonsale in self.onsaleconsumables:
                        self.BuyablesArea.blit(itemonsale[0], itemonsale[1])

                    try:
                        count = self.player.items[[i.name for i in self.player.items].index(self.SelectedItem[2].name)].ammunitioncount
                    except:
                        count = 0
                    self.NumOwnedText = Functions.get_font(int(25*self.enlargmentfactor[0])).render(f'Owned: {int(count)}', False, (255,255,255))
                    self.NumOwnedRect = self.NumOwnedText.get_rect(
                        topright=(self.ScreenLength -25 * self.enlargmentfactor[0], self.ScreenWidth / 5 * 4))

                    self.screen.blit(self.NumOwnedText, self.NumOwnedRect)

                Rect = self.SelectedItem[4].get_rect(center=(self.ScreenLength / 2, (self.ScreenWidth / 8) * 7))
                self.screen.blit(self.SelectedItem[4], Rect)
            else:
                self.BuyablesArea.blit(pygame.transform.scale(pygame.image.load('./Art/Shop/Sold Out.png').convert_alpha(), (self.BuyablesArea.get_size())), (0,0))

            self.screen.blit(self.BuyablesArea, (0,self.ScreenWidth/4))
            self.screen.blit(self.MENUtext, self.MENUrect)
            self.screen.blit(self.wallet, self.walletRect)
            self.screen.blit(self.walletImage, self.walletImagerect)

            if self.currentindex != 0:
                self.LeftButton.changeColor(menumouseposition)
                self.LeftButton.update(self.screen)
            if self.EquippablesButton.clicked:
                if self.currentindex != len(self.onsale) -1 and self.SelectedItem:
                    self.RightButton.changeColor(menumouseposition)
                    self.RightButton.update(self.screen)
            else:
                if self.currentindex != len(self.onsaleconsumables) -1 and self.SelectedItem:
                    self.RightButton.changeColor(menumouseposition)
                    self.RightButton.update(self.screen)
            if self.SelectedItem:
                try:
                    test = [i.name for i in self.player.items].index(self.SelectedItem[2].name).ammunitioncount < self.SelectedItem[2].Maxamount
                except:
                    test = True


                if self.SelectedItem[2].price <= self.player.money and not self.SelectedItem[2].purchased and test:
                    self.PurchaseButton.changeColor(menumouseposition)
                else:
                    self.PurchaseButton.ForceColor((208,0,0))
            else:
                self.PurchaseButton.ForceColor((208, 0, 0))
            self.PurchaseButton.update(self.screen)


            for button in [self.ExitToMenuButton, self.ContinueButton, self.EquippablesButton, self.ConsumablesButton]:
                button.changeColor(menumouseposition)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.SelectedItem:
                            if self.PurchaseButton.checkForInput(menumouseposition) and self.SelectedItem[2].price <= self.player.money and not self.SelectedItem[2].purchased and test:
                                self.Purchase()
                        if self.ExitToMenuButton.checkForInput(menumouseposition):
                            Functions.SaveGame(self.player)
                            mainmenu.main_menu(self.screen, (self.ScreenLength, self.ScreenWidth))
                        if self.ContinueButton.checkForInput(menumouseposition):
                            self.Continue()
                        if self.LeftButton.checkForInput(menumouseposition) and self.currentindex !=0:
                            self.IncrementItems(-1)
                        if self.EquippablesButton.clicked:
                            if self.RightButton.checkForInput(menumouseposition) and self.currentindex != len(self.onsale) -1:
                                self.IncrementItems(1)
                                print('test')
                        else:
                            if self.RightButton.checkForInput(menumouseposition) and self.currentindex != len(self.onsaleconsumables) -1:
                                self.IncrementItems(1)
                                print('test')
                        check = self.EquippablesButton.checkForInput(menumouseposition)
                        if check == 0:
                            self.ConsumablesButton.image = self.ConsumablesButton.Hoverimage
                            self.ConsumablesButton.clicked = True
                            self.currentindex = 0
                            self.DrawConsumables(self.currentindex)
                        elif check == 1:
                            self.ConsumablesButton.image = self.ConsumablesButton.regularimage
                            self.ConsumablesButton.clicked = False
                            self.currentindex = 0
                            self.DrawItems(self.currentindex)
                        check = self.ConsumablesButton.checkForInput(menumouseposition)
                        if check == 0:
                            self.EquippablesButton.image = self.EquippablesButton.Hoverimage
                            self.EquippablesButton.clicked = True
                            self.currentindex = 0
                            self.DrawItems(self.currentindex)
                        elif check == 1:
                            self.EquippablesButton.image = self.EquippablesButton.regularimage
                            self.EquippablesButton.clicked = False
                            self.currentindex = 0
                            self.DrawConsumables(self.currentindex)

            pygame.display.update()

#Shop(Classes.Player('blank','blank', coins= 12000), screen, screen.get_size())
