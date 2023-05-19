import pygame, sys
from button import Button
from mainmenu import main_menu

pygame.init()

# a different background for the darker gray areas of the screen
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
background = pygame.Surface((1280, 720))
light_gray = ((84,86,86))
background.fill(light_gray)

# a different background for the darker gray areas of the screen
background1 = pygame.Surface((300, 430))
Dark_gray = ((105,105,105))
background1.fill(Dark_gray)
background.set_alpha(75)

# a different background for the darker gray areas of the screen
background2 = pygame.Surface((300, 430))
background2.fill(Dark_gray)
background2.set_alpha(75)

# a different background for the darker gray areas of the screen
background3 = pygame.Surface((300, 430))
background3.fill(Dark_gray)
background3.set_alpha(75)

screen = pygame.display.set_mode((1280, 720))

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

# main menu function controls, the other functions
def Pause_menu(display):
    paused = True
    while paused:
        display.blit(background, (0,0))
        display.blit(background1, (825,150))
        display.blit(background2, (475,150))
        display.blit(background3, (125,150))

        menumouseposition = pygame.mouse.get_pos()

        MENUtext = get_font(50).render("You Died", True, "#b68f40")
        MENUrect = MENUtext.get_rect(center=(640, 100))
        screen.blit(MENUtext, MENUrect)

# displaying the buttons on the main menu
        ShopButton = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(850, 650),
                            text_input="Continue to credits", font=get_font(35), base_color="#d7fcd4", hovering_color="White")

        # display Score board
        scoretext = get_font(25).render("Score board:", True, "#2debae")
        scorerect = scoretext.get_rect(center=(285, 200))
        screen.blit(scoretext, scorerect)
        # display Items

        itemtext = get_font(25).render("Items:", True, "#2debae")
        itemrect = itemtext.get_rect(center=(620, 200))
        screen.blit(itemtext, itemrect)

        # display Statistics
        statstext = get_font(25).render("Statistics:", True, "#2debae")
        statsrect = statstext.get_rect(center=(975, 200))
        screen.blit(statstext, statsrect)
# putting the button on the screen and making it change color if hovered over
        for button in [ShopButton]:
            button.changeColor(menumouseposition)
            button.update(screen)

#Running through all the events to see if a button was clicked then run a function if something was clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ShopButton.checkForInput(menumouseposition):
                    #credit function
                    main_menu(screen, screen.get_size())


        pygame.display.update()
Pause_menu(screen)