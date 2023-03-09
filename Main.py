import pygame
from pygame import mixer
import math
from Procedural_Generator import ProceduralGenerator
from Classes import Player
#sets up pygame and mixer
pygame.init()
mixer.init()

#sets up temp background music
mixer.music.load('Music/Character_Menu.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.10)



ScreenLength = 1870
ScreenWidth = 1030

#sets up the generator class with tile size
generator = ProceduralGenerator(int(ScreenLength / 10), int(ScreenWidth / 10))

#generates map
generator.Generate(5, 10, 30, 5, True, 50, 10, 2, None, 1, 2, 5, 25)

#inits player
player = Player((generator.startloc[0][0], generator.startloc[0][1]))

# Set up the drawing window
screen = pygame.display.set_mode([ScreenLength, ScreenWidth])
map = pygame.Surface((ScreenLength, ScreenWidth))
pygame.display.set_caption('The Lost Dungeon')

screen.fill((0, 0, 0))
obstructions = []

#draws map
map = generator.DrawMap(map, obstructions)

#hides mouse
pygame.mouse.set_visible(False)
#loads image
direction_indicator = pygame.transform.scale_by(pygame.image.load("Art/Character/Direction-Temp.png"), 1 / 6).convert()
direction_indicator.set_colorkey((255,255,255))
direction_indicator_rect = direction_indicator.get_rect(center= (ScreenLength/2, ScreenWidth/2))

# Run until the user asks to quit
running = True

#sets up main verables
camera_X = 0 - generator.startloc[0][0] * 5 + ScreenLength / 2 - 10
camera_Y = 0 - generator.startloc[0][1] * 5 + ScreenWidth / 2 - 10
cameraSpeed = 1
mapsize = map.get_size()
newsize = (mapsize[0] * 5, mapsize[1] * 5)
BIGmap = pygame.transform.scale(map, newsize)
mapopen = False
screen.blit(BIGmap, (camera_X, camera_Y))
moveTime = 1
maptriggered = False
playerLocation = [generator.startloc[0][0], generator.startloc[0][1]]
updateScreen = True
angle = 0
skipmousecheck = False

while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #if key goes up
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_m:
                maptriggered = False
        elif event.type == pygame.KEYDOWN:
            #if user presses M open map
            if event.key == pygame.K_m:
                if mapopen and not maptriggered:
                    mapopen = False
                elif not mapopen:
                    mapopen = True
            elif event.key == pygame.K_ESCAPE:
                running = False


        #if player moves the mouse calculate new angle for the direction indicator
        elif event.type == pygame.MOUSEMOTION and not skipmousecheck:
            mouse_x, mouse_y = event.pos
            mouse_rel_x, mouse_rel_y = event.rel
            print(event.rel)
            if abs(mouse_rel_x) > abs(mouse_rel_y):
                angle += math.ceil(mouse_rel_x/5)

            else:
                angle += math.ceil(mouse_rel_y/5)

    #gets all keys and does movment for the player.
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        if not player.Checkcollisions(obstructions):
            camera_X += cameraSpeed
            playerLocation[0] -= cameraSpeed / 5
        else:
            movement = player.MoveFromWall(cameraSpeed, camera_X, camera_Y, playerLocation)
            camera_X = movement[0]
            camera_Y = movement[1]
        # playerLocation = player.MoveLeft(moveTime, (ScreenLength,ScreenWidth))
        # moveTime +=1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        if not player.Checkcollisions(obstructions):
            camera_X -= cameraSpeed
            playerLocation[0] += cameraSpeed / 5
            updateScreen = True
        else:
            movement = player.MoveFromWall(cameraSpeed, camera_X, camera_Y, playerLocation)
            camera_X = movement[0]
            camera_Y = movement[1]

        # playerLocation = player.MoveRight(moveTime, (ScreenLength, ScreenWidth))
        # moveTime += 1
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        if not player.Checkcollisions(obstructions):
            camera_Y += cameraSpeed
            playerLocation[1] -= cameraSpeed / 5
        else:
            movement = player.MoveFromWall(cameraSpeed, camera_X, camera_Y, playerLocation)
            camera_X = movement[0]
            camera_Y = movement[1]

        # playerLocation = player.MoveUp(moveTime, (ScreenLength, ScreenWidth))
        # moveTime += 1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        if not player.Checkcollisions(obstructions):
            camera_Y -= cameraSpeed
            playerLocation[1] += cameraSpeed / 5
        else:
            movement = player.MoveFromWall(cameraSpeed, camera_X, camera_Y, playerLocation)
            camera_X = movement[0]
            camera_Y = movement[1]

        # playerLocation = player.MoveDown(moveTime, (ScreenLength, ScreenWidth))
        # moveTime += 1
        # print(moveTime)
        # print(playerLocation)
    if playerLocation == (ScreenLength / 2 - 25, ScreenWidth / 2 - 25):
        moveTime = 1

    #rotates direction indicator based off angle
    direction_indicator_rotated = pygame.transform.rotate(direction_indicator, -angle)
    rect = direction_indicator_rotated.get_rect(center=direction_indicator_rect.center)

    # Fill the background with white
    screen.fill((0, 0, 0))
    #if map is closed draw game window to screen
    if not mapopen:
        screen.blit(BIGmap, (camera_X, camera_Y))
        screen.blit(player.image, (ScreenLength / 2 - 10, ScreenWidth / 2 - 10))
        screen.blit(direction_indicator_rotated, rect)
    #otherwise draw map
    else:
        screen.blit(map, (0, 0))
        screen.blit(player.tinyimage, playerLocation)

    #updates playerlocation
    player.rect.x = playerLocation[0]
    player.rect.y = playerLocation[1]
    # Flip the display
    pygame.display.flip()
    #if mouse leaves screen teleport it back to center
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_x < 100 or mouse_x > ScreenLength-100 or mouse_y < 100 or mouse_y > ScreenWidth-100:
        skipmousecheck = True
        pygame.mouse.set_pos(ScreenLength/2, ScreenWidth/2)
    else:
        skipmousecheck = False

# Done! Time to quit.
pygame.quit()
