import pygame, sys
from button import Button
from mainmenu import main_menu
from settings import settings
pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
background = pygame.Surface((1280, 720))
light_gray = ((84,86,86))
background.fill(light_gray)
background.set_alpha(75)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

# Makes paused function flae so game starts again
def resume():
    paused = False
    print(paused)

# pause menu function controls the buttons and connect to the other functions
def Pause_menu(display):
    paused = True
    while paused:
        display.blit(background, (0,0))

        menumouseposition = pygame.mouse.get_pos()

        MENUtext = get_font(100).render("PAUSE MENU", True, "#b68f40")
        MENUrect = MENUtext.get_rect(center=(640, 100))

# displaying the buttons on the main menu
        resumebutton = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 250),
                            text_input="Resume", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        settingsbutton = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 400),
                            text_input="Settings", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUITbutton = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                            text_input="Exit to Menu", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENUtext, MENUrect)

        # putting the button on the screen and making it change color if hovered over
        for button in [settingsbutton, resumebutton, QUITbutton]:
            button.changeColor(menumouseposition)
            button.update(screen)

        # Running through all the events to see if a button was clicked then run a function if something was clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if settingsbutton.checkForInput(menumouseposition):
                    settings(display)
                if resumebutton.checkForInput(menumouseposition):
                    paused = False
                if QUITbutton.checkForInput(menumouseposition):
                    main_menu(screen, screen.get_size())

        pygame.display.update()
Pause_menu(screen)