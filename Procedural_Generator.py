import random
import pygame
import Functions
from operator import itemgetter
from Classes import Tile, EnemySpawn
import Classes
import math
def SpawnRoom(roomMin, roomMax, distancebetween, size, generator):
    #generates room size
    roomsize = (random.randrange(roomMin,roomMax), random.randrange(roomMin,roomMax))
    searching = True
    while searching:
        #if it is the first room pick anywhere on the grid
        if len(generator.rooms) == 0:
            locationtopleft = (int((size[0]-roomsize[0])/2), int((size[1]-roomsize[1])/2))
            searching = False
        else:
            try:
                generateoff = generator.rooms[random.randrange(0, len(generator.rooms)-1)]
            except:
                generateoff = generator.rooms[0]
            #creates a dictionary of all possible locations, remvoes overlap
            Xloc = {
                0:random.randrange(generateoff[1][0]-distancebetween-roomsize[0], generateoff[1][0]+2-roomsize[0]),
                1:random.randrange(generateoff[1][0]+generateoff[0][0] -2 ,generateoff[1][0] + distancebetween +generateoff[0][0])
            }
            YLoc = {
                0:random.randrange(generateoff[1][1]-distancebetween-roomsize[1], generateoff[1][1]+2-roomsize[1]),
                1:random.randrange(generateoff[1][1] + generateoff[0][1] - 2 ,generateoff[1][1] + generateoff[0][1]+roomsize[1]+distancebetween)
            }
            #picks one of the 2 items in the dictonary
            locationtopleft = (Xloc[random.randrange(0,2)], YLoc[random.randrange(0,2)])
            #if it is outside of the screen. or is in the start room
            if locationtopleft[0] <0 or locationtopleft[0] >size[0] -roomsize[0] or locationtopleft[1] < 0 or locationtopleft[1] > size[1] - roomsize[1]:
                searching = True
            elif locationtopleft in generateoff[2]:
                searching = True
            else:
                searching = False
    tiles = []
    #creates all tiles
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
    inline = [False,False]
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
                if not inline[0] and Newpoint[0] == EndroomLoc[0]:
                    inline[0] = True
                    print('break')
                    break
                if not inline[1] and Newpoint[1] == EndroomLoc[1]:
                    print('break')
                    inline[1] = True
                    break
            except Exception:
                break


        print('test')
        #checks if cooridor overlaps with corridors
        for i in tiles:
            if i in Endroom[2]:
                print('found')
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
                try:
                    if walls[0] and walls[1] and generator.map[coord[0]+1][coord[1]-1]:
                        generator.map[coord[0]][coord[1]].corner[1] = True
                except:
                    pass
                try:
                    if walls[1] and walls[2] and generator.map[coord[0]+1][coord[1]+1]:
                        generator.map[coord[0]][coord[1]].corner[2] = True
                except:
                    pass
                try:
                    if walls[2] and walls[3] and generator.map[coord[0]-1][coord[1]+1]:
                        generator.map[coord[0]][coord[1]].corner[3] = True
                except:
                    pass
                try:
                    if walls[3] and walls[0] and generator.map[coord[0]-1][coord[1]-1]:
                        generator.map[coord[0]][coord[1]].corner[0] = True
                except:
                    pass

def choosestart(generator, size):
    #choses the room it is in
    roomin = generator.rooms[random.randrange(0, len(generator.rooms))]
    #picks a tile to spawn the start in
    location = (random.randrange(roomin[1][0], roomin[1][0]+roomin[0][0]-2)*10, random.randrange(roomin[1][1], roomin[1][1]+roomin[0][1]-2)*10)
    return location, roomin

def chooseend(generator):
    rooms = list(generator.rooms)
    rooms.remove(generator.startRoom)
    roomin = rooms[random.randrange(0, len(rooms))]
    # picks a tile to spawn the start in
    location = (random.randrange(roomin[1][0], roomin[1][0] + roomin[0][0] - 2) * 10,
                random.randrange(roomin[1][1], roomin[1][1] + roomin[0][1] - 2) * 10)
    return Classes.Endpoint(location, roomin)
def enemySpawns(diffuculty, generator):
    #gets a list of all rooms
    locationstospawnenemys = list(generator.rooms)
    #removes start room
    locationstospawnenemys.remove(generator.startRoom)
    #loops through a random number based of the diffuculty
    enemys = pygame.sprite.Group()
    for i in range(0, random.randrange(diffuculty*generator.diffucultyincrese*2, diffuculty*generator.diffucultyincrese*5)):
        #if no rooms possible to be spawned in stop the loop
        if len(locationstospawnenemys) == 0:
            break
        #picks the room and the tile and sets it to be a spawnee
        room = list(locationstospawnenemys[random.randrange(0, len(locationstospawnenemys))])
        tile = room[2][random.randrange(0, len(room[2]))]
        generator.map[tile[0]][tile[1]].enemys = True
        try:
            enemys.add(EnemySpawn(random.randrange(1,math.ceil(diffuculty/4)), (tile[0] * 10, tile[1] *10)))
        except:
            enemys.add(EnemySpawn(1, (tile[0] * 10, tile[1] *10)))
    return enemys
def SpawnObjectives(generator, numObjectives, diffuculty):
    Objectives = pygame.sprite.Group()
    rooms = list(generator.rooms)
    rooms.remove(generator.startRoom)
    rooms.remove(generator.endpoint.room)
    for i in range(0, numObjectives):
        Objectives.add(Classes.Objective(poispawnloc(generator, (5,5), rooms), math.ceil(diffuculty/2)))
    return Objectives



def poispawnloc(generator, size, rooms):
    #generates spawn location for POI
    room = list(rooms[random.randrange(0, len(rooms))])
    location = (random.randrange(room[1][0], room[1][0]+room[0][0]-size[0]), random.randrange(room[1][1], room[1][1]+room[0][1]-size[1]))
    return location
def spawnchest(generator, loot, diffuculty):
    #spawns chests
    chests = []
    rooms = list(generator.rooms)
    for i in range(0, random.randrange(1,loot)):
        chests.append((Classes.Treasure(poispawnloc(generator,(6,6),rooms), random.randrange(0,8), math.ceil(diffuculty/4), 4)))
    return chests
def spawnJars(generator, maxjarchance):
    jars = pygame.sprite.Group()
    #spawns jars
    for i in range(random.randrange(1,maxjarchance)):
        location = generator.edgerooms[random.randrange(0,len(generator.edgerooms))]
        jars.add(Classes.Jar(location))
    return jars

class ProceduralGenerator():
    #init function, sets up all variables
    def __init__(self,length, width,seed = None):
        super(ProceduralGenerator, self).__init__()
        self.matrix = None
        self.size = (length-1, width-1)
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
        self.tiles = []
        self.startloc = None
        self.startRoom= None
        self.endpoint = None
        self.enemys = []
        self.Treasure = pygame.sprite.Group()
        self.Jar = pygame.sprite.Group()
        self.Objectives = pygame.sprite.Group()
        self.diffucultyincrese = 2
        self.Objectivesnum = 2
        self.loot = 0
        self.edgerooms = []
        self.jars = pygame.sprite.Group()
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
    def Generate(self, numrooms, roomMin, roomMax, maxdistance, branching, corridormaxlen, splittingchance, MaxCorridorsPerRoom, DeadEnds, Diffuculty, ObjectivesNum, loot, maxjars):
        print('Generating Rooms')
        for i in range(numrooms):
            self.rooms.append(SpawnRoom(roomMin, roomMax, maxdistance, self.size, self))
            self.tiles.append(self.rooms[len(self.rooms)-1][2])
        print('Generating Corridors')
        GenerateCorridors(branching, corridormaxlen, MaxCorridorsPerRoom, splittingchance, DeadEnds, self)
        print('Generating Walls')
        SpawnWalls(self)
        print('Picking Start')
        self.startloc = choosestart(self, self.size)
        self.startRoom = self.startloc[1]
        print('picking end')
        self.endpoint = chooseend(self)
        print('spawning enemys')
        self.enemys = enemySpawns(Diffuculty, self)
        print('creating POIs')
        self.Objectives = (SpawnObjectives(self,ObjectivesNum,Diffuculty))
        self.treasure = spawnchest(self,loot, Diffuculty)
        self.jars = spawnJars(self, maxjars)
        print('Completed Generation')
    def DrawMap(self,map):
        #sets up all Surfaces
        obstructions = pygame.sprite.Group()
        floortile = pygame.Surface((10, 10))
        corner = pygame.Surface((5, 5))
        start = pygame.Surface((20, 20))
        enemytile = pygame.Surface((10, 10))
        enemytile.fill((210, 150, 75))
        start.fill((0, 0, 100))
        corner.fill((127, 127, 127))
        floortile.fill((255, 255, 255))
        wall = pygame.Surface((5,10))
        wall.fill((127,127,127))
        #loops through all tiles in map and if they have walls or tiles draw them on the map surface
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                tile = self.map[x][y]
                if tile.Active:
                    map.blit(floortile, (x * 10, y * 10))
                for i in tile.wall:
                    if i:
                        map.blit(i.image, i.rect)
                        obstructions.add(i)
                if tile.corner[0]:
                    map.blit(corner, ((x * 10) - 5, (y * 10) - 5))
                if tile.corner[1]:
                    map.blit(corner, ((x * 10) + 10, (y * 10) - 5))
                if tile.corner[2]:
                    map.blit(corner, ((x * 10) + 10, (y * 10) + 10))
                if tile.corner[3]:
                    map.blit(corner, ((x * 10) - 5, (y * 10) + 10))
        #loops through all pois and draws them to the map
        obstructions.add(self.jars.sprites())
        #adds start location
        map.blit(start, self.startloc[0])
        map.blit(self.endpoint.image, self.endpoint.drawingrect)
        return map, obstructions

    def DrawChangebles(self, map):
        treasure = pygame.Surface((10, 30))
        treasure.fill((0, 255, 170))
        for jar in self.jars.sprites():
            map.blit(jar.bigself.image, jar.bigself.rect)
        map.set_colorkey((0,0,0))
        self.Objectives.draw(map)
        for i in self.treasure:
            treasurecopy = pygame.transform.rotozoom(treasure, i.direction * 45, 1)
            treasurecopy.set_colorkey((0, 0, 0))
            map.blit(treasurecopy, i.Location)
        return map
