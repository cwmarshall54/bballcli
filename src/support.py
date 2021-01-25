#!/usr/bin/python3

import unidecode

from utils import Utils
from yahoo_get import YahooAPI
from bball_api import BBallAPI
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

# BBALL
def bball_get_all_player_ids():
	player_list = bball_API.get_all_player_ids()
	utils.write_file("bball_playerids.json", player_list)

# Merge BBall and Yahoo players to master player list
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


