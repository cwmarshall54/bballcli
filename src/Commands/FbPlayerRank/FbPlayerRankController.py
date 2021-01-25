import pandas as pd

from utils import Utils
from formatter import Formatter
from bball_api import BBallAPI
from yahoo_get import YahooAPI
from Commands.FbPlayerRank.FbPlayerRankPandas import FbRankPandas

pd.set_option("display.max_rows", None)


class FbPlayerRankController:
	def __init__(self):
		self.utils = Utils()
		self.formatter = Formatter()
		self.basketball_API = BBallAPI()
		self.yahoo_API = YahooAPI()
		self.pandas_FbRank = FbRankPandas()
	
	def refresh_player_stats(self):
		players_with_stats = self.basketball_API.refresh_2021_season_player_stats()
		self.utils.write_file("player_stats_index.json", players_with_stats)
		return players_with_stats
	
	def get_ownership_of_taken_players(self):
		owner_list = self.yahoo_API.ownership_of_taken_players()
		self.utils.write_file("owner_index.json", owner_list)
		return owner_list
	
	def print_fb_rank(self, should_refresh, count):
		if should_refresh:
			player_stats = self.refresh_player_stats()
			owner_list = self.get_ownership_of_taken_players()
		else:
			player_stats = self.utils.read_file("player_stats_index.json")
			owner_list = self.utils.read_file("owner_index.json")
		
		self.pandas_FbRank.yahoo_rank(player_stats, owner_list, count)
