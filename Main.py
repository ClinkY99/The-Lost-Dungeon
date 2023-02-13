import pygame
from Procedural_Generator import ProceduralGenerator

pygame.init()

ScreenLength = 1870
ScreenWidth = 1030

generator = ProceduralGenerator(int(ScreenLength/10), int(ScreenWidth/10), 50)

generator.Generate(5, 10, 30,5 ,True, 50, 10, 2, None, 1,2, 5, 25)


# Set up the drawing window
screen = pygame.display.set_mode([ScreenLength, ScreenWidth])
map = pygame.Surface((ScreenLength,ScreenWidth))
pygame.display.set_caption('The Lost Dungeon')

screen.fill((0, 0, 0))
map = generator.DrawMap(map)


# Run until the user asks to quit
running = True
inputed = int(input('input 0 for overhead map view, input 1 for test moving map with WASD keys '))
if inputed == 0:

    screen.blit(map, (0, 0))
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white

        # Flip the display
        pygame.display.flip()
else:
    camera_X = 0-generator.startloc[0][0]*5 + ScreenLength/2-25
    camera_Y = 0-generator.startloc[0][1]*5 + ScreenWidth/2-25
    cameraSpeed = 5
    mapsize = map.get_size()
    newsize = (mapsize[0] *5, mapsize[1]*5)
    map = pygame.transform.scale(map, newsize)

    screen.blit(map,(camera_X, camera_Y))
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            camera_X += cameraSpeed
        if keys[pygame.K_RIGHT]:
            camera_X -= cameraSpeed
        if keys[pygame.K_UP]:
            camera_Y += cameraSpeed
        if keys[pygame.K_DOWN]:
            camera_Y -= cameraSpeed

        # Fill the background with white
        screen.fill((0,0,0))

        screen.blit(map, (camera_X,camera_Y))
        # Flip the display
        pygame.display.flip()

# Done! Time to quit.
pygame.quit()