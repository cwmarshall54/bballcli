#!/usr/bin/python3

import os
import sys

import pandas as pd
from utils import Utils
from yahoo_get import YahooAPI

utils = Utils()
yahoo_API = YahooAPI()
pd.set_option("display.max_rows", None)

columns = ['FG%', 'FT%', '3PM', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TO']
rank_columns = ['FG% Rank', 'FT% Rank', '3PM Rank', 'PTS Rank', 'REB Rank', 'AST Rank', 'STL Rank', 'BLK Rank', 'TO Rank']

def yahoo_get_current_league_matchups():
	curr_week = utils.get_curr_week()
	league_matchups = yahoo_API.get_matchups(curr_week)
	utils.write_file("week_" + str(curr_week) + ".json", league_matchups)

def generate_team_ranks(df):
	for column in columns:
		df = df.sort_values(by=column, ascending=(column!='TO'))
		df.loc[:, (column + " Rank")] = utils.order_list(df[column].tolist())
	df.loc[:, ("Total Rank")] = df[rank_columns].sum(axis=1)
	return df.sort_values(by="Total Rank", ascending=False)

def generate_better_team_ranks(df):
	for column in columns:
		df = df.sort_values(by=column, ascending=(column!='TO'))
		df.loc[:, (column + " Rank")] =  recreate_list(df[column].tolist(), df, column)

	df.loc[:, ("Top 6 Rank")] = drop_three_lowest(df)
	df.loc[:, ("Total Rank")] = df[rank_columns].sum(axis=1)
	return df.sort_values(by="Total Rank", ascending=False)

def recreate_list(lst, df, column):
	worst = df[column].iloc[0]
	best = df[column].iloc[9]
	coe = (worst/best)*10

	new_lst = []
	for item in lst:
		val = round((9/(best - worst)) * (item - best) + 10, 2)
		new_lst.append(val)
	return new_lst

def drop_three_lowest(df):
	df = df.drop(["FGM/A", "FG%", "FTM/A", "FT%", "3PM", "PTS", "REB",  "AST",  "STL",  "BLK",   "TO"], axis=1)
	series = []
	for row_num in range(0, 10):
		lst = df.iloc[row_num].tolist()
		lst.sort()
		series.append(round(sum(lst[3:9]), 2))

	return series


def parse_all_matchups():
	all_data = parse_week_matchups(1)
	for week_num in range(2, utils.get_curr_week() + 1):
		week_data = parse_week_matchups(week_num)
		all_data = utils.combine_weeks(all_data, week_data)
	return all_data.set_index('name')

def parse_week_matchups(week):
	data = utils.flatten_week(utils.read_file('week_' + str(week) + '.json'))
	return pd.DataFrame.from_dict(data, orient='index')

if __name__ == '__main__':
	yahoo_get_current_league_matchups()
	#df = generate_team_ranks(parse_week_matchups(4).set_index('name'))
	df = generate_better_team_ranks(parse_all_matchups())
	print(df)




