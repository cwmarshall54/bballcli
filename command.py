#!/usr/bin/python3
import click

from Commands.FbPlayerRank.FbPlayerRankController import FbPlayerRankController
from Commands.FbTeamRank.FbTeamRankController import FbTeamRankController
from Commands.PlayerIndex.PlayerIndexController import PlayerIndexController
from Commands.Games.GamesController import GamesController
from APIs.odds_api import OddsAPI


@click.group()
@click.version_option()
def cli():
	"""A command line application"""
	pass


@cli.command()
@click.option('--refresh', '-r', help='Should refresh player stats', is_flag=True)
@click.option('--count', '-c', default=15, help='Number of players', type=int)
@click.option('--show_zscore', '-z', help='Show zscore', is_flag=True)
def fbplayers(refresh, count, show_zscore):
	FbPlayerRankController().print_fb_rank(refresh, count, show_zscore)
	

@cli.command()
def fbteams():
	FbTeamRankController().fb_teams_rank()
	

@cli.command()
@click.option('--name', '-n', help='Name of player you want to search for', type=str)
@click.option('--all_players', '-a', help='Show all players', is_flag=True)
def playerindex(name, all_players):
	PlayerIndexController().player_index(name, all_players)
	

@cli.command()
@click.option('--refresh', '-r', help='Should refresh', is_flag=True)
def odds(refresh):
	OddsAPI().command(refresh)
	
	
@cli.command()
@click.option('--name', '-n', help='Name of player you want to search for', type=str)
@click.option('--refresh', '-r', help='Should refresh player stats', is_flag=True)
def games(name, refresh):
	GamesController().games(name, refresh)


if __name__ == '__main__':
	fbplayers()
	fbteams()
	playerindex()
	odds()
	games()
