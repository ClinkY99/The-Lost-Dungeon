import pygame
from Procedural_Generator import ProceduralGenerator

pygame.init()

ScreenLength = 1800
ScreenWidth = 720

generator = ProceduralGenerator(int(ScreenLength/10), int(ScreenWidth/10), 50)

generator.Generate(50, 2, 10, True, 1, 25, 5, None, None)

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

    for x in range(len(generator.map)):
        for y in range(len(generator.map[x])):
            if generator.map[x][y]:
                screen.blit(tile, (x*10, y*10))


    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()