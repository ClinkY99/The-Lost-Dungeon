import random
from operator import itemgetter
def DistanceCoordinates(co1, co2):
    #gets distance
    return (co1[0]- co2[0])**2 + (co1[1]-co2[1])**2
def Direction(startroomloc, endroomloc):
    directions = []
    #checks directions up down
    if startroomloc[0] > endroomloc[0]:
       directions.append(3)
    elif startroomloc[0] == endroomloc[0]:
        directions.append(None)
    else:
        directions.append(1)
    #checks direction left right
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
        #gets random direction from the 2 returne
        directions = directions[random.randrange(0, 2)]
    except:
        #if only 1 is returned return that 1
        directions = directions[0]
    return directions
def ClosestRooms(BasePoint, RoomsToPick, numoptions, RoomRef):
    closerooms = []
    RoomOptions = list(RoomsToPick)
    #loops through to return the number of options right
    for i in range(0, numoptions):
        # picks closest to startroom
        #if there are rooms left
        if len(RoomOptions) != 0:
            #gets the closest room
            closest = RoomRef[list(map(itemgetter(1), RoomRef)).index(min(RoomOptions, key=lambda x: DistanceCoordinates(x, BasePoint)))]
            #removes the closest room to get the next closest room
            RoomOptions.remove(closest[1])
            closerooms.append(closest)
    try:
        #returns one of the random rooms in closerooms
        return closerooms[random.randrange(0,len(closerooms)-1)]
    except Exception:
        try:
            return closerooms[0]
        except:
            return False
def WallCheck(generator, coord):
    walls = [False,False,False,False]
    #checks if wall is needed up
    try:
        if not generator.map[coord[0]][coord[1] - 1].Active:
            walls[0] = True
    except:
        walls[0] = True
    # checks if wall is needed right
    try:
        if not generator.map[coord[0] + 1][coord[1]].Active:
            walls[1] = True
    except:
        walls[1] = True
    # checks if wall is needed down
    try:
        if not generator.map[coord[0]][coord[1] + 1].Active:
            walls[2] = True
    except:
        walls[2] = True
    # checks if wall is needed left
    try:
        if not generator.map[coord[0] - 1][coord[1]].Active:
            walls[3] = True
    except:
        walls[3] = True
    return walls