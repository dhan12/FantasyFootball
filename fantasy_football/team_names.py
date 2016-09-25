nickNames = {
    'Saints': 'New-Orleans',
    'Cowboys': 'Dallas',
    'Redskins': 'Washington',
    'Vikings': 'Minnesota',
    'Broncos': 'Denver',
    'Buccaneers': 'Tampa-Bay',
    'Browns': 'Cleveland',
    'Panthers': 'Carolina',
    'Cardinals': 'Arizona',
    'Steelers': 'Pittsburgh',
    'Bears': 'Chicago',
    '49ers': 'San-Francisco',
    'Chiefs': 'Kansas-City',
    'Falcons': 'Atlanta',
    'Giants': 'NY-Giants',
    'Jaguars': 'Jacksonville',
    'Dolphins': 'Miami',
    'Packers': 'Green-Bay',
    'Lions': 'Detroit',
    'Eagles': 'Philadelphia',
    'Colts': 'Indianapolis',
    'Patriots': 'New-England',
    'Bills': 'Buffalo',
    'Ravens': 'Baltimore',
    'Texans': 'Houston',
    'Raiders': 'Oakland',
    'Bengals': 'Cincinnati',
    'Chargers': 'San-Diego',
    'Titans': 'Tennessee',
    'Jets': 'NY-Jets',
    'Rams': 'Los-Angeles',
    'Seahawks': 'Seattle',
}
abbreviations = {
    'NO': 'New-Orleans',
    'DAL': 'Dallas',
    'WSH': 'Washington',
    'MIN': 'Minnesota',
    'DEN': 'Denver',
    'TB': 'Tampa-Bay',
    'CLE': 'Cleveland',
    'CAR': 'Carolina',
    'ARI': 'Arizona',
    'PIT': 'Pittsburgh',
    'CHI': 'Chicago',
    'SF': 'San-Francisco',
    'KC': 'Kansas-City',
    'ATL': 'Atlanta',
    'NYG': 'NY-Giants',
    'JAX': 'Jacksonville',
    'MIA': 'Miami',
    'GB': 'Green-Bay',
    'DET': 'Detroit',
    'PHI': 'Philadelphia',
    'IND': 'Indianapolis',
    'NE': 'New-England',
    'BUF': 'Buffalo',
    'BAL': 'Baltimore',
    'HOU': 'Houston',
    'OAK': 'Oakland',
    'CIN': 'Cincinnati',
    'SD': 'San-Diego',
    'TEN': 'Tennessee',
    'NYJ': 'NY-Jets',
    'LA': 'Los-Angeles',
    'SEA': 'Seattle',
}
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
