import pygame, sys
from mainmenu import main_menu
from button import Button
pygame.init()


screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
background = pygame.Surface((1280, 720))
light_gray = ((84,86,86))
background1 = pygame.Surface((880, 280))
Dark_gray = ((105,105,105))
background1.fill(Dark_gray)
background.fill(light_gray)
background.set_alpha(75)

screen = pygame.display.set_mode((1280, 720))

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

# main menu function controls, the other functions
def end_screen(display):
    paused = True
    while paused:
        display.blit(background, (0,0))
        display.blit(background1, (200,250))
        menumouseposition = pygame.mouse.get_pos()

        MENUtext = get_font(50).render("CONGRATULATIONS", True, "#b68f40")
        MENUrect = MENUtext.get_rect(center=(640, 200))
        screen.blit(MENUtext, MENUrect)
# creating the buttons
        ShopButton = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(950, 650),
                            text_input="Continue to shop", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        MainMenuButton = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(240, 50),
                            text_input="Exit to menu", font=get_font(35), base_color="#d7fcd4", hovering_color="White")

        # display Statistics

        statstext = get_font(35).render("Statistics:", True, "#2debae")
        statsrect = statstext.get_rect(center=(650, 300))
        screen.blit(statstext, statsrect)

# putting the button on the screen and making it change color if hovered over

        for button in [ShopButton, MainMenuButton]:
            button.changeColor(menumouseposition)
            button.update(screen)

# Running through all the events to see if a button was clicked then run a function if something was clicked

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ShopButton.checkForInput(menumouseposition):
                    print("test")
                    pass#shop function
                if MainMenuButton.checkForInput(menumouseposition):
                    main_menu(screen, screen.get_size())
        pygame.display.update()
end_screen(screen)