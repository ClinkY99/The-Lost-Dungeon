import random
import pygame


def SpawnRoom(roomMin, roomMax, size, generator):
    roomsize = (random.randrange(roomMin,roomMax), random.randrange(roomMin,roomMax))
    locationtopleft = (random.randrange(0, size[0]-roomsize[0]), random.randrange(0, size[1]-roomsize[1]))
    for i in range(locationtopleft[0], locationtopleft[0] + roomsize[0]):
        for x in range(locationtopleft[1], locationtopleft[1] + roomsize[1]):
            generator.map[i][x] = True


class ProceduralGenerator():
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
        self.Diffuculty = None
        self.map = []
        for x in range(length):
            new_row = []
            for i in range(width):
                new_row.append(False)
            self.map.append(new_row)
        if seed == None:
            random.seed()
        else:
            random.seed(seed)

    def Generate(self, numrooms, roomMin, roomMax, branching, corridormaxlen, splittingchance, DeadEnds, Diffuculty):
        for i in range(numrooms):
            self.rooms.append(SpawnRoom(roomMin, roomMax, self.size, self))




