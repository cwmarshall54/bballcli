import pandas as pd

from utils import Utils
from APIs.formatter import Formatter
from APIs.bball_api import BBallAPI
from APIs.yahoo_get import YahooAPI
from Commands.FbPlayerRank.FbPlayerRankPandas import FbRankPandas

pd.set_option("display.max_rows", None)

columns = ['FG%', 'FT%', '3PM', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TO']
rank_columns = ['FG% Rank', 'FT% Rank', '3PM Rank', 'PTS Rank', 'REB Rank', 'AST Rank', 'STL Rank', 'BLK Rank', 'TO Rank']


class FbTeamRankController:
	def __init__(self):
		self.utils = Utils()
		self.formatter = Formatter()
		self.basketball_API = BBallAPI()
		self.yahoo_API = YahooAPI()
		self.pandas_FbRank = FbRankPandas()
		
	def fb_teams_rank(self):
		self.yahoo_get_current_league_matchups()
		df = self.generate_better_team_ranks(self.parse_all_matchups())
		print(df)
	
	def yahoo_get_current_league_matchups(self):
		curr_week = self.utils.get_curr_week()
		league_matchups = self.yahoo_API.get_match_ups(curr_week)
		self.utils.write_file("week_" + str(curr_week) + ".json", league_matchups)
	
	def generate_team_ranks(self, df):
		for column in columns:
			df = df.sort_values(by=column, ascending=(column != 'TO'))
			df.loc[:, (column + " Rank")] = self.utils.order_list(df[column].tolist())
		df.loc[:, "Total Rank"] = df[rank_columns].sum(axis=1)
		return df.sort_values(by="Total Rank", ascending=False)
	
	def generate_better_team_ranks(self, df):
		for column in columns:
			df = df.sort_values(by=column, ascending=(column != 'TO'))
			df.loc[:, (column + " Rank")] = self.recreate_list(df[column].tolist(), df, column)
		
		df.loc[:, "Top 6 Rank"] = self.drop_three_lowest(df)
		df.loc[:, "Total Rank"] = df[rank_columns].sum(axis=1)
		return df.sort_values(by="Total Rank", ascending=False)
	
	@staticmethod
	def recreate_list(lst, df, column):
		worst = df[column].iloc[0]
		best = df[column].iloc[9]
		
		new_lst = []
		for item in lst:
			val = round((9 / (best - worst)) * (item - best) + 10, 2)
			new_lst.append(val)
		return new_lst
	
	@staticmethod
	def drop_three_lowest(df):
		df = df.drop(["FGM/A", "FG%", "FTM/A", "FT%", "3PM", "PTS", "REB", "AST", "STL", "BLK", "TO"], axis=1)
		series = []
		for row_num in range(0, 10):
			lst = df.iloc[row_num].tolist()
			lst.sort()
			series.append(round(sum(lst[3:9]), 2))
		
		return series

	def parse_all_matchups(self):
		all_data = self.parse_week_matchups(9)
		for week_num in range(10, self.utils.get_curr_week() + 1):
			week_data = self.parse_week_matchups(week_num)
			all_data = self.utils.combine_weeks(all_data, week_data)
		return all_data.set_index('name')
	
	def parse_week_matchups(self, week):
		data = self.utils.flatten_week(self.utils.read_file('week_' + str(week) + '.json'))
		return pd.DataFrame.from_dict(data, orient='index')
