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

    # Get arguments
    form = TeamsForm()
    if form.validate_on_submit():
        print 'in forms validate'
        teams = teams=form.teams.data
        print 'in forms validate', teams

        return redirect(url_for('fantasy_football.content', teams=teams))

    if 'teams' in request.args:
        teams = request.args['teams'].split()
    else:
        teams = []

    pos = 'qb'

    # Get input data
    teamsToShow = strength_of_schedule.getSchedules(teams)
    team_scores = strength_of_schedule.team_scores
    schedule = strength_of_schedule.schedule
    score_tiers = strength_of_schedule.score_tiers

    # Output
    headers = ['']
    for i in xrange(16): headers.append('Week ' + str(i + 1))
    scoresTable = []

    # Process data
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
                    score = int(team_scores[ fullName ][pos + ''] / 
                               team_scores[ fullName ][pos + 'Weight'] )
                except ZeroDivisionError:
                    score = 0

            if   score == -1:
                tier = 'na'
                score = ''
            elif score <= score_tiers[pos]['low']:
                tier = 'low'
            elif score >= score_tiers[pos]['hi']:
                tier = 'hi'
            else:
                tier = 'default'

            row.append({ 'score': score, 'opponent': opponent, 'tier': tier} )
        scoresTable.append(row)

    return render_template('content.html', **locals())
