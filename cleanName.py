def cleanName(line):
    return line.replace('Green Bay', 'Green-Bay') \
            .replace('NY Jets', 'NY-Jets')\
            .replace('NY Giants', 'NY-Giants')\
            .replace('San Diego', 'San-Diego')\
            .replace('Los Angeles', 'Los-Angeles')\
            .replace('New Orleans', 'New-Orleans')\
            .replace('Tampa Bay', 'Tampa-Bay')\
            .replace('New England', 'New-England')\
            .replace('San Francisco', 'San-Francisco')\
            .replace('Kansas City', 'Kansas-City')\
