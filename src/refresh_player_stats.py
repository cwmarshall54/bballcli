#!/usr/bin/python3

import os
import sys

import pandas as pd
import unidecode
import click

from utils import Utils
from yahoo_get import YahooAPI
from bball_api import BBallAPI
from formatter import Formatter


formatter = Formatter()
utils = Utils()
yahoo_API = YahooAPI()
bball_API = BBallAPI()
pd.set_option("display.max_rows", None)


def refresh_player_stats():
	players_with_stats = bball_API.refresh_2021_season_player_stats()
	utils.write_file("player_stats_index.json", players_with_stats)
	return players_with_stats

def get_ownership_of_taken_players():
	owner_list = yahoo_API.ownership_of_taken_players()
	utils.write_file("owner_index.json", owner_list)
	return owner_list



def combine_stats_with_owner(refresh=False):
	player_stats = {}
	owner_list = []

	if refresh:
		player_stats = refresh_player_stats()
		owner_list = get_ownership_of_taken_players()
	else:
		player_stats = utils.read_file("player_stats_index.json")
		owner_list = utils.read_file("owner_index.json")

	owned_yahoo_keys = owner_list.keys()
	keys = player_stats.keys()

	new_dic = {}

	for key in keys:
		player = player_stats[key]
		yahoo_id = str(player['yahoo_id'])
		if yahoo_id in owned_yahoo_keys:
			player_ownership_info = owner_list[yahoo_id]
			if "owner_team_name" in player_ownership_info:
				print(player_ownership_info)
				owner_team_name = player_ownership_info['owner_team_name']
				player['owner_team_name'] = owner_team_name

		new_dic[key] = player

	return new_dic

def trade_machine(df, my_players, their_players):
	my_df = df[df["Name"].isin(my_players)]
	their_df = df[df["Name"].isin(their_players)]

	utils.print(my_df.sort_values(by="My Rank", ascending=True))
	print("")
	utils.print(their_df.sort_values(by="My Rank", ascending=True))

@click.command()
def player_averages():
	raw_stats = combine_stats_with_owner()

	combined = formatter.combine_player_stats_dic(raw_stats)

	df = pd.DataFrame(combined)

	df = df[df['min'] > 5]

	df['ft_per'] = df['ftm']/df['fta']
	df['ft_weighted'] = (df['ft_per'] - df['ft_per'].mean()) * df['ftm']

	df['fg_per'] = df['fgm']/df['fga']
	df['fg_weighted'] = (df['fg_per'] - df['fg_per'].mean() ) * df['fgm']

	cols = list(df.columns)

	for col in ['Roster status', 'Name', "IS", "Eligible positions", 'ftm', 'fta', 'fga', 'fgm', 'ft_per', 'fg_per', 'min']:
		cols.remove(col)


	for col in cols:
		col_zscore = col + '_zscore'
		top = df.sort_values(by=col, ascending=False).head(350)
		drop_na_col = top[col]
		if col == "TO":
			df[col_zscore] = (drop_na_col - drop_na_col.mean())/drop_na_col.std(ddof=1) * -1
		else:
			df[col_zscore] = (drop_na_col - drop_na_col.mean())/drop_na_col.std(ddof=1)

	df = df.fillna(0)

	df["Total_zscore"] = df["ast_zscore"]  + df["fg3m_zscore"] + df["pts_zscore"] + df["reb_zscore"] + df["stl_zscore"] + df["blk_zscore"] + df['TO_zscore'] + df['ft_weighted_zscore'] + df['fg_weighted_zscore']
	df['Total Rank'] = df['Total_zscore'].rank(ascending=False).astype(int)


	df["My_zscore"] = df["stl_zscore"]  + df["fg3m_zscore"] + df["pts_zscore"] + df["reb_zscore"] + df["ast_zscore"] + df['ft_weighted_zscore']
	df['My Rank'] = df['My_zscore'].rank(ascending=False).astype(int)
	df['diff'] = df['Total Rank'] - df['My Rank']
	df = df.set_index('Total Rank')

	df = df.drop(['GP_zscore', 'blk_zscore', 'fg3m_zscore', 'ast_zscore', 'reb_zscore', 'stl_zscore', "TO_zscore", "ft_weighted",  "fg_weighted", "pts_zscore", "ft_weighted_zscore", "fg_weighted_zscore", "Eligible positions"], axis=1)

	print(df.sort_values(by="Total Rank", ascending=True))

	#df = df[['name', 'ast_zscore', 'blk_zscore', 'fg3m_zscore', 'pts_zscore', 'reb_zscore', 'stl_zscore', 'ft_weighted_zscore', 'fg_weighted_zscore', 'turnover_zscore', 'Total_zscore']]

	# df1 = df[df["Roster status"]].isin(["Chuck it for buckets", "Dame Time"])

	# print(df1.sort_values(by="My Rank", ascending=True))

	# #df = df[df["Roster status"] != "FA"]

if __name__ == '__main__':
	player_averages()


	



