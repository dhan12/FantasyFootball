import team_names
filename = 'fantasy_football/data/point.spread.week7.txt'

with open(filename, 'r') as data:
    for line in data:
        items = team_names.cleanName(line).replace('At ','').split()
        if len(items) < 4: continue

        try:
            favorite = items[0]
            spread = float(items[1])
            underdog = items[2]
            total = float(items[3])
        except:
            continue

        bigValue = (total - spread) / 2
        smallValue  = bigValue + spread

        print favorite, bigValue, underdog, smallValue
