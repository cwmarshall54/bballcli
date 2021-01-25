import pandas as pd

from utils import Utils
from formatter import Formatter

pd.set_option("display.max_rows", None)


class FbRankPandas:
	def __init__(self):
		self.utils = Utils()
		self.formatter = Formatter()
		
	def yahoo_rank(self, player_stats, owner_list, count):
		raw_stats = self.combine_stats_with_owner(player_stats, owner_list)
		
		combined = self.formatter.combine_player_stats_dic(raw_stats)
		
		df = pd.DataFrame(combined)
		
		df = df[df['min'] > 5]
		
		df['ft_per'] = df['ftm'] / df['fta']
		df['ft_weighted'] = (df['ft_per'] - df['ft_per'].mean()) * df['ftm']
		
		df['fg_per'] = df['fgm'] / df['fga']
		df['fg_weighted'] = (df['fg_per'] - df['fg_per'].mean()) * df['fgm']
		
		cols = list(df.columns)
		
		for col in ['Roster status', 'Name', "IS", "Eligible positions", 'ftm', 'fta', 'fga', 'fgm', 'ft_per', 'fg_per',
		            'min']:
			cols.remove(col)
		
		for col in cols:
			col_zscore = col + '_zscore'
			top = df.sort_values(by=col, ascending=False).head(350)
			drop_na_col = top[col]
			if col == "TO":
				df[col_zscore] = (drop_na_col - drop_na_col.mean()) / drop_na_col.std(ddof=1) * -1
			else:
				df[col_zscore] = (drop_na_col - drop_na_col.mean()) / drop_na_col.std(ddof=1)
		
		df = df.fillna(0)
		
		df["Total_zscore"] = df["ast_zscore"] + df["fg3m_zscore"] + df["pts_zscore"] + df["reb_zscore"] + df[
			"stl_zscore"] + \
		                     df["blk_zscore"] + df['TO_zscore'] + df['ft_weighted_zscore'] + df['fg_weighted_zscore']
		df['Total Rank'] = df['Total_zscore'].rank(ascending=False).astype(int)
		
		df = df.set_index('Total Rank')
		
		df = df.drop(
			['GP_zscore', 'blk_zscore', 'fg3m_zscore', 'ast_zscore', 'reb_zscore', 'stl_zscore', "TO_zscore",
			 "ft_weighted",
			 "fg_weighted", "pts_zscore", "ft_weighted_zscore", "fg_weighted_zscore", "Eligible positions"], axis=1)
		
		print(df.sort_values(by="Total Rank", ascending=True).head(count))
	
		# df = df[['name', 'ast_zscore', 'blk_zscore', 'fg3m_zscore', 'pts_zscore', 'reb_zscore', 'stl_zscore',
		# 'ft_weighted_zscore', 'fg_weighted_zscore', 'turnover_zscore', 'Total_zscore']]
		
		# df1 = df[df["Roster status"]].isin(["Chuck it for buckets", "Dame Time"])
		
		# print(df1.sort_values(by="My Rank", ascending=True))
		
		# #df = df[df["Roster status"] != "FA"]
	
	@staticmethod
	def combine_stats_with_owner(player_stats, owner_list):
		owned_yahoo_keys = owner_list.keys()
		keys = player_stats.keys()
		
		new_dic = {}
		
		for key in keys:
			player = player_stats[key]
			yahoo_id = str(player['yahoo_id'])
			if yahoo_id in owned_yahoo_keys:
				player_ownership_info = owner_list[yahoo_id]
				if "owner_team_name" in player_ownership_info:
					owner_team_name = player_ownership_info['owner_team_name']
					player['owner_team_name'] = owner_team_name
			
			new_dic[key] = player
		
		return new_dic