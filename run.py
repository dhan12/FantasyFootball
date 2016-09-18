#!/usr/bin/env python
import os
from flask import Flask
from flask_bootstrap import Bootstrap


'''
Script to run and test the fantasy_football module.
'''

bootstrap = Bootstrap()
def create_app():
    """Create an application instance."""
    app = Flask(__name__)
    bootstrap.init_app(app)

    # import configuration
    cfg = os.path.join(os.getcwd(), 'config.py')
    app.config.from_pyfile(cfg)

    # import blueprints
    from fantasy_football import fantasy_football as fantasy_football_blueprint
    app.register_blueprint(fantasy_football_blueprint)

    return app

application = create_app()
if __name__ == '__main__':
    application.run('0.0.0.0')
