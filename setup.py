from setuptools import setup

setup(name='FantasyFootball',
      version='0.0.1',
      packages=['FantasyFootball'],
      entry_points={
          'console_scripts': [
              'FantasyFootball = FantasyFootball.__main__:main'
          ]
      },
      )
