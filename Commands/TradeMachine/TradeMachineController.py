import pandas as pd

from utils import Utils
from APIs.formatter import Formatter
from APIs.bball_api import BBallAPI
from APIs.yahoo_get import YahooAPI
from Commands.FbPlayerRank.FbPlayerRankPandas import FbRankPandas

pd.set_option("display.max_rows", None)


class TradeMachineController:
	def __init__(self):
		self.utils = Utils()
		self.formatter = Formatter()
		self.basketball_API = BBallAPI()
		self.yahoo_API = YahooAPI()
		self.pandas_FbRank = FbRankPandas()

	def trade_machine(self, df, my_players, their_players):
		my_df = df[df["Name"].isin(my_players)]
		their_df = df[df["Name"].isin(their_players)]
	
		self.utils.print(my_df.sort_values(by="My Rank", ascending=True))
		print("")
		self.utils.print(their_df.sort_values(by="My Rank", ascending=True))