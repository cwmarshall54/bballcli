from setuptools import setup, find_packages

setup(
    name='fantasybball',
    version='0.1',
    packages=find_packages(),
    install_requires=[
    	'click',
    	'unidecode',
    	'yahoo_fantasy_api',
    	'yahoo_oauth',
    	'pandas'
    ],
    entry_points='''
        [console_scripts]
        player_averages=player_averages:cli
    '''
    ,
)