import pygame, sys, math

import Functions
from Interactables import Button
import mainmenu
from settings import settings


DEFAULT_IMAGE_SIZE = (1280, 720)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

# pause menu function controls the buttons and connect to the other functions
def Pause_menu(display, size, player):

    pygame.mixer.music.pause()

    displaycopy = display.copy()

    background = pygame.Surface(size)
    light_gray = ((84, 86, 86))
    background.fill(light_gray)
    background.set_alpha(200)
    display.blit(background, (0, 0))
    paused = True

    pygame.mouse.set_visible(True)

    while paused:


        menumouseposition = pygame.mouse.get_pos()

        MENUtext = get_font(100).render("Game Is Paused", True, "#b68f40")
        MENUrect = MENUtext.get_rect(center=(size[0]/2, 100))

# displaying the buttons on the main menu
        Playbuttonimage = pygame.image.load("assets/Play Rect.png")
        Playbuttonimage = pygame.transform.scale(Playbuttonimage, (
        math.ceil(Playbuttonimage.get_size()[0] * (size[0] // DEFAULT_IMAGE_SIZE[0]) * 1.5),
        math.ceil(Playbuttonimage.get_size()[1] * (size[1] // DEFAULT_IMAGE_SIZE[1]) * 1.5)))

        # sizing the buttons
        OPTIONbuttonimage = pygame.image.load("assets/Options Rect.png")
        OPTIONbuttonimage = pygame.transform.scale(OPTIONbuttonimage, (
            math.ceil(OPTIONbuttonimage.get_size()[0] * (size[0] // DEFAULT_IMAGE_SIZE[0]) * 1.5),
            math.ceil(OPTIONbuttonimage.get_size()[1] * (size[1] // DEFAULT_IMAGE_SIZE[1]) * 1.5)))

        # sizing the buttons
        Quitbuttonimage = pygame.image.load("assets/Quit Rect.png")
        Quitbuttonimage = pygame.transform.scale(Quitbuttonimage, (
            math.ceil(Quitbuttonimage.get_size()[0] * (size[0] // DEFAULT_IMAGE_SIZE[0]) * 1.5),
            math.ceil(Quitbuttonimage.get_size()[1] * (size[1] // DEFAULT_IMAGE_SIZE[1]) * 1.5)))

        # displaying the buttons on the main menu
        resumebutton = Button(image=Playbuttonimage.set_alpha(0), pos=(size[0] / 2, (size[1] / 4) * 1.5),
                            text_input="Resume Game", font=get_font(math.ceil(size[0] // DEFAULT_IMAGE_SIZE[0] * 50 * 1.5)),
                            base_color="#d7fcd4", hovering_color="White")
        settingsbutton = Button(image=OPTIONbuttonimage.set_alpha(0), pos=(size[0] / 2, (size[1] / 4) * 2.5),
                              text_input="Settings",
                              font=get_font(math.ceil(size[0] // DEFAULT_IMAGE_SIZE[0] * 50 * 1.5)),
                              base_color="#d7fcd4", hovering_color="White")
        QUITbutton = Button(image=Quitbuttonimage.set_alpha(0), pos=(size[0] / 2, (size[1] / 4) * 3.5),
                            text_input="Save & Quit", font=get_font(math.ceil(size[0] // DEFAULT_IMAGE_SIZE[0] * 50 * 1.5)),
                            base_color="#d7fcd4", hovering_color="White")

        display.blit(MENUtext, MENUrect)

        # putting the button on the screen and making it change color if hovered over
        for button in [settingsbutton, resumebutton, QUITbutton]:
            button.changeColor(menumouseposition)
            button.update(display)

        # Running through all the events to see if a button was clicked then run a function if something was clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if settingsbutton.checkForInput(menumouseposition):
                    settings(display,display.get_size())
                    display.blit(displaycopy, (0,0))
                    display.blit(background, (0,0))
                if resumebutton.checkForInput(menumouseposition):
                    paused = False
                    pygame.mouse.set_visible(False)
                    pygame.mixer.music.unpause()

                if QUITbutton.checkForInput(menumouseposition):
                    Functions.SaveGame(player)
                    mainmenu.main_menu(display, display.get_size())

        pygame.display.update()