from flask import render_template, redirect, url_for, request, current_app
from flask import Markup
import markdown
from . import fantasy_football
import strength_of_schedule
import team_names
from .forms import TeamsForm

def _getVersion():
    import subprocess
    import os
    try:
        with open(os.devnull, 'a') as devnull:
            revisionCode = subprocess.check_output(['git', 'rev-parse', 'HEAD'],
                    stderr=devnull)
            return revisionCode[:8]
    except subprocess.CalledProcessError as e:
        return ''

@fantasy_football.route('/', methods=['GET','POST'])
def content():
    version = _getVersion() 

    # Get a base html that we'll inherit from
    if current_app.config.get('SIMPLE_PAGE_BASE_HTML'):
        base_html = current_app.config.get('SIMPLE_PAGE_BASE_HTML')

    # Get arguments
    form = TeamsForm()

    passingTeams  = []
    rushingTeams  = []
    receivingTeams  = []
    receivingTeams2  = []
    if form.validate_on_submit():
        passingTeams  = form.passingTeams.data.split()
        rushingTeams  = form.rushingTeams.data.split()
        receivingTeams  = form.receivingTeams.data.split()
        receivingTeams2  = form.receivingTeams2.data.split()


    posToTeamsMap = {
        'qb': passingTeams,
        'rb': rushingTeams,
        'wr': receivingTeams,
        'te': receivingTeams2,
    }


    # Get input data
    team_scores = strength_of_schedule.team_scores
    schedule = strength_of_schedule.schedule
    score_tiers = strength_of_schedule.score_tiers

    # Output
    headers = ['']
    for i in xrange(16): headers.append('Week ' + str(i + 1))
    scoresTable = {
        'qb': [],
        'rb': [],
        'wr': [],
        'te': []
    }

    # Process data
    for pos in posToTeamsMap:
        teamsToShow = strength_of_schedule.getSchedules(posToTeamsMap[pos])

        dataset = pos
        if dataset == 'te': dataset = 'wr'

        for t in teamsToShow:
            abbr = t['team']
            teamName = team_names.abbreviations[abbr]
            row = [{'name': teamName}]

            week = 1
            for opponent in schedule[abbr]:
                if week >= 17: break
                week += 1 

                # Get the score
                if opponent == 'BYE':
                    opponent = 'BYE'
                    score = -1
                else:
                    fullName = team_names.abbreviations[opponent.replace('@','')]
                    try:
                        score = int(team_scores[ fullName ][dataset + ''] / 
                                team_scores[ fullName ][dataset + 'Weight'] )
                    except ZeroDivisionError:
                        score = 0

                if   score == -1:
                    tier = 'na'
                    score = ''
                elif score <= score_tiers[dataset]['low']:
                    tier = 'low'
                elif score >= score_tiers[dataset]['hi']:
                    tier = 'hi'
                else:
                    tier = 'default'

                row.append({ 'score': score, 'opponent': opponent, 'tier': tier} )
            scoresTable[pos].append(row)

    return render_template('content.html', **locals())
