import pygame
pygame.init()
display=pygame.display.set_mode((500, 600))
clock= pygame.time.Clock()

FPS=50
screen = pygame.display.set_mode((1280, 720))

background = pygame.image.load("assets/Hotpot-2.png")
PLAYtext = get_font(45).render("DARKEST DUNGEON.", True, "White")

DEFAULT_IMAGE_SIZE = (1280, 720)
background = pygame.transform.scale(background, DEFAULT_IMAGE_SIZE)
screen.blit(background, (0, 0))

def game():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pygame.display.update()
        clock.tick(FPS)
game()
pygame.quit()
