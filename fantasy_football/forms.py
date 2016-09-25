from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import Required, Length


class TeamsForm(Form):
    passingTeams = StringField('QB Teams')
    rushingTeams = StringField('RB Teams')
    receivingTeams = StringField('WR Teams')
    receivingTeams2 = StringField('TE Teams')
    #password = PasswordField('Password', validators=[Required()])
    #remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')
