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
    	'pandas',
	    'requests'
    ],
    entry_points='''
        [console_scripts]
        nba=command:cli
    '''
    ,
)