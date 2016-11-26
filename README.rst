This holds a few scripts related to fantasy football.

Flask app
---------
This contains a flask app that shows a strength of schedule.

Run it by doing the following:

    . venv/bin/activate
    ./run.py

Reuse
-----

The flask app can be used as a blueprint in other flask projects. 

    # Install the code

    pip install -I git+https://github.com/dhan12/FantasyFootball


    # Then use the blue print in flask

    from fantasy_football import fantasy_football as fantasy_football_blueprint

    app.register_blueprint(fantasy_football_blueprint, url_prefix='/fantasyfootball') 

You can also create a distribution like this

    # python setup.py sdist

One off
-------
A bunch of other quick scripts are in the one_off folder. These are not part of the flask application.

