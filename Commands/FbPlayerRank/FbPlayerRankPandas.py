import pandas as pd

from utils import Utils
from APIs.formatter import Formatter
from APIs.bball_api import BBallAPI
from APIs.yahoo_get import YahooAPI

pd.set_option("display.max_rows", None)


class FbRankPandas:
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
		
	def yahoo_rank(self, should_refresh, count, show_z, sort):
		if should_refresh:
			player_stats = self.refresh_player_stats()
			owner_list = self.get_ownership_of_taken_players()
		else:
			player_stats = self.utils.read_file("player_stats_index.json")
			owner_list = self.utils.read_file("owner_index.json")
			
		df = self.formatter.pandas_player_averages(player_stats, owner_list)
		
		df = df.head(200)
		
		df['ft_per'] = df['ftm'] / df['fta']
		df['ft_weighted'] = (df['ft_per'] - df['ft_per'].mean()) * df['ftm']
		
		df['fg_per'] = df['fgm'] / df['fga']
		df['fg_weighted'] = (df['fg_per'] - df['fg_per'].mean()) * df['fgm']
		
		cols = list(df.columns)
		
		for col in ['Roster status', 'Name', "IS", "Eligible positions", 'ftm', 'fta', 'fga', 'fgm', 'ft_per', 'fg_per',
		            'min']:
			cols.remove(col)
		
		for col in cols:
			col_z = col + '_z'
			top = df.sort_values(by=col, ascending=False).head(350)
			drop_na_col = top[col]
			if col == "TO":
				df[col_z] = (drop_na_col - drop_na_col.mean()) / drop_na_col.std(ddof=1) * -1
			else:
				df[col_z] = (drop_na_col - drop_na_col.mean()) / drop_na_col.std(ddof=1)
		
		df = df.fillna(0)
		
		df["Total_z"] = df["ast_z"] + df["fg3m_z"] + df["pts_z"] + df["reb_z"] + df["stl_z"] \
		                + df["blk_z"] + df['ft_weighted_z'] + df['fg_weighted_z']  # + df['TO_z']
		df['Total Rank'] = df['Total_z'].rank(ascending=False).astype(int)
		
		df = df.set_index('Total Rank')
		
		if show_z:
			df = df.drop(
				['GP_z', 'blk', 'fg3m', 'ast', 'reb', 'stl', "TO",
				 "ft_weighted", "fga", "fgm", "ftm", "fta", "ft_per", "fg_per",
				 "fg_weighted", "pts", "Eligible positions"], axis=1)
		else:
			df = df.drop(
				['GP_z', 'blk_z', 'fg3m_z', 'ast_z', 'reb_z', 'stl_z', "TO_z",
				 "ft_weighted",
				 "fg_weighted", "pts_z", "ft_weighted_z", "fg_weighted_z", "Eligible positions"], axis=1)
			
		if sort:
			sort_by = sort
			asc = False
		else:
			sort_by = "Total Rank"
			asc = True
					
		df = df.sort_values(by=sort_by, ascending=asc).head(count).round(3)
		return df
	
		# df = df[['name', 'ast_z', 'blk_z', 'fg3m_z', 'pts_z', 'reb_z', 'stl_z',
		# 'ft_weighted_z', 'fg_weighted_z', 'turnover_z', 'Total_z']]
		
		# df1 = df[df["Roster status"]].isin(["Chuck it for buckets", "Dame Time"])
		
		# print(df1.sort_values(by="My Rank", ascending=True))
		
		# #df = df[df["Roster status"] != "FA"]
