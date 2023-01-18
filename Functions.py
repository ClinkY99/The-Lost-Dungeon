import random
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
    try:
        directions = directions[random.randrange(0, len(directions) -1)]
    except Exception:
        pass
    return directions