import pygame
from Procedural_Generator import ProceduralGenerator

pygame.init()

ScreenLength = 1870
ScreenWidth = 1030

generator = ProceduralGenerator(int(ScreenLength/10), int(ScreenWidth/10))

generator.Generate(5, 10, 30,5 ,True, 50, 10, 2, None, 1,2, 5, 25)


# Set up the drawing window
screen = pygame.display.set_mode([ScreenLength, ScreenWidth])
map = pygame.Surface((ScreenLength,ScreenWidth))
pygame.display.set_caption('The Lost Dungeon')

screen.fill((0, 0, 0))
map = generator.DrawMap(map)
screen.blit(map, (0,0))


# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white





    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()