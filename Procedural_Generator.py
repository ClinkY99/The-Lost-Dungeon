import random
import pygame
import Functions
from operator import itemgetter
from Classes import Tile

def SpawnRoom(roomMin, roomMax, size, generator):
    #generates extents of rooms
    roomsize = (random.randrange(roomMin,roomMax), random.randrange(roomMin,roomMax))
    #picks location on grid
    locationtopleft = (random.randrange(0, size[0]-roomsize[0]), random.randrange(0, size[1]-roomsize[1]))
    tiles = []
    #loops through all room tiles and adds to grid
    for x in range(locationtopleft[0], locationtopleft[0] + roomsize[0]):
        for y in range(locationtopleft[1], locationtopleft[1] + roomsize[1]):
            generator.map[x][y].Active = True
            tiles.append((x,y))
    room = [roomsize, locationtopleft, tiles, False, 0]
    return room

def GenerateCorridors(Branching, corridorMaxLen, MaxCorridorsPerRoom, SplittingChance, DeadEnds, Generator):
    #Sets Up Variables for Generating corridors
    ConnectedRooms = []
    RoomsToBeProscessed = []
    RoomsToBeProscessedNext = []
    AllRooms = list(Generator.rooms)
    RemainingRooms = list(AllRooms)
    StartRoom = RemainingRooms[random.randrange(0, len(RemainingRooms)-1)]
    RoomsToBeProscessed.append(StartRoom)
    #sets up generation loop
    Generating = True
    while Generating:
        #loops through all rooms needing to be proscessed
        for i in RoomsToBeProscessed:
            #sets possibleRooms to be sorted remaining rooms, Possible rooms is just a reusable variable
            PossibleRooms = sorted(RemainingRooms, key=itemgetter(1))
            #tries to remove i from possible rooms so it cant go to itself, if it isnt in possible rooms, it will be ignored
            try:
                PossibleRooms.remove(i)
            except Exception:
                pass
            #creates random amount of corridors per room based off maxcorridors
            for x in range(0, random.randrange(1, MaxCorridorsPerRoom+1)):
                #calls spawnCorridor and sets Corrdor to be the returned output
                Corridor = SpawnCorridor(i, PossibleRooms, corridorMaxLen, Generator)
                if Corridor == False:
                    Generating = False
                    break
                #sets possible rooms to be everything - the rooms it went too
                PossibleRooms = Corridor[1]
                #gets the index of the starting room
                roomindex = AllRooms.index(i)
                #increses the connections to rooms by 1
                AllRooms[roomindex][4] += 1
                AllRooms[AllRooms.index(Corridor[0])][4]+= 1
                #adds to Connected rooms unless it is already there
                if Corridor[0] not in ConnectedRooms:
                    ConnectedRooms.append(Corridor[0])
                #checks if it has more connections than max connections to room, if so deletes it, if not it gets added to rooms to be proscessed next
                if not AllRooms[AllRooms.index(Corridor[0])][4] >MaxCorridorsPerRoom:
                    del RemainingRooms[RemainingRooms.index(Corridor[0])]

                else:
                    if AllRooms[AllRooms.index(Corridor[0])][3]:
                        RoomsToBeProscessedNext.append(Corridor[0])
                
            #sets it to have been generated from
            AllRooms[AllRooms.index(i)][3] = True
            if AllRooms[AllRooms.index(i)][4] > MaxCorridorsPerRoom:
                try:
                    RemainingRooms.remove(i)
                except Exception:
                    pass
            if i not in ConnectedRooms:
                ConnectedRooms.append(i)
        #if Connected Rooms is the same length as all rooms stop generating
        if len(ConnectedRooms) == len(Generator.rooms):
            Generating = False
        #sets rooms to be proscessed to = the list of the
        RoomsToBeProscessed = list(RoomsToBeProscessedNext)
        RoomsToBeProscessedNext = []
        #if rooms to be proscessed next is empty
        if RoomsToBeProscessed == []:
            RoomsLeftForPicking = list(map(itemgetter(1), ConnectedRooms))
            #if Remaining rooms is less than 1 find the pick a new start room
            if len(RemainingRooms) > 1:
                RoomsToBeProscessed.append(Functions.ClosestRooms(RemainingRooms[random.randrange(0, len(RemainingRooms)-1)][1], RoomsLeftForPicking, 5, ConnectedRooms))
            #if ReamainingRooms is 1 pick a new start room to connect to it
            elif len(RemainingRooms) == 1:
                RoomsToBeProscessed.append(Functions.ClosestRooms(RemainingRooms[0][1],RoomsLeftForPicking, 5, ConnectedRooms))
            #otherwise stop generatiing
            else:
                Generating = False




def SpawnCorridor(StartRoom, RemainingRooms, corridorMaxLen, generator):
    closerooms = []
    tiles = []
    #gets top left location of all rooms
    RoomsLeftForPicking = list(map(itemgetter(1), RemainingRooms))
    #set endrom to be the closest room to start room
    Endroom = Functions.ClosestRooms(StartRoom[1], RoomsLeftForPicking, 5, RemainingRooms)
    #if it cant find end room break out
    if(Endroom == False):
        return False
    #set end room loc to be a random tile in end room
    EndroomLoc = Endroom[2][random.randrange(0, len(Endroom[2])-1)]
    #gets direction to head
    direction = Functions.Direction(StartRoom[1], EndroomLoc)
    #picks starting points
    startingpoints = []
    #loops through tiles in start room
    for x in StartRoom[2]:
        #if the direction is up and the tile is on the top add it to start rooms
        if direction == 0:
            if x[1] == StartRoom[1][1]:
                startingpoints.append(x)
        #if direction is left and the tile is on the left add it to start rooms
        elif direction == 3:
            if x[0] == StartRoom[1][0]:
                startingpoints.append(x)
        #if direction is down and start room is on the bottom add it to start room
        elif direction == 2:
            if x[1] == StartRoom[1][1]+StartRoom[0][1]-1:
                startingpoints.append(x)
        #if direction is right and it is on the right add it to start room
        else:
            if x[0] == StartRoom[1][0]+StartRoom[0][0]-1:
                startingpoints.append(x)
    #pick a random start point
    startingpoint = startingpoints[random.randrange(0, len(startingpoints)-1)]
    #start generating
    generationPath = True
    while generationPath:
        #loops through a random range for corridor length
        for i in range(1, random.randrange(2, corridorMaxLen)):
            Newpoint = None
            #sets the next tile
            if direction == 0:
                 Newpoint =(startingpoint[0] , startingpoint[1]-i)
            elif direction == 1:
                 Newpoint = (startingpoint[0]+i, startingpoint[1])
            elif direction == 2:
                Newpoint = (startingpoint[0], startingpoint[1]+i)
            else:
                Newpoint = (startingpoint[0]-i,startingpoint[1] )
            try:
                #sets tile to be active
                generator.map[Newpoint[0]][Newpoint[1]].Active = True
                tiles.append(Newpoint)
            except Exception:
                break
            if Newpoint[0] == EndroomLoc[0] or Newpoint[1] == EndroomLoc[1]:
                break

        #checks if cooridor overlaps with corridors
        for i in tiles:
            if i in Endroom[2]:
                generationPath = False
                break
        #gets new starting point
        startingpoint = tiles[len(tiles) - 1]
        #gets new direction
        direction = Functions.Direction(startingpoint,EndroomLoc)
    #rooms left
    roomsreturn = list(RemainingRooms)
    roomsreturn.remove(Endroom)
    #returns the end room
    return Endroom, roomsreturn

def SpawnWalls(generator):
    #loops through all tiles
    for i in generator.map:
        for x in i:
            #checks if x is active
            if x.Active:
                #gets the coords of the tile
                coord = generator.map.index(i) ,i.index(x)
                #checks where to put walls
                walls = Functions.WallCheck(generator, coord)
                #sets walls to be the return of the function
                generator.map[coord[0]][coord[1]].wall = list(walls)
                #checks for the cooridors are needed in all 4 directions
                if walls[0] and walls[1]:
                    generator.map[coord[0]][coord[1]].corner[1] = True
                if walls[1] and walls[2]:
                    generator.map[coord[0]][coord[1]].corner[2] = True
                if walls[2] and walls[3]:
                    generator.map[coord[0]][coord[1]].corner[3] = True
                if walls[3] and walls[0]:
                    generator.map[coord[0]][coord[1]].corner[0] = True



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
                new_row.append(Tile())
            self.map.append(new_row)
        #if no imputed seed create seed
        if seed == None:
            random.seed()
        #if imputed seed init seed
        else:
            random.seed(seed)

    #generate function
    def Generate(self, numrooms, roomMin, roomMax, branching, corridormaxlen, splittingchance, MaxCorridorsPerRoom, DeadEnds, Diffuculty):
        print('Generating Rooms')
        for i in range(numrooms):
            self.rooms.append(SpawnRoom(roomMin, roomMax, self.size, self))
        print('Generating Corridors')
        GenerateCorridors(branching, corridormaxlen, MaxCorridorsPerRoom, splittingchance, DeadEnds, self)
        print('Generating Walls')
        SpawnWalls(self)


