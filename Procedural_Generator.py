import random
import pygame
import Functions
from operator import itemgetter

def SpawnRoom(roomMin, roomMax, size, generator):
    #generates extents of rooms
    roomsize = (random.randrange(roomMin,roomMax), random.randrange(roomMin,roomMax))
    #picks location on grid
    locationtopleft = (random.randrange(0, size[0]-roomsize[0]), random.randrange(0, size[1]-roomsize[1]))
    tiles = []
    #loops through all room tiles and adds to grid
    for x in range(locationtopleft[0], locationtopleft[0] + roomsize[0]):
        for y in range(locationtopleft[1], locationtopleft[1] + roomsize[1]):
            generator.map[x][y] = True
            tiles.append((x,y))
    room = [roomsize, locationtopleft, tiles, False, 0]
    return room
# def spawnCorridors(branching, corridormaxlen, splittingchance, deadends, rooms, generator):
#     picking = True
#     while picking:
#         startroom = random.randrange(0,len(rooms)-1)
#         choosing = True
#         count = 0
#         while choosing:
#             endroom = random.randrange(0, len(rooms) - 1)
#
#             if rooms[endroom][5] == 0:
#                 choosing = False
#             elif count >= 10:
#                 if rooms[endroom][5] <= 1:
#                     choosing = False
#             elif count >= 20:
#                 if rooms[endroom][5] <= 2:
#                     choosing = False
#             else:
#                 choosing = False
#             count += 1
#         print('count is ')
#         print(count)
#
#         if startroom != endroom:
#             picking = False
#     #0 is top, 1 is right, 2 is bottom, 3 is left
#     directionStart = []
#     startroomloc = rooms[startroom][1]
#     endroomloc = rooms[endroom][2][random.randrange(0, len(rooms[endroom][2]) -1)]
#     chanceofsplitting = splittingchance
#
#     tiles = []
#     if startroomloc[0] > endroomloc[0]:
#         directionStart.append(3)
#     elif startroomloc[0] == endroomloc[0]:
#         directionStart.append(None)
#     else:
#         directionStart.append(1)
#     if startroomloc[1] > endroomloc[1]:
#         directionStart.append(0)
#     elif startroomloc[1] == endroomloc[1]:
#         directionStart.append(None)
#     else:
#         directionStart.append(2)
#     try:
#         directionStart.remove(None)
#     except Exception:
#         pass
#     try:
#         directionStart = directionStart[random.randrange(0, len(directionStart) -1)]
#     except Exception:
#         print(Exception)
#     direction = directionStart
#     startingpoints = []
#     print(direction)
#
#     for x in rooms[startroom][2]:
#         print(rooms[startroom][1][0]+rooms[startroom][0][1]-1)
#         print(x[0])
#         print('break')
#         if directionStart == 0:
#             if x[1] == rooms[startroom][1][1]:
#                 startingpoints.append(x)
#         elif directionStart == 3:
#             if x[0] == rooms[startroom][1][0]:
#                 startingpoints.append(x)
#
#         elif directionStart == 2:
#             if x[1] == rooms[startroom][1][1]+rooms[startroom][0][1]-1:
#                 startingpoints.append(x)
#         else:
#             if x[0] == rooms[startroom][1][0]+rooms[startroom][0][0]-1:
#                 startingpoints.append(x)
#     print(len(startingpoints)-1)
#     startingpoint = startingpoints[random.randrange(0, len(startingpoints)-1)]
#     generationpath = True
#     while generationpath:
#         for i in range(1, random.randrange(2, corridormaxlen)):
#             Newpoint = None
#             if direction == 0:
#                  Newpoint =( startingpoint[0] , startingpoint[1]-i)
#             elif direction == 1:
#                  Newpoint = (startingpoint[0]+i, startingpoint[1])
#             elif direction == 2:
#                 Newpoint = (startingpoint[0], startingpoint[1]+i)
#             else:
#                 Newpoint = (startingpoint[0]-i,startingpoint[1] )
#             try:
#
#                 generator.map[Newpoint[0]][Newpoint[1]] = True
#             except Exception:
#                 pass
#             print(Newpoint)
#             tiles.append(Newpoint)
#         if branching == True:
#             if random.randrange(1, 100) <= chanceofsplitting:
#                 newtiles = GenerateOffshoot(branching, corridormaxlen, chanceofsplitting, deadends, rooms,
#                                             tiles[len(tiles) - 1], direction, generator)
#                 for i in newtiles:
#                     tiles.append(i)
#                 chanceofsplitting -= 10
#
#         print('break')
#         for i in tiles:
#
#             if i in rooms[endroom][2]:
#                 generationpath = False
#                 break
#
#         directionStart = []
#
#         startingpoint = tiles[len(tiles) - 1]
#         print(startingpoint)
#         print(endroomloc)
#
#         if startingpoint[0] > endroomloc[0]:
#             directionStart.append(3)
#             print('left')
#         elif startingpoint[0] == endroomloc[0]:
#             directionStart.append(None)
#         else:
#             directionStart.append(1)
#             print('right')
#         if startingpoint[1] > endroomloc[1]:
#             directionStart.append(0)
#             print('up')
#         elif startingpoint[1] == endroomloc[1]:
#             directionStart.append(None)
#         else:
#             directionStart.append(2)
#             print('down')
#         try:
#             directionStart.remove(None)
#         except Exception:
#             pass
#         try:
#             if direction == 0:
#                 directionStart.remove(2)
#             elif direction == 1:
#                 directionStart.remove(3)
#             elif direction == 2:
#                 directionStart.remove(0)
#             else:
#                 directionStart.remove(1)
#         except Exception:
#             pass
#         try:
#             directionStart = directionStart[random.randrange(0, len(directionStart))]
#         except Exception:
#             pass
#
#         direction = directionStart
#         print(direction)
#         print('break 2')
#
#     print('finished')
#     for i in tiles:
#         for x in rooms:
#             if i in x[2]:
#                 generator.rooms[rooms.index(x)][5] +=1
#
# def GenerateOffshoot(branching, corridormaxlen, splittingchance, deadends, rooms, startingloc, directioncamefrom, generator):
#     tiles = []
#     chanceofsplitting = splittingchance - 25
#     endroom = random.randrange(0, len(rooms) - 1)
#     directionStart = []
#     directionEnd = []
#     endroomloc = None
#     choosing = True
#     count = 0
#     while choosing:
#         endroom = random.randrange(0, len(rooms) - 1)
#
#         if rooms[endroom][5] == 0:
#             choosing = False
#         elif count >= 10:
#             if rooms[endroom][5] <= 1:
#                 choosing = False
#         elif count >= 20:
#             if rooms[endroom][5] <=2:
#                 choosing = False
#         else:
#             choosing = False
#         count+= 1
#     print('count is ')
#     print(count)
#     endroomloc = rooms[endroom][2][random.randrange(0, len(rooms[endroom][2]) - 1)]
#     print('break')
#     print(startingloc)
#     print(endroomloc)
#     if startingloc[0] > endroomloc[0]:
#         directionStart.append(3)
#     elif startingloc[0] == endroomloc[0]:
#         directionStart.append(None)
#     else:
#         directionStart.append(1)
#     if startingloc[1] > endroomloc[1]:
#         directionStart.append(0)
#     elif startingloc[1] == endroomloc[1]:
#         directionStart.append(None)
#     else:
#         directionStart.append(2)
#
#
#     try:
#         directionStart.remove(None)
#     except Exception:
#         pass
#     try:
#         directionStart = directionStart[random.randrange(0,len(directionStart)-1)]
#     except Exception:
#         directionStart = directionStart[0]
#     direction = directionStart
#     generationpath = True
#     newstartloc = startingloc
#     while generationpath:
#         for i in range(1, random.randrange(2, corridormaxlen)):
#
#             Newpoint = None
#             if direction == 0:
#                 Newpoint = (newstartloc[0], newstartloc[1] - i)
#             elif direction == 1:
#                 Newpoint = (newstartloc[0] + i, newstartloc[1])
#             elif direction == 2:
#                 Newpoint = (newstartloc[0], newstartloc[1] + i)
#             else:
#                 Newpoint = (newstartloc[0] - i, newstartloc[1])
#             try:
#
#                 generator.map[Newpoint[0]][Newpoint[1]] = True
#             except Exception:
#                 pass
#             print(Newpoint)
#             tiles.append(Newpoint)
#
#
#         print(tiles)
#         if branching == True:
#             if random.randrange(1, 100) <= chanceofsplitting:
#                 print('split')
#                 newtiles =GenerateOffshoot(branching, corridormaxlen, chanceofsplitting, deadends, rooms, tiles[len(tiles) - 1], direction, generator)
#                 for i in newtiles:
#                     tiles.append(i)
#                 chanceofsplitting -= 10
#         for i in tiles:
#             if i in rooms[endroom][2]:
#                 generationpath = False
#                 break
#         print(len(tiles) - 1)
#         newstartloc = tiles[len(tiles)-1]
#         directionStart = []
#
#         if newstartloc[0] > endroomloc[0]:
#             directionStart.append(3)
#         elif newstartloc[0] == endroomloc[0]:
#             directionStart.append(None)
#         else:
#             directionStart.append(1)
#         if newstartloc[1] > endroomloc[1]:
#             directionStart.append(0)
#         elif newstartloc[1] == endroomloc[1]:
#             directionStart.append(None)
#         else:
#             directionStart.append(2)
#         try:
#               directionStart.remove(None)
#         except Exception:
#             pass
#
#
#         try:
#             directionStart = directionStart[random.randrange(0, len(directionStart))]
#         except Exception:
#             pass
#         direction = directionStart
#     for i in tiles:
#         for x in rooms:
#             if i in x[2]:
#                 generator.rooms[rooms.index(x)][5] +=1
#     return tiles
#
#
#
#

def GenerateCorridors(Branching, corridorMaxLen, MaxCorridorsPerRoom, SplittingChance, DeadEnds, Generator):
    ConnectedRooms = []
    RoomsToBeProscessed = []
    RoomsToBeProscessedNext = []
    AllRooms = Generator.rooms
    RemainingRooms = AllRooms
    StartRoom = RemainingRooms[random.randrange(0, len(RemainingRooms)-1)]
    RoomsToBeProscessed.append(StartRoom)
    Generating = True
    while Generating:
        for i in RoomsToBeProscessed:
            #sets possibleRooms to be sorted remaining rooms, Possible rooms is just a reusable variable
            PossibleRooms = sorted(RemainingRooms, key=itemgetter(1))
            PossibleRooms.remove(i)
            for x in range(1, random.randrange(1, MaxCorridorsPerRoom)):
                Corridor = SpawnCorridor(i, PossibleRooms)
                RoomsToBeProscessed.append(Corridor[0])
                PossibleRooms = Corridor[1]



def SpawnCorridor(StartRoom, RemainingRooms, corridorMaxLen, generator):
    closerooms = []
    tiles = []
    #gets top left location of all rooms
    RoomsLeftForPicking = list(map(itemgetter(1), RemainingRooms))
    PickingClosest = True
    for i in range(0,5):
        #picks closest to startroom
        closest = RemainingRooms[RemainingRooms.index(min(RoomsLeftForPicking, key=lambda x: Functions.DistanceCoordinates(x,StartRoom[1])))]
        RoomsLeftForPicking.remove(closest)
        closerooms.append(closest)
    Endroom = closerooms[random.randrange(0,4)]
    EndroomLoc = Endroom[2][random.randrange(0, len(Endroom[2]))]
    direction = Functions.Direction(StartRoom[1], EndroomLoc)
    startingpoints = []
    for x in StartRoom[2]:
        if direction == 0:
            if x[1] == StartRoom[1][1]:
                startingpoints.append(x)
        elif direction == 3:
            if x[0] == StartRoom[1][0]:
                startingpoints.append(x)

        elif direction == 2:
            if x[1] == StartRoom[1][1]+StartRoom[0][1]-1:
                startingpoints.append(x)
        else:
            if x[0] == StartRoom[1][0]+StartRoom[0][0]-1:
                startingpoints.append(x)
    startingpoint = startingpoints[random.randrange(0, len(startingpoints)-1)]
    generationPath = True
    while generationPath:
        for i in range(1, random.randrange(2, corridorMaxLen)):
            Newpoint = None
            if direction == 0:
                 Newpoint =( startingpoint[0] , startingpoint[1]-i)
            elif direction == 1:
                 Newpoint = (startingpoint[0]+i, startingpoint[1])
            elif direction == 2:
                Newpoint = (startingpoint[0], startingpoint[1]+i)
            else:
                Newpoint = (startingpoint[0]-i,startingpoint[1] )
            try:
                generator.map[Newpoint[0]][Newpoint[1]] = True
                tiles.append(Newpoint)
            except Exception:
                pass
            if Newpoint[0] == EndroomLoc[0] or Newpoint[1] == EndroomLoc[1]:
                break
    for i in tiles:
        if i in Endroom[2]:
            generationPath = False
            break
    startingpoint = tiles[len(tiles) - 1]
    direction = Functions.Direction(startingpoint,EndroomLoc)



class ProceduralGenerator():
    #init function, sets up all variables
    def __init__(self,length, width,seed):
        super(ProceduralGenerator, self).__init__()
        self.size = (length, width)
        self.numrooms = None
        self.roomMax = None
        self.roomMin = None
        self.rooms = []
        self.branching = None
        self.corridormaxlen = None
        self.splittingchance = None
        self.DeadEnds = None
        self.Corridors = []
        self.Diffuculty = None
        self.map = []
        #creates grid
        for x in range(length):
            new_row = []
            for i in range(width):
                new_row.append(False)
            self.map.append(new_row)
        #if no imputed seed create seed
        if seed == None:
            random.seed()
        #if imputed seed init seed
        else:
            random.seed(seed)

    #generate function
    def Generate(self, numrooms, roomMin, roomMax, branching, corridormaxlen, splittingchance, corridordecay, DeadEnds, Diffuculty):
        for i in range(numrooms):
            self.rooms.append(SpawnRoom(roomMin, roomMax, self.size, self))
        generatingcorridors = True
        corridorchance = 100
        # while generatingcorridors:
        #     if random.randrange(1,100) <= corridorchance:
        #         spawnCorridors(branching ,corridormaxlen, splittingchance, DeadEnds, self.rooms, self)
        #         corridorchance -= corridordecay
        #     else:
        #         generatingcorridors = False


