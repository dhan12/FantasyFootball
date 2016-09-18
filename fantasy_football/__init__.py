'''
This module defines a blueprint that is used to render 
simple pages written in markdown in a flask app. 
'''
from flask import Blueprint

fantasy_football = Blueprint('fantasy_football', __name__, template_folder='./templates')

from . import routes
