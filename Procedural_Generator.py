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

def GenerateCorridors(Branching, corridorMaxLen, MaxCorridorsPerRoom, SplittingChance, DeadEnds, Generator):
    ConnectedRooms = []
    RoomsToBeProscessed = []
    RoomsToBeProscessedNext = []
    AllRooms = list(Generator.rooms)
    RemainingRooms = list(AllRooms)
    StartRoom = RemainingRooms[random.randrange(0, len(RemainingRooms)-1)]
    RoomsToBeProscessed.append(StartRoom)
    Generating = True
    while Generating:
        print(ConnectedRooms)
        for i in RoomsToBeProscessed:
            #sets possibleRooms to be sorted remaining rooms, Possible rooms is just a reusable variable
            PossibleRooms = sorted(RemainingRooms, key=itemgetter(1))
            try:
                PossibleRooms.remove(i)
            except Exception:
                pass

            for x in range(0, random.randrange(1, MaxCorridorsPerRoom+1)):
                print(x)
                Corridor = SpawnCorridor(i, PossibleRooms, corridorMaxLen, Generator)
                PossibleRooms = Corridor[1]
                roomindex = AllRooms.index(i)
                AllRooms[roomindex][4] += 1
                AllRooms[AllRooms.index(Corridor[0])][4]+= 1
                if Corridor[0] not in ConnectedRooms:
                    ConnectedRooms.append(Corridor[0])
                if not AllRooms[AllRooms.index(Corridor[0])][4] >MaxCorridorsPerRoom:
                    del RemainingRooms[RemainingRooms.index(Corridor[0])]

                else:
                    if AllRooms[AllRooms.index(Corridor[0])][3]:
                        RoomsToBeProscessedNext.append(Corridor[0])
                
            
            AllRooms[AllRooms.index(i)][3] = True
            if AllRooms[AllRooms.index(i)][4] > MaxCorridorsPerRoom:
                try:
                    RemainingRooms.remove(i)
                except Exception:
                    pass
            if i not in ConnectedRooms:
                ConnectedRooms.append(i)
        if len(ConnectedRooms) == len(Generator.rooms):
            Generating = False
        RoomsToBeProscessed = list(RoomsToBeProscessedNext)
        RoomsToBeProscessedNext = []
        if RoomsToBeProscessed == []:
            RoomsLeftForPicking = list(map(itemgetter(1), ConnectedRooms))
            if len(RemainingRooms) > 1:
                RoomsToBeProscessed.append(Functions.ClosestRooms(RemainingRooms[random.randrange(0, len(RemainingRooms)-1)][1], RoomsLeftForPicking, 5, ConnectedRooms))
            elif len(RemainingRooms) == 1:
                RoomsToBeProscessed.append(Functions.ClosestRooms(RemainingRooms[0][1],RoomsLeftForPicking, 5, ConnectedRooms))
            else:
                Generating = False
        print('break')




def SpawnCorridor(StartRoom, RemainingRooms, corridorMaxLen, generator):
    closerooms = []
    tiles = []
    #gets top left location of all rooms
    RoomsLeftForPicking = list(map(itemgetter(1), RemainingRooms))
    Endroom = Functions.ClosestRooms(StartRoom[1], RoomsLeftForPicking, 5, RemainingRooms)
    print(Endroom)
    EndroomLoc = Endroom[2][random.randrange(0, len(Endroom[2])-1)]
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

    roomsreturn = list(RemainingRooms)
    roomsreturn.remove(Endroom)
    print(roomsreturn)
    print('Complete')
    return Endroom, roomsreturn


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
    def Generate(self, numrooms, roomMin, roomMax, branching, corridormaxlen, splittingchance, MaxCorridorsPerRoom, DeadEnds, Diffuculty):
        for i in range(numrooms):
            self.rooms.append(SpawnRoom(roomMin, roomMax, self.size, self))
        GenerateCorridors(branching, corridormaxlen, MaxCorridorsPerRoom, splittingchance, DeadEnds, self)


