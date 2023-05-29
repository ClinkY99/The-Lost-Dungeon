import pygame, sys
from Interactables import Button
pygame.init()


#UNUSED ALL OF THIS
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

screen = pygame.display.set_mode((1280, 720))

# settings functions with all teh setting controls
def settings(display,size):
    settings = True

    while settings:
        playmouseposition = pygame.mouse.get_pos()

        display.fill("blue")

        PLAYtext = get_font(45).render("This is the Settings screen.", True, "White")
        PLAYrect = PLAYtext.get_rect(center=(size[0]/2, 100))
        display.blit(PLAYtext,PLAYrect)

        playback = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="turquoise")

        playback.changeColor(playmouseposition)
        playback.update(display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playback.checkForInput(playmouseposition):
                    settings = False

        pygame.display.update()