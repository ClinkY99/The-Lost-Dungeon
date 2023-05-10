import pygame, sys
from button import Button
pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
background = pygame.Surface((1280, 720))
light_gray = ((84,86,86))
background.fill(light_gray)
background.set_alpha(75)



def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

# play function controls text, screen, a button clicking
def settings():
    while True:
        playmouseposition = pygame.mouse.get_pos()

        screen.fill("blue")

        PLAYtext = get_font(45).render("This is the Settings screen.", True, "White")
        PLAYrect = PLAYtext.get_rect(center=(640, 260))
        screen.blit(PLAYtext,PLAYrect )

        playback = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="turquoise")

        playback.changeColor(playmouseposition)
        playback.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playback.checkForInput(playmouseposition):
                    main_menu()

        pygame.display.update()

# options function controls text, screen, a button clicking
def resume():
    while True:
        optionsmouseposition = pygame.mouse.get_pos()

        screen.fill("red")

        OPTIONtext = get_font(45).render("Exit to Menu", True, "Black")
        OPTIONrect = OPTIONtext.get_rect(center=(640, 260))
        screen.blit(OPTIONtext, OPTIONrect)

        OPTIONback = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="turquoise")
        OPTIONback.changeColor(optionsmouseposition)
        OPTIONback.update(screen)

        tutorial = Button(image=None, pos=(640, 560),
                           text_input="TUTORIAL", font=get_font(75), base_color="Black", hovering_color="Green")
        tutorial.changeColor(optionsmouseposition)
        tutorial.update(screen)

        level = Button(image=None, pos=(640, 650),
                          text_input="LEVEL", font=get_font(75), base_color="Black", hovering_color="purple")
        level.changeColor(optionsmouseposition)
        level.update(screen)




        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONback.checkForInput(optionsmouseposition):
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level.checkForInput(optionsmouseposition):
                    level_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tutorial.checkForInput(optionsmouseposition):
                    tutorial_menu()

        pygame.display.update()
# Level function controls the level button in the options screen
def level_menu():
    while True:
        levelmouseposition = pygame.mouse.get_pos()

        screen.fill("yellow")
        leveltext = get_font(45).render("Resume", True, "Black")
        levelrect = leveltext.get_rect(center=(640, 260))
        screen.blit(leveltext, levelrect)

        levelback = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="turquoise")

        levelback.changeColor(levelmouseposition)
        levelback.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if levelback.checkForInput(levelmouseposition):
                    main_menu()
        pygame.display.update()

# tutorial function controls the tutorial button in the options screen
def tutorial_menu():
    while True:
        tutorialmouseposition = pygame.mouse.get_pos()
        screen.fill("blue")
        Tutorialtext = get_font(45).render("This is the TUTORIAL screen.", True, "Black")
        Tutorialrect = Tutorialtext.get_rect(center=(640, 260))
        screen.blit(Tutorialtext, Tutorialrect)

        tutorialback = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="turquoise")

        tutorialback.changeColor(tutorialmouseposition)
        tutorialback.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tutorialback.checkForInput(tutorialmouseposition):
                    main_menu()
        pygame.display.update()
# main menu function controls, the other functions
def Pause_menu():
    while True:
        screen.blit(background, (0,0))

        menumouseposition = pygame.mouse.get_pos()

        MENUtext = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENUrect = MENUtext.get_rect(center=(640, 100))

# displaying the buttons on the main menu
        PLAYbutton = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                            text_input="Settings", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONbutton = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                            text_input="Resume", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUITbutton = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                            text_input="Exit to Menu", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENUtext, MENUrect)

        for button in [PLAYbutton, OPTIONbutton, QUITbutton]:
            button.changeColor(menumouseposition)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAYbutton.checkForInput(menumouseposition):
                    play()

                if OPTIONbutton.checkForInput(menumouseposition):
                    options()
                if QUITbutton.checkForInput(menumouseposition):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()