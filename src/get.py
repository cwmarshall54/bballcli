#!/usr/bin/python3

import os
import sys

import unidecode

from utils import Utils
from yahoo_get import YahooAPI
from bball_get import BBallAPI
from formatter import Formatter

utils = Utils()
yahoo_API = YahooAPI()
bball_API = BBallAPI()
formatter = Formatter()

translate = {
	"moeharkless": "mauriceharkless",
	"kevinknoxii": "kevinknox",
	"camreddish": "cameronreddish",
	"marcusmorrissr": "marcusmorris",
	"guillermohernangomez": "willyhernangomez",
	"robertwilliams": "robertwilliamsiii"
}

exceptions = ["moeharkless", "kevinknoxii", "camreddish", "marcusmorrissr", "guillermohernangomez", "robertwilliams"]
ignore = ["kjmartinjr"]

#YAHOO
def yahoo_get_current_league_matchups():
	curr_week = utils.get_curr_week()
	league_matchups = yahoo_API.get_matchups(curr_week)
	utils.write_file("week_" + str(curr_week) + ".json", league_matchups)

#BBALL
def bball_get_all_player_ids():
	player_list = bball_API.get_all_player_ids()
	utils.write_file("bball_playerids.json", player_list)

def refresh_player_stats():
	players_with_stats = bball_API.refresh_2021_season_player_stats()
	utils.write_file("player_stats_index.json", players_with_stats)

#Merge BBall and Yahoo players to master player list
def merge(yahoo, bball):
	merged = []
	for yahooplayer in yahoo:
		key_name = unidecode.unidecode(yahooplayer['name'].lower().replace(" ", "").replace(".", "").replace("'", ""))
		if key_name in ignore:
			continue
		if key_name in exceptions:
			key_name = translate[key_name]
		yahooplayer['bball_id'] = bball[key_name]
		merged.append(yahooplayer)
	return merged

# Refresh player stats
refresh_player_stats()


# Team analytics
# python3 get.py && python3 analytics.py
# yahoo_get_current_league_matchups()


