import math
import random

import pygame, sys, json, Interactables, Main

import Classes
from Interactables import Button
DEFAULT_IMAGE_SIZE = (1280, 720)
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def NewGame(screen,size, background, enlargmentfactor):
    newgameopen = True

    newgamebackground = pygame.Surface((size[0]/3, size[1]/3))
    newgamebackground.fill((50,50,50))
    newgamebackground.set_alpha(225)
    newgamebackgroundrect = newgamebackground.get_rect(center = (size[0]/2, size[1]/2))


    screen.blit(newgamebackground, newgamebackgroundrect)

    MENUtext = get_font(int(15*enlargmentfactor[0])).render("Name:", True, (255,255,255))
    MENUrect = MENUtext.get_rect(center=(size[0]/3, size[1]/2-30*enlargmentfactor[0]))

    name_input_box = Interactables.TextInputBox(size[0]/2, size[1]/2-10*enlargmentfactor[1], 200*enlargmentfactor[0], get_font(int(20*enlargmentfactor[0])), (255,255,255), highlightcolor=(147,147,147))

    MENUrect.x = name_input_box.rect.x

    BackButton = Button(image=None, pos=(size[0]/3+50*enlargmentfactor[0], size[1]/2-50*enlargmentfactor[0]),
                        text_input="Back", font=get_font(int(15*enlargmentfactor[0])), base_color="#d7fcd4", hovering_color="White")

    ContinueButton = Button(image=None, pos=(size[0]/2 + newgamebackground.get_size()[0]/4, size[1]/2+50*enlargmentfactor[0]),
                        text_input="Continue", font=get_font(int(15*enlargmentfactor[0])), base_color="#d7fcd4", hovering_color="White")

    TutorialButton = Interactables.ImageButton(image=pygame.transform.scale_by(pygame.image.load('./Art/Menu/CheckBox_Unchecked.png'), enlargmentfactor[0]/3),
                                               Hoverimage= pygame.transform.scale_by(pygame.image.load('./Art/Menu/CheckBox_Checked.png'), enlargmentfactor[0]/3),
                                                pos=(size[0]/2 - 33 * enlargmentfactor[0],size[1]/2 + 40*enlargmentfactor[1]), stayclicked=True)
    TutorialButton.rect.x = name_input_box.rect.x




    while newgameopen:

        mousepositon = pygame.mouse.get_pos()

        screen.blit(background, (0, 0))
        screen.blit(newgamebackground, newgamebackgroundrect)
        screen.blit(MENUtext, MENUrect)
        screen.blit(name_input_box.image, name_input_box.rect)

        for i in [BackButton, ContinueButton, TutorialButton]:
            i.changeColor(mousepositon)
            i.update(screen)


        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    TutorialButton.checkForInput(mousepositon)
                    if BackButton.checkForInput(mousepositon):
                        newgameopen = False
                    if ContinueButton.checkForInput(mousepositon):
                        pygame.mixer.music.fadeout(750)
                        name = ''
                        file = open('./Saves/Save.Dungeon', 'r')

                        jsondata = json.load(file)
                        if name_input_box.text == '':
                            for i in range(1, 200):
                                try:
                                    jsondata['Saves'][f'Player {i}']
                                except:
                                    name = f'Player {i}'
                                    file.close()
                                    break
                        else:
                            name = name_input_box.text

                        file = open('./Saves/Save.Dungeon', 'w')

                        if not TutorialButton.clicked:
                            seed = random.randrange(sys.maxsize)
                        else:
                            seed = 10

                        player = Classes.Player(name, seed)


                        jsonoutput = {
                            "Level" : 1,
                            "Seed" :seed ,
                            "Player Data" : {
                                "coins": 0,
                                "health" : 100,
                                "score" : 0,
                                "items": [[i.name, i.ammunitioncount] for i in player.items]
                            }
                        }

                        jsondata["Saves"][f'{name}'] = jsonoutput

                        jsondata['MostRecentSave'] = name

                        json.dump(jsondata, file, indent= 4)
                        file.close()

                        for i in range(1,250):
                            background.fill((0,0,0))
                            background.set_alpha(i/5)
                            screen.blit(background, (0,0))
                            pygame.display.update()
                        Main.game(TutorialButton.clicked, player, 1, seed, screen, screen.get_size())




        name_input_box.update(event_list)

        pygame.display.update()

def loadGame(screen,size, background, enlargmentfactor ):
    loadgameopen = True

    loadgamebackground = pygame.Surface((size[0] / 3, size[1] / 3))
    loadgamebackground.fill((50, 50, 50))
    loadgamebackground.set_alpha(225)
    loadgamebackgroundrect = loadgamebackground.get_rect(center=(size[0] / 2, size[1] / 2))

    screen.blit(loadgamebackground, loadgamebackgroundrect)

    MENUtext = get_font(int(15 * enlargmentfactor[0])).render("Save Name:", True, (255, 255, 255))
    MENUrect = MENUtext.get_rect(center=(size[0] / 3, size[1] / 2 - 30 * enlargmentfactor[0]))

    name_input_box = Interactables.TextInputBox(size[0] / 2, size[1] / 2 - 10 * enlargmentfactor[1],
                                                200 * enlargmentfactor[0], get_font(int(20 * enlargmentfactor[0])),
                                                (255, 255, 255), highlightcolor=(147, 147, 147))

    MENUrect.x = name_input_box.rect.x

    BackButton = Button(image=None,
                        pos=(size[0] / 3 + 50 * enlargmentfactor[0], size[1] / 2 - 50 * enlargmentfactor[0]),
                        text_input="Back", font=get_font(int(15 * enlargmentfactor[0])), base_color="#d7fcd4",
                        hovering_color="White")

    ContinueButton = Button(image=None, pos=(
    size[0] / 2 + loadgamebackground.get_size()[0] / 4, size[1] / 2 + 50 * enlargmentfactor[0]),
                            text_input="Continue", font=get_font(int(15 * enlargmentfactor[0])), base_color="#d7fcd4",
                            hovering_color="White")

    while loadgameopen:

        mousepositon = pygame.mouse.get_pos()

        screen.blit(background, (0, 0))
        screen.blit(loadgamebackground, loadgamebackgroundrect)
        screen.blit(MENUtext, MENUrect)
        screen.blit(name_input_box.image, name_input_box.rect)

        file = open('./Saves/Save.Dungeon')

        jsondata = json.load(file)
        file.close()

        try:
            if jsondata['Saves'][f'{name_input_box.text}']:
                saveexists = True
                ContinueButton.changeColor(mousepositon)
        except:
            saveexists = False
            ContinueButton.ForceColor((208,0,0))

        ContinueButton.update(screen)


        for i in [BackButton]:
            i.changeColor(mousepositon)
            i.update(screen)

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if BackButton.checkForInput(mousepositon):
                        loadgameopen = False
                    if ContinueButton.checkForInput(mousepositon) and saveexists:
                        pygame.mixer.music.fadeout(750)
                        file = open('./Saves/Save.Dungeon', 'r')

                        jsondata = json.load(file)
                        file.close()

                        name = name_input_box.text

                        savedata = jsondata['Saves'][f'{name}']

                        items = []
                        for i in savedata['Player Data']['items']:
                            item = Classes.itemreference[i[0]]()
                            if issubclass(type(item), Classes.secondaryWeapon):
                                item.ammunitioncount = i[1]
                            items.append(item)

                        player = Classes.Player(name, savedata['Seed'], coins=savedata['Player Data']['coins'], levelnum=savedata['Level'],
                                                score=savedata['Player Data']['score'],
                                                health=savedata['Player Data']['health'],
                                                items=items)

                        file = open('./Saves/Save.Dungeon', 'w')


                        jsondata['MostRecentSave'] = name

                        json.dump(jsondata, file, indent=4)

                        for i in range(1, 250):
                            background.fill((0, 0, 0))
                            background.set_alpha(i / 5)
                            screen.blit(background, (0, 0))
                            pygame.display.update()
                        Main.game(False, player, 1, savedata['Seed'],screen, screen.get_size())

        name_input_box.update(event_list)

        pygame.display.update()

# play function controls text, display, and button clicking for play screen
def play(display,size):
    background = pygame.image.load("assets/Hotpot-2.png")
    background = pygame.transform.scale(background, size)

    coverbox = pygame.transform.scale(pygame.image.load('./Art/Menu/CoverBox.png'), (size[0]/2,size[1]))


    enlargmentfactor = (size[0]/DEFAULT_IMAGE_SIZE[1], size[1]/DEFAULT_IMAGE_SIZE[1])

    MENUtext = get_font(100).render("THE LOST DUNGEON", True, "#b68f40")
    MENUrect = MENUtext.get_rect(center=(size[0] / 2, 100))

    f = open('./Saves/Save.Dungeon')

    savedata = json.load(f)

    if savedata['MostRecentSave'] != "None":
        ContinueGame = Button(image=None, pos=(size[0]/4, size[1]-275*enlargmentfactor[0]),
                              text_input="Continue", font=get_font(int(35*enlargmentfactor[0])), base_color="#d7fcd4", hovering_color="White")
    else:
        ContinueGame = Button(image=None, pos=(size[0]/4, size[1]-275*enlargmentfactor[0]),
                              text_input="Continue", font=get_font(int(35*enlargmentfactor[0])), base_color=(73,73,73), hovering_color="White", disabled=True)

    # creating the buttons
    NewGameButton = Button(image=None, pos=(size[0]/4, size[1]-200*enlargmentfactor[0]),
                     text_input="New Game", font=get_font(int(35*enlargmentfactor[0])), base_color="#d7fcd4", hovering_color="White")
    LoadGame = Button(image=None, pos=(size[0]/4, size[1]-125*enlargmentfactor[0]),
                      text_input="Load Game", font=get_font(int(35*enlargmentfactor[0])), base_color="#d7fcd4", hovering_color="White")
    BackButton = Button(image=None, pos=(size[0]/4, size[1]-50*enlargmentfactor[0]),
                        text_input="Back", font=get_font(int(35*enlargmentfactor[0])), base_color="#d7fcd4", hovering_color="White")

    f.close()
    display.blit(background, (0,0))
    display.blit(coverbox, (0,0))
    display.blit(MENUtext,MENUrect)


    playmenuopen = True

    while playmenuopen:
        playmouseposition = pygame.mouse.get_pos()

        for i in [NewGameButton, LoadGame, BackButton, ContinueGame]:
            i.changeColor(playmouseposition)
            i.update(display)

        # Running through all the events to see if a button was clicked then run a function if something was clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if BackButton.checkForInput(playmouseposition):
                        playmenuopen = False

                    if NewGameButton.checkForInput(playmouseposition):
                        NewGame(display,display.get_size(), display.copy(), enlargmentfactor)
                        display.blit(background, (0, 0))
                        display.blit(coverbox, (0, 0))
                        display.blit(MENUtext, MENUrect)
                    if ContinueGame.checkForInput(playmouseposition):
                        pygame.mixer.music.fadeout(750)
                        file = open('./Saves/Save.Dungeon', 'r')

                        jsondata = json.load(file)

                        savedata = jsondata['Saves'][f'{jsondata["MostRecentSave"]}']

                        items = []
                        for i in savedata['Player Data']['items']:
                            item = Classes.itemreference[i[0]]()
                            if issubclass(type(item), Classes.consumable):
                                item.ammunitioncount = i[1]
                            elif issubclass(type(item), Classes.secondaryWeapon):
                                item.Buy(items, True)
                            items.append(item)

                        player = Classes.Player(jsondata["MostRecentSave"], savedata['Seed'], coins= savedata['Player Data']['coins'], levelnum= savedata['Level'], score= savedata['Player Data']['score'], health= savedata['Player Data']['health'], items=items)
                        for i in range(1,100):
                            background.fill((0,0,0))
                            background.set_alpha(i)
                            display.blit(background, (0,0))
                            pygame.display.update()
                        Main.game(False, player, player.levelnum, savedata['Seed'],display, display.get_size())
                    if LoadGame.checkForInput(playmouseposition):
                        loadGame(display,display.get_size(), display.copy(), enlargmentfactor)
                        display.blit(background, (0, 0))
                        display.blit(coverbox, (0, 0))
                        display.blit(MENUtext, MENUrect)



        pygame.display.update()

# options function controls text, display, and button clicking for options screen
def options(display):
    while True:
        optionsmouseposition = pygame.mouse.get_pos()

        display.fill("red")

        OPTIONtext = get_font(45).render("This is the OPTIONS display.", True, "Black")
        OPTIONrect = OPTIONtext.get_rect(center=(640, 260))
        display.blit(OPTIONtext, OPTIONrect)
        # creating the buttons
        OPTIONback = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="turquoise")
        OPTIONback.changeColor(optionsmouseposition)
        OPTIONback.update(display)
        # creating the buttons
        tutorial = Button(image=None, pos=(640, 560),
                           text_input="TUTORIAL", font=get_font(75), base_color="Black", hovering_color="Green")
        tutorial.changeColor(optionsmouseposition)
        tutorial.update(display)
        # creating the buttons
        level = Button(image=None, pos=(640, 650),
                          text_input="LEVEL", font=get_font(75), base_color="Black", hovering_color="purple")
        level.changeColor(optionsmouseposition)
        level.update(display)

        # Running through all the events to see if a button was clicked then run a function if something was clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONback.checkForInput(optionsmouseposition):
                    main_menu(display,display.get_size())
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level.checkForInput(optionsmouseposition):
                    level_menu(display)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tutorial.checkForInput(optionsmouseposition):
                    tutorial_menu(display)

        pygame.display.update()

# level menu function controls text, display, and button clicking for level menu screen
def level_menu(display):
    while True:
        levelmouseposition = pygame.mouse.get_pos()

        display.fill("yellow")
        leveltext = get_font(45).render("This is the LEVEL display.", True, "Black")
        levelrect = leveltext.get_rect(center=(640, 260))
        display.blit(leveltext, levelrect)
        # creating the buttons
        levelback = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="turquoise")

        levelback.changeColor(levelmouseposition)
        levelback.update(display)

        # Running through all the events to see if a button was clicked then run a function if something was clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if levelback.checkForInput(levelmouseposition):
                    main_menu(display, display.get_size())
        pygame.display.update()

# tutorial menu function controls text, display, and button clicking for tutorial screen
def tutorial_menu(display):
    while True:
        tutorialmouseposition = pygame.mouse.get_pos()
        display.fill("blue")
        Tutorialtext = get_font(45).render("This is the TUTORIAL display.", True, "Black")
        Tutorialrect = Tutorialtext.get_rect(center=(640, 260))
        display.blit(Tutorialtext, Tutorialrect)
        # creating the buttons
        tutorialback = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="turquoise")

        tutorialback.changeColor(tutorialmouseposition)
        tutorialback.update(display)
        # Running through all the events to see if a button was clicked then run a function if something was clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tutorialback.checkForInput(tutorialmouseposition):
                    main_menu(display,display.get_size())
        pygame.display.update()

# main menu function controls text, display, and button clicking for main menu screen and the other functions
def main_menu(display,size):
    background = pygame.image.load("assets/Hotpot-2.png")
    background = pygame.transform.scale(background, size)

    pygame.mixer.music.stop()
    pygame.mixer.music.load('./Music/Menu.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1)
    while True:
        display.blit(background, (0, 0))

        menumouseposition = pygame.mouse.get_pos()
        # sizing the buttons
        MENUtext = get_font(100).render("THE LOST DUNGEON", True, "#b68f40")
        MENUrect = MENUtext.get_rect(center=(size[0]/2, 100))
        Playbuttonimage = pygame.image.load("assets/Play Rect.png")
        Playbuttonimage = pygame.transform.scale(Playbuttonimage, (math.ceil(Playbuttonimage.get_size()[0] * (size[0]//DEFAULT_IMAGE_SIZE[0]) *1.5),math.ceil(Playbuttonimage.get_size()[1]*(size[1]//DEFAULT_IMAGE_SIZE[1])*1.5)))

        # sizing the buttons
        OPTIONbuttonimage = pygame.image.load("assets/Options Rect.png")
        OPTIONbuttonimage = pygame.transform.scale(OPTIONbuttonimage, (
            math.ceil(OPTIONbuttonimage.get_size()[0] * (size[0] // DEFAULT_IMAGE_SIZE[0]) * 1.5),
            math.ceil(OPTIONbuttonimage.get_size()[1] * (size[1] // DEFAULT_IMAGE_SIZE[1]) * 1.5)))

        # sizing the buttons
        Quitbuttonimage =pygame.image.load("assets/Quit Rect.png")
        Quitbuttonimage = pygame.transform.scale(Quitbuttonimage, (
            math.ceil(Quitbuttonimage.get_size()[0] * (size[0] // DEFAULT_IMAGE_SIZE[0]) * 1.5),
            math.ceil(Quitbuttonimage.get_size()[1] * (size[1] // DEFAULT_IMAGE_SIZE[1]) * 1.5)))

# displaying the buttons on the main menu
        PLAYbutton = Button(image=Playbuttonimage, pos=(size[0]/2, (size[1]/4)*1.5),
                            text_input="PLAY", font=get_font(math.ceil(size[0]//DEFAULT_IMAGE_SIZE[0]*75*1.5)), base_color="#d7fcd4", hovering_color="White")
        OPTIONbutton = Button(image=OPTIONbuttonimage, pos=(size[0]/2, (size[1]/4)*2.5),
                            text_input="OPTIONS", font=get_font(math.ceil(size[0]//DEFAULT_IMAGE_SIZE[0]*75*1.5)), base_color="#d7fcd4", hovering_color="White")
        QUITbutton = Button(image=Quitbuttonimage, pos=(size[0]/2, (size[1]/4)*3.5),
                            text_input="QUIT", font=get_font(math.ceil(size[0]//DEFAULT_IMAGE_SIZE[0]*75*1.5)), base_color="#d7fcd4", hovering_color="White")

        display.blit(MENUtext, MENUrect)

        # putting the button on the screen and making it change color if hovered over
        for button in [PLAYbutton, OPTIONbutton, QUITbutton]:
            button.changeColor(menumouseposition)
            button.update(display)

        # Running through all the events to see if a button was clicked then run a function if something was clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if PLAYbutton.checkForInput(menumouseposition):
                        play(display, display.get_size())
                    if OPTIONbutton.checkForInput(menumouseposition):
                        options(display)
                    if QUITbutton.checkForInput(menumouseposition):
                        pygame.quit()
                        sys.exit()

        pygame.display.update()

#Splash function displays the splash screen and calls main menu function
def splash(display, size):

    opening = pygame.mixer.Sound('./Music/Company_Intro.mp3')
    opening.play()

    enlagmentfactorx = size[0] / DEFAULT_IMAGE_SIZE[0]
    enlagmentfactory = size[1]/DEFAULT_IMAGE_SIZE[1]

    background = pygame.image.load("assets/Hotpot-2.png")
    splashtext = get_font(int(50 * enlagmentfactorx)).render("THE LOST DUNGEON.", True, "White")
    splashrect = splashtext.get_rect(center = (size[0]/2, size[1]/4))

    names = get_font(int(25*enlagmentfactorx)).render("By Maddox Ganesh, and Kieran Cline", True, "White")
    namesrect= names.get_rect(center = (size[0]/2, size[1]/4+25+splashrect.height))

    text = get_font(int(50*enlagmentfactorx)).render("Click to continue", True, "White")
    textrect = text.get_rect(center = (size[0]/2, size[1]/6*5))

    background1 = pygame.transform.scale(background, size)

    company = pygame.image.load('Art/Menu/Company Intro.png').convert_alpha()

    companyrect = company.get_rect(center = (size[0]/2,size[1]/2))

    display.blit(company, companyrect)

    pygame.time.set_timer(pygame.event.Event(100), 2500, loops= 1)

    # Running through all the events to see if a button was clicked then run a function if something was clicked
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                opening.stop()
                main_menu(display, size)

            if event.type == 100:
                print(event.type)
                display.blit(background1, (0, 0))
                display.blit(splashtext, splashrect)
                display.blit(names, namesrect)
                display.blit(text, textrect)
        pygame.display.update()

#Game function to monitor the timing and prevent screen from quitting immediately.
def game():
    clock = pygame.time.Clock()
    FPS = 50
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pygame.display.update()
        clock.tick(FPS)
