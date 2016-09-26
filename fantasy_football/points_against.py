'''
Refresh points against data.
''' 
from HTMLParser import HTMLParser
import requests
import team_names
import os
import time
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

class MyHtmlParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.foundPlayerTableTable = False
        self.reset_team()
        self.data = {}

    def reset_team(self):
        self.teamToProcess = None
        self.pointsTagFound = False


    def handle_starttag(self, tag, attrs):
        if not self.foundPlayerTableTable:
            if tag == 'table' and attrs[0][1] == 'playerTableTable tableBody':
                # print "found start tag:", tag, attrs
                self.foundPlayerTableTable = True
            return

        if self.teamToProcess:
            if tag == 'td' and \
                len(attrs) > 0 and \
                attrs[0][1] == 'playertableStat appliedPoints':
                self.pointsTagFound = True
                # print "found encountered start tag:", tag, attrs
            return

    def handle_endtag(self, tag):
        # print "encountered end   tag:", tag
        return

    def handle_data(self, data):
        if not self.foundPlayerTableTable: return

        if not self.teamToProcess:
            items = data.split()
            if len(items) != 3: return
            try:
                # print "getting team:", items
                name = team_names.nickNames[items[0]]
                pos = items[2]
                self.teamToProcess = name
                return
            except:
                pass

        if self.pointsTagFound:
            score = float(data)
            # print 'assinging score ', self.teamToProcess, score 
            self.data[self.teamToProcess] = score 
            self.reset_team()

def getPointsAgainstFiles(year):
    return [CURRENT_DIR + '/data/points_against.' + str(year) + '.' + pos + '.txt'
            for pos in ['QB', 'RB', 'WR', 'TE']]

def processFromWeb(year):

    yearStr = str(year)
    urls = [
        {'pos': 'QB', 'url': 'http://games.espn.com/ffl/pointsagainst?positionId=1&seasonId=' + yearStr},
        {'pos': 'RB', 'url': 'http://games.espn.com/ffl/pointsagainst?positionId=2&seasonId=' + yearStr},
        {'pos': 'WR', 'url': 'http://games.espn.com/ffl/pointsagainst?positionId=3&seasonId=' + yearStr},
        {'pos': 'TE', 'url': 'http://games.espn.com/ffl/pointsagainst?positionId=4&seasonId=' + yearStr},
    ]


    retData = []
    for agg in urls:
        pos = agg['pos']
        url = agg['url']

        # Make remote call to get data
        resp = requests.get(url)

        # Process the data
        parser = MyHtmlParser()
        parser.feed(resp.text)

        # Return data
        retData.append({'pos': pos, 'data': parser.data})

    return retData

def saveParsedData(year, data):
    # Save parsed data
    output = CURRENT_DIR + '/data/points_against.' + str(year) + '.' + data['pos'] + '.txt'
    with open(output,'w') as writer:
        for name, score  in data['data'].iteritems():
            writer.write(name + ',' + str(score) + '\n')

def processFromFile():
    with open(CURRENT_DIR + '/data/test_points_against.html','r') as inputHtml:
        # Process the data
        parser = MyHtmlParser()
        parser.feed(inputHtml.read())

        # Return processed data
        for name, score  in parser.data.iteritems():
            print name, score

def getLastUpdated(year):
    path = CURRENT_DIR + '/data/points_against.' + str(year) + '.QB.txt'
    return time.ctime(os.path.getmtime(path))

if __name__ == '__main__':
    # processFromFile()
    year = 2016
    data = processFromWeb(year)
    for agg in data:
        saveParsedData(year, agg)

