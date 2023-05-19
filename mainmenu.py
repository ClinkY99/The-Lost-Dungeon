import math
import pygame, sys
from button import Button
pygame.init()
DEFAULT_IMAGE_SIZE = (1280, 720)
ScreenLength = 1280
ScreenWidth = 720
screen = pygame.display.set_mode((ScreenLength, ScreenWidth))
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

# play function controls text, display, and button clicking for play screen
def play(display):
    while True:
        playmouseposition = pygame.mouse.get_pos()
        display.fill("blue")
        PLAYtext = get_font(45).render("This is the PLAY display.", True, "White")
        PLAYrect = PLAYtext.get_rect(center=(640, 260))
        display.blit(PLAYtext,PLAYrect)

        # creating the buttons
        playback = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="turquoise")
        playback.changeColor(playmouseposition)
        playback.update(display)

        # Running through all the events to see if a button was clicked then run a function if something was clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playback.checkForInput(playmouseposition):
                    main_menu(display,display.get_size())

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
    while True:
        display.blit(background, (0, 0))

        menumouseposition = pygame.mouse.get_pos()
        # sizing the buttons
        MENUtext = get_font(100).render("MAIN MENU", True, "#b68f40")
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
                        play(display)
                    if OPTIONbutton.checkForInput(menumouseposition):
                        options(display)
                    if QUITbutton.checkForInput(menumouseposition):
                        pygame.quit()
                        sys.exit()

        pygame.display.update()

#Splash function displays the splash screen and calls main menu function
def splash(display, size):
    background = pygame.image.load("assets/Hotpot-2.png")
    splashtext = get_font(45).render("DARKEST DUNGEON.", True, "White")
    names = get_font(25).render("By Maddox Ganesh, and Kieran Cline", True, "White")
    text = get_font(45).render("Click to continue", True, "White")
    DEFAULT_IMAGE_SIZE = (1280, 720)
    background1 = pygame.transform.scale(background, DEFAULT_IMAGE_SIZE)
    screen.blit(background1, (0, 0))
    screen.blit(splashtext, (320, 140))
    screen.blit(names, (240, 240))
    screen.blit(text, (260, 500))

    # Running through all the events to see if a button was clicked then run a function if something was clicked
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                main_menu(display, size)
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
