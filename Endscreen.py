import pygame, sys

import Functions
import mainmenu
from Interactables import Button
import Shop


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

# main menu function controls, the other functions
def end_screen(display, displaysize, enlargmentvalue, player):
    pygame.mouse.set_visible(True)

    pygame.display.set_caption("Menu")
    background = pygame.Surface(displaysize)
    light_gray = ((84, 86, 86))
    background1 = pygame.Surface((880*enlargmentvalue[0], 280*enlargmentvalue[1]))
    Dark_gray = ((105, 105, 105))
    background1.fill(Dark_gray)
    background.fill(light_gray)
    background.set_alpha(75)
    paused = True

    player.levelnum +=1
    Functions.SaveGame(player)

    while paused:

        display.blit(background, (0,0))
        display.blit(background1, (200*enlargmentvalue[0],250*enlargmentvalue[1]))
        menumouseposition = pygame.mouse.get_pos()

        MENUtext = get_font(50).render("CONGRATULATIONS", True, "#b68f40")
        MENUrect = MENUtext.get_rect(center=(640*enlargmentvalue[0], 200*enlargmentvalue[1]))
        display.blit(MENUtext, MENUrect)
# creating the buttons
        ShopButton = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(950*enlargmentvalue[0], 650*enlargmentvalue[1]),
                            text_input="Continue to shop", font=get_font(int(35*enlargmentvalue[0])), base_color="#d7fcd4", hovering_color="White")
        MainMenuButton = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(240*enlargmentvalue[0], 50*enlargmentvalue[1]),
                            text_input="Exit to menu", font=get_font(int(35*enlargmentvalue[0])), base_color="#d7fcd4", hovering_color="White")

        # display Statistics

        statstext = get_font(35).render("Statistics:", True, "#2debae")
        statsrect = statstext.get_rect(center=(650*enlargmentvalue[0], 300*enlargmentvalue[1]))
        display.blit(statstext, statsrect)

# putting the button on the screen and making it change color if hovered over

        for button in [ShopButton, MainMenuButton]:
            button.changeColor(menumouseposition)
            button.update(display)

# Running through all the events to see if a button was clicked then run a function if something was clicked

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ShopButton.checkForInput(menumouseposition):
                    Shop.Shop(player, display,display.get_size())
                if MainMenuButton.checkForInput(menumouseposition):
                    mainmenu.main_menu(display, display.get_size())
        pygame.display.update()
#end_screen(screen)