import random
from operator import itemgetter
def DistanceCoordinates(co1, co2):
    return (co1[0]- co2[0])**2 + (co1[1]-co2[1])**2
def Direction(startroomloc, endroomloc):
    directions = []
    if startroomloc[0] > endroomloc[0]:
       directions.append(3)
    elif startroomloc[0] == endroomloc[0]:
        directions.append(None)
    else:
        directions.append(1)
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
    print(directions)
    try:
        directions = directions[random.randrange(0, 1)]
    except:
        directions = directions[0]
    return directions
def ClosestRooms(BasePoint, RoomsToPick, numoptions, RoomRef):
    closerooms = []
    RoomOptions = list(RoomsToPick)
    for i in range(0, numoptions):
        # picks closest to startroom
        if len(RoomOptions) != 0:
            closest = RoomRef[list(map(itemgetter(1), RoomRef)).index(min(RoomOptions, key=lambda x: DistanceCoordinates(x, BasePoint)))]
            RoomOptions.remove(closest[1])
            closerooms.append(closest)
    try:
        return closerooms[random.randrange(0,len(closerooms)-1)]
    except:
        return closerooms[0]
