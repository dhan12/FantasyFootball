from cleanName import cleanName
filename = 'data/point.spread.week2.txt'

with open(filename, 'r') as data:
    for line in data:
        items = cleanName(line).replace('At ','').split()
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
