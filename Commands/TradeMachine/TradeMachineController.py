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

	def trade_machine(self, my_players, their_players, should_refresh):
		df = self.pandas_FbRank.yahoo_rank(should_refresh, 200, None, None)
		
		my_df = df[df["Name"].isin([my_players])]
		their_df = df[df["Name"].isin([their_players])]
	
		self.utils.print(pd.concat([my_df, their_df]).sort_values(by="Total Rank", ascending=True))