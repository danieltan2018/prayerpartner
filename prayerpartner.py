import random


def getcurrent():
    with open('countmein.txt', 'r') as current:
        currentlist = []
        for row in current:
            row = row.strip('\n')
            currentlist.append(row)
    return(currentlist)


def scramble():
    current = getcurrent()
    size = len(current)
    new = []
    while len(new) < size:
        dice = random.randrange(0, size)
        if current[dice] not in new:
            new.append(current[dice])
    return new


def getpairs():
    with open('pairings.txt', 'r') as pairings:
        week = []
        all_pairs = []
        for row in pairings:
            row = row.strip('\n')
            if str(row[0]).isnumeric():
                if len(week) > 0:
                    all_pairs.append(week)
                    week = []
                    nextdate = row
            else:
                week.append(row)
    return(all_pairs, nextdate)


def checkpairs(all_pairs):
    newlist = scramble()
    for x in range(0, len(newlist), 2):
        p1 = newlist[x]
        p2 = newlist[x+1]
        for week in all_pairs:
            findp1 = (week.index(p1) if p1 in week else -1)
            if (findp1 > -1):
                if (findp1 % 2 == 0):
                    if p2 == week[findp1+1]:
                        return False
                else:
                    if p2 == week[findp1-1]:
                        return False
    return newlist


def mapper():
    with open('telehandles.txt', 'r') as telehandles:
        map = {}
        lines = telehandles.readlines()
        for i in range(0, len(lines), 2):
            name = lines[i].strip('\n')
            handle = lines[i+1].strip('\n')
            map[name] = handle
    return map


def generator():
    pair_data = getpairs()
    all_pairs = pair_data[0]
    nextdate = pair_data[1]
    newlist = checkpairs(all_pairs)
    while (newlist == False):
        newlist = checkpairs(all_pairs)
    with open('new.txt', 'w') as myfile:
        for item in newlist:
            myfile.write(item + '\n')
    print('\nYF Prayer Partners (' + nextdate + ')')
    map = mapper()
    for x in range(0, len(newlist), 2):
        left = newlist[x]
        right = newlist[x+1]
        left = (map[left] if left in map else left)
        right = (map[right] if right in map else right)
        print(left, '&', right)


generator()
