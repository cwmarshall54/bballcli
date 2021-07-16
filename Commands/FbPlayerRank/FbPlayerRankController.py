import pandas as pd

from utils import Utils
from APIs.formatter import Formatter
from APIs.bball_api import BBallAPI
from APIs.yahoo_get import YahooAPI
from Commands.FbPlayerRank.FbPlayerRankPandas import FbRankPandas

pd.set_option("display.max_rows", None)


class FbPlayerRankController:
	def __init__(self):
		self.utils = Utils()
		self.formatter = Formatter()
		self.basketball_API = BBallAPI()
		self.yahoo_API = YahooAPI()
		self.pandas_FbRank = FbRankPandas()
	
	def print_fb_rank(self, should_refresh, count, show_zscore, sort_by):
		df = self.pandas_FbRank.yahoo_rank(should_refresh, count, show_zscore, sort_by)
		print(df)
