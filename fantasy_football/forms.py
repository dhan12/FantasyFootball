from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import Required, Length


class TeamsForm(Form):
    passingTeams = StringField('QB Teams')
    rushingTeams = StringField('RB Teams')
    receivingTeams = StringField('WR Teams')
    receivingTeams2 = StringField('TE Teams')
    weeksToSkip = StringField('Skip through week ')
    submit = SubmitField('Submit')

class RefreshData(Form):
    refresh = SubmitField('Refresh')

