'''
Get data for a league.
'''
from html.parser import HTMLParser
import requests
from FantasyFootball.team_names import nickNames


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
        if not self.foundPlayerTableTable:
            return

        if not self.teamToProcess:
            items = data.split()
            if len(items) != 3:
                return
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


def processFromWeb(htmlFile):
    '''
    try:
        # If file exists, don't fetch again
        with open(htmlFile, 'r'):
            pass
    except IOError:
        # If file doesn't exist, fetch file.
    '''
    ROSTER_URL = 'http://games.espn.com/ffl/leaguerosters?leagueId=225977'

    # Make remote call to get data
    resp = requests.get(ROSTER_URL)
    print(dir(resp))
    help(resp)
    print(resp)

    # Save response
    with open(htmlFile, 'w') as output:
        output.write(resp.text)

    # Process the data
    '''
    with open(htmlFile, 'r') as inputFile:
        parser = MyHtmlParser()
        parser.feed(inputFile.read())
    '''


def parse(outputFileDir):
    htmlFile = outputFileDir + '/espn_teams.html'
    data = processFromWeb(htmlFile)
