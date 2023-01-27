import pygame
from Procedural_Generator import ProceduralGenerator

pygame.init()

ScreenLength = 1870
ScreenWidth = 1030

generator = ProceduralGenerator(int(ScreenLength/10), int(ScreenWidth/10), 50)

generator.Generate(20, 10, 25,50, True, 50, 10, 2, None, 2)


# Set up the drawing window
screen = pygame.display.set_mode([ScreenLength, ScreenWidth])
map = pygame.Surface((ScreenLength,ScreenWidth))
pygame.display.set_caption('The Lost Dungeon')

screen.fill((0, 0, 0))

# Draw a solid blue circle in the center
tile = pygame.Surface((10, 10))
wall = pygame.Surface((5, 10))
corner = pygame.Surface((5,5))
start = pygame.Surface((20,20))
enemytile = pygame.Surface((10,10))
enemytile.fill((210,150,75))
start.fill((0,0,100))
corner.fill((127,127,127))
wall.fill((127,127,127))
tile.fill((255,255,255))
for x in range(len(generator.map)):
    for y in range(len(generator.map[x])):
        if generator.map[x][y].Active:
            if generator.map[x][y].enemys:
                map.blit(enemytile, (x*10, y*10))
            else:
                map.blit(tile, (x*10, y*10))
        if generator.map[x][y].wall[1]:
            map.blit(wall, ((x*10)+10, y*10))
        if generator.map[x][y].wall[3]:
            map.blit(wall, ((x*10)-5, y*10))
        rotatedwall = pygame.transform.rotate(wall, 270)
        if generator.map[x][y].wall[0]:
            map.blit(rotatedwall, (x*10, (y*10)-5))
        if generator.map[x][y].wall[2]:
            map.blit(rotatedwall, (x*10, (y*10)+10))
        if generator.map[x][y].corner[0]:
            map.blit(corner, ((x*10)-5,(y*10)-5))
        if generator.map[x][y].corner[1]:
            map.blit(corner, ((x*10)+10,(y*10)-5))
        if generator.map[x][y].corner[2]:
            map.blit(corner, ((x*10)+10, (y*10)+10))
        if generator.map[x][y].corner[3]:
            map.blit(corner, ((x*10)-5, (y*10)+10))
map.blit(start, generator.startloc[0])
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