import math
import random, json

import pygame.draw

import Classes
from operator import itemgetter


def DistanceCoordinates(co1, co2):
    # gets distance
    return (co1[0] - co2[0]) ** 2 + (co1[1] - co2[1]) ** 2


def Direction(startroomloc, endroomloc):
    directions = []
    # checks directions up down
    if startroomloc[0] > endroomloc[0]:
        directions.append(3)
    elif startroomloc[0] == endroomloc[0]:
        directions.append(None)
    else:
        directions.append(1)
    # checks direction left right
    if startroomloc[1] > endroomloc[1]:
        directions.append(0)
    elif startroomloc[1] == endroomloc[1]:
        directions.append(None)
    else:
        directions.append(2)
    try:
        directions.remove(None)
    except Exception:
        pass
    try:
        # gets random direction from the 2 returne
        directions = directions[random.randrange(0, 2)]
    except:
        # if only 1 is returned return that 1
        directions = directions[0]
    return directions


def ClosestRooms(BasePoint, RoomsToPick, numoptions, RoomRef):
    closerooms = []
    RoomOptions = list(RoomsToPick)
    # loops through to return the number of options right
    for i in range(0, numoptions):
        # picks closest to startroom
        # if there are rooms left
        if len(RoomOptions) != 0:
            # gets the closest room
            closest = RoomRef[list(map(itemgetter(1), RoomRef)).index(
                min(RoomOptions, key=lambda x: DistanceCoordinates(x, BasePoint)))]
            # removes the closest room to get the next closest room
            RoomOptions.remove(closest[1])
            closerooms.append(closest)
    try:
        # returns one of the random rooms in closerooms
        return closerooms[random.randrange(0, len(closerooms) - 1)]
    except Exception:
        try:
            return closerooms[0]
        except:
            return False


def WallCheck(generator, coord):
    walls = [False, False, False, False]
    # checks if wall is needed up
    try:
        if not generator.map[coord[0]][coord[1] - 1].Active:
            walls[0] = Classes.wall(coord[0] * 10, (coord[1] * 10) - 5, 10, 5)
    except:
        walls[0] = Classes.wall(coord[0] * 10, (coord[1] * 10) - 5, 10, 5)
    # checks if wall is needed right
    try:
        if not generator.map[coord[0] + 1][coord[1]].Active:
            walls[1] = Classes.wall((coord[0] * 10) + 10, coord[1] * 10, 5, 10)
    except:
        walls[1] = Classes.wall((coord[0] * 10) + 10, coord[1] * 10, 5, 10)
    # checks if wall is needed down
    try:
        if not generator.map[coord[0]][coord[1] + 1].Active:
            walls[2] = Classes.wall(coord[0] * 10, (coord[1] * 10) + 10, 10, 5)
    except:
        walls[2] = Classes.wall(coord[0] * 10, (coord[1] * 10) + 10, 10, 5)
    # checks if wall is needed left
    try:
        if not generator.map[coord[0] - 1][coord[1]].Active:
            walls[3] = Classes.wall((coord[0] * 10) - 5, coord[1] * 10, 5, 10)
    except:
        walls[3] = Classes.wall((coord[0] * 10) - 5, coord[1] * 10, 5, 10)
    for i in walls:
        if i:
            generator.edgerooms.append(coord)
    return walls


def OverlapLine(distance, angle, startpoint, damgables, size):
    angle = math.radians(angle-135)
    endpoint = (startpoint[0] + (distance * math.cos(angle)), startpoint[1] + (distance * math.sin(angle)))
    line = pygame.draw.line(pygame.Surface(size), (0,255,0), startpoint, endpoint)
    overlaps = []
    for i in damgables.sprites():
        if line.colliderect(i.overlaprect):
            if i.overlaprect.clipline(startpoint, endpoint):
                overlaps.append(i)
    return overlaps

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def SaveGame(player):
    file = open('./Saves/Save.Dungeon')
    jsonfile = json.load(file)
    file.close()

    file = open('./Saves/Save.Dungeon', 'w')

    Savedata = jsonfile['Saves'][player.name]

    Savedata['Level'] = player.levelnum
    Savedata['Player Data']['coins'] = player.money
    Savedata['Player Data']['health'] = player.health
    Savedata['Player Data']['score'] = player.XP
    Savedata['Player Data']['items'] = [i.name for i in player.items]

    jsonfile['Saves'][player.name] = Savedata

    json.dump(jsonfile, file, indent= 4)

def FTB(screen, length):
    black = pygame.Surface(screen.get_size())
    black.fill((0,0,0))

    pygame.mixer.music.fadeout(length*3)

    for i in range(1, length):
        black.set_alpha(i/(250/length))
        screen.blit(black, (0,0))
        pygame.display.update()