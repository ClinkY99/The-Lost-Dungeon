import pygame
from Procedural_Generator import ProceduralGenerator

pygame.init()





ScreenLength = 500
ScreenWidth = 500

generator = ProceduralGenerator(int(ScreenLength/10), int(ScreenWidth/10), 50)

generator.Generate(7, 2, 10, None, None, None, None, None)

# Set up the drawing window
screen = pygame.display.set_mode([ScreenLength, ScreenWidth])

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((0, 0, 0))

    # Draw a solid blue circle in the center
    tile = pygame.Surface((10, 10))
    tile.fill((255,255,255))

    for i in range(len(generator.map)):
        for x in range(len(generator.map[i])):
            if generator.map[i][x]:
                screen.blit(tile, (i*10, x*10))


    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()