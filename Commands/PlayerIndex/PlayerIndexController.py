import pandas as pd

from utils import Utils
from APIs.formatter import Formatter
from APIs.bball_api import BBallAPI
from APIs.yahoo_get import YahooAPI

pd.set_option("display.max_rows", None)


class PlayerIndexController:
	def __init__(self):
		self.utils = Utils()
		self.formatter = Formatter()
		self.basketball_API = BBallAPI()
		self.yahoo_API = YahooAPI()
		
	def player_index(self, name, all_players):
		if name == "" or name is None and not all_players:
			print("Use -n to specify a partial first name")
			print("Eg: '-n Le' would return 'Lebron James'")
			return
		
		player_stats = self.utils.read_file("player_stats_index.json")
		owner_list = self.utils.read_file("owner_index.json")
		df = self.formatter.pandas_player_averages(player_stats, owner_list)
		
		if all_players:
			print(df)
			return
		
		df['match'] = df['Name'].str.startswith(name)
		
		df = df.drop(df.loc[df["match"] == False].index)
		
		df = df.drop(['match'], axis=1)
		
		print(df)
