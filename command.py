#!/usr/bin/python3
import click

from Commands.FbPlayerRank.FbPlayerRankController import FbPlayerRankController
from Commands.FbTeamRank.FbTeamRankController import FbTeamRankController


@click.group()
@click.version_option()
def cli():
	"""A command line application"""
	pass


@cli.command()
@click.option('-r', default=False, help='Should refresh player stats', type=bool)
@click.option('-c', default=15, help='Number of players', type=int)
def fbPlayers(r, c):
	FbPlayerRankController().print_fb_rank(r, c)
	

@cli.command()
def fbTeams():
	FbTeamRankController().fb_teams_rank()


if __name__ == '__main__':
	fbPlayers()
	fbTeams()
