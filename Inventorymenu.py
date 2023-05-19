import pygame, sys
from mainmenu import main_menu
from button import Button
pygame.init()

num=90 #the coin function
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Inventory Menu")
background = pygame.Surface((1280, 720))
light_gray = ((84,86,86))
background.fill(light_gray)
background.set_alpha(75)

screen = pygame.display.set_mode((1280, 720))

def settings(display):
    settings = True

    while settings:
        playmouseposition = pygame.mouse.get_pos()

        display.fill("blue")

        PLAYtext = get_font(45).render("This is the Settings screen.", True, "White")
        PLAYrect = PLAYtext.get_rect(center=(640, 260))
        display.blit(PLAYtext,PLAYrect )

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
                    settings = False

        pygame.display.update()

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

# options function controls text, screen, a button clicking
def resume():
    paused = False
    print(paused)
# Level function controls the level button in the options screen

# main menu function controls, the other functions
def Pause_menu(display):
    paused = True
    while paused:
        display.blit(background, (0,0))

        menumouseposition = pygame.mouse.get_pos()

        MENUtext = get_font(50).render("INVENTORY MENU", True, "#b68f40")
        MENUrect = MENUtext.get_rect(center=(640, 150))

# displaying the buttons on the main menu
        resumebutton = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(150, 60),
                            text_input="Continue", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        magicbutton = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(250, 60),
                              text_input="Magic", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        consumablesbutton = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(350, 60),
                              text_input="Consumables", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        armorbutton = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(450, 60),
                              text_input="Armor", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        weaponsbutton = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(550, 60),
                              text_input="Weapons", font=get_font(35), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENUtext, MENUrect)

        for button in [resumebutton, magicbutton,consumablesbutton, armorbutton,  weaponsbutton ]:
            button.changeColor(menumouseposition)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resumebutton.checkForInput(menumouseposition):
                    paused = False

        pygame.display.update()
Pause_menu(screen)