#!/usr/bin/python3

import os
import sys

import pandas as pd
from utils import Utils
from bball_get import BBallAPI
from formatter import Formatter

utils = Utils()
formatter = Formatter()
pd.set_option("display.max_rows", None)

columns = ['FG%', 'FT%', '3PM', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TO']
rank_columns = ['FG% Rank', 'FT% Rank', '3PM Rank', 'PTS Rank', 'REB Rank', 'AST Rank', 'STL Rank', 'BLK Rank', 'TO Rank']

def generate_team_ranks(df):
	for column in columns:
		df = df.sort_values(by=column, ascending=(column!='TO'))
		df.loc[:, (column + " Rank")] = utils.order_list(df[column].tolist())
	df.loc[:, ("Total Rank")] = df[rank_columns].sum(axis=1)
	return df.sort_values(by="Total Rank", ascending=False)

def parse_week_matchups(week):
	data = utils.flatten_week(utils.read_file('week_' + str(week) + '.json'))
	return generate_team_ranks(pd.DataFrame.from_dict(data, orient='index'))

def parse_all_matchups():
	all_data = parse_week_matchups(1)
	for week_num in range(2, utils.get_curr_week() + 1):
		week_data = parse_week_matchups(week_num)
		all_data = utils.combine_weeks(all_data, week_data)
	return generate_team_ranks(all_data)



# Player analytics










