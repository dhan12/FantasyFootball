from distutils.core import setup
setup(name='fantasy_football',
        version='1.0',
        packages=['fantasy_football'],
        package_data={'fantasy_football': ['data/*.txt', 'templates/*.html']},
        include_package_data=True )
