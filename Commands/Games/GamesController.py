import pandas as pd

from utils import Utils
from APIs.formatter import Formatter
from APIs.bball_api import BBallAPI
from APIs.yahoo_get import YahooAPI

pd.set_option("display.max_rows", None)


class GamesController:
	def __init__(self):
		self.utils = Utils()
		self.formatter = Formatter()
		self.basketball_API = BBallAPI()
		self.yahoo_API = YahooAPI()
	
	def refresh_player_stats(self):
		players_with_stats = self.basketball_API.refresh_2021_season_player_stats()
		self.utils.write_file("player_stats_index.json", players_with_stats)
		return players_with_stats
	
	def get_ownership_of_taken_players(self):
		owner_list = self.yahoo_API.ownership_of_taken_players()
		self.utils.write_file("owner_index.json", owner_list)
		return owner_list
	
	def games(self, name, refresh):
		if name == "" or name is None:
			print("Use -n to specify a partial first name")
			print("Eg: '-n Le' would return 'Lebron James'")
			return
		
		if refresh:
			player_stats = self.refresh_player_stats()
			owner_list = self.get_ownership_of_taken_players()
		else:
			player_stats = self.utils.read_file("player_stats_index.json")
			owner_list = self.utils.read_file("owner_index.json")
		df = self.formatter.pandas_player_games(player_stats, owner_list)
		
		df['match'] = df['name'].str.find(name) != -1
		
		df = df.drop(df.loc[df["match"] == False].index)
		
		df = df.drop(['match'], axis=1)
		
		df = df.set_index('date')
		
		print(df.sort_values(by="date", ascending=False))
