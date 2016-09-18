from flask import render_template, redirect, url_for, request, current_app
from flask import Markup
import markdown
from . import fantasy_football
import strength_of_schedule

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

@fantasy_football.route('/')
def content():
    version = _getVersion() 

    # Get arguments

    # Run script to get data
    teamsToShow = strength_of_schedule.getSchedules(['HOU'])
    data = strength_of_schedule.team_scores


    return render_template('content.html', **locals())
