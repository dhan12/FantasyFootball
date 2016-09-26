from flask import render_template, redirect, url_for, request, current_app
from flask import Markup
import markdown
from . import fantasy_football
import strength_of_schedule
import team_names
import points_against
import forms

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
    last_updated = points_against.getLastUpdated(2016)

    # Get a base html that we'll inherit from
    if current_app.config.get('SIMPLE_PAGE_BASE_HTML'):
        base_html = current_app.config.get('SIMPLE_PAGE_BASE_HTML')

    # Get arguments
    form = forms.TeamsForm()

    passingTeams  = []
    rushingTeams  = []
    receivingTeams  = []
    receivingTeams2  = []
    if form.validate_on_submit():
        passingTeams  = form.passingTeams.data.split()
        rushingTeams  = form.rushingTeams.data.split()
        receivingTeams  = form.receivingTeams.data.split()
        receivingTeams2  = form.receivingTeams2.data.split()

    posToTeams = [
        { 'pos': 'qb', 'teams' : passingTeams},
        { 'pos': 'rb', 'teams' : rushingTeams},
        { 'pos': 'wr', 'teams' : receivingTeams},
        { 'pos': 'te', 'teams' : receivingTeams2},
    ]


    # Get input data
    team_scores = strength_of_schedule.team_scores
    schedule = strength_of_schedule.schedule
    score_tiers = strength_of_schedule.score_tiers

    # Output
    scoresTable = []
    headers = ['']
    for i in xrange(16): headers.append('Week ' + str(i + 1))

    # Process data
    for agg in posToTeams:
        pos = agg['pos']
        teams = agg['teams']
        teamsToShow = strength_of_schedule.getSchedules(teams)
        scores = []

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
            scores.append(row)
        scoresTable.append({'pos': pos.upper(), 'scores': scores})

    return render_template('ff_strength_of_schedule.html', **locals())

@fantasy_football.route('/raw', methods=['GET','POST'])
def raw():
    version = _getVersion() 
    data = []

    # Get a base html that we'll inherit from
    if current_app.config.get('SIMPLE_PAGE_BASE_HTML'):
        base_html = current_app.config.get('SIMPLE_PAGE_BASE_HTML')

    # Get arguments
    form = forms.RefreshData()
    if form.validate_on_submit():
        if form.refresh:
            newData = points_against.processFromWeb(2016)
            for agg in newData:
                points_against.saveParsedData(2016, agg)
                data.append({'file_name': 'new data for ' + agg['pos'], 
                            'lines': agg['data'] })

            data_updated = 'Data was just updated !'
            return render_template('ff_points_against_raw.html', **locals())

    # Get input data
    files = points_against.getPointsAgainstFiles(2015)
    for f in files:
        with open(f, 'r') as fInput:
            data.append({'file_name': f, 'lines': fInput.read()})
    files = points_against.getPointsAgainstFiles(2016)
    for f in files:
        with open(f, 'r') as fInput:
            data.append({'file_name': f, 'lines': fInput.read()})

    # Retrieve data from web
    newData = points_against.processFromWeb(2016)
    for agg in newData:
        data.append({'file_name': 'new data for ' + agg['pos'], 
                     'lines': agg['data'] })


    return render_template('ff_points_against_raw.html', **locals())
