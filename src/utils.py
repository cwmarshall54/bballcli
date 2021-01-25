import pprint
import json
import pandas as pd
from datetime import date

pd.options.mode.chained_assignment = None
file_path = "/Users/chasemarshall1/Desktop/fantasybball/"

curr_week = 5


class Utils:
	def __init__(self):
		self.stat_ids = {
			"9004003": "FGM/A",
			"5": "FG%",
			"9007006": "FTM/A",
			"8": "FT%",
			"10": "3PM",
			"12": "PTS",
			"15": "REB",
			"16": "AST",
			"17": "STL",
			"18": "BLK",
			"19": "TO"
		}
		self.curr_week = curr_week
		self.file_path = file_path
		self.pp = pprint.PrettyPrinter(indent=4)

	def get_curr_week(self):
		return self.curr_week

	def get_curr_date(self):
		return date.today().strftime("%Y-%m-%d")

	def get_out_file_path(self):
		return self.file_path + "out/"

	def get_yahoo_key_file(self):
		return self.file_path + "config/yahoo_api_key.json"

	def get_num_cols(self):
		return list(self.stat_ids.values())[4:]

	def get_str_cols(self):
		return list(self.stat_ids.values())[:4]

	def write_file(self, file_name, data):
		print("Started writing: " + file_name)
		with open(self.get_out_file_path() + file_name, 'w') as outfile:
			json.dump(data,  outfile)
			print("Finished writing: " + file_name)

	def read_file(self, file_name):
		print("Started reading: " + file_name)
		with open(self.get_out_file_path() + file_name) as json_file:
			file = json.load(json_file)
			print("Finished reading: " + file_name)
			return file

	def print(self, data):
		self.pp.pprint(data)

	def order_list(self, lst):
		new_lst = []
		roll_lst = []
		i = 0
		while i < len(lst):
			item = lst[i]
			item2 = lst[i+1]

			roll_lst.append(i+1) # index1 + 1

			if (item != item2):
				new_lst = new_lst + self.combine(roll_lst)
				roll_lst = []


			if (i+2 == len(lst)): # end of lst
				if (item == item2):
					roll_lst.append(i+2) # last index
					new_lst = new_lst + self.combine(roll_lst)
				elif(len(roll_lst) == 0):
					new_lst.append(i+2)
				else:
					new_lst.append(self.combine(roll_lst))
				i += 1
			i += 1
		return new_lst

	def combine(self, lst):
		new_lst = []
		average = sum(lst)/len(lst)
		for x in range(len(lst)):
			new_lst.append(average)
		return new_lst

	def get_player_ids(self, old_data):
		data = []
		for item in old_data:
			data.append(item['player_id'])
		return data

	def flatten_week(self, old_data):
		stats = {}
		count = 0
		data = old_data['fantasy_content']['league'][1]['scoreboard']['0']['matchups']
		for item in data.items():
			first = item[1]
			if(type(first) == dict):
				if(first['matchup']):

					player1 = first['matchup']['0']['teams']['0']['team'][0][1]['team_id']
					player2 = first['matchup']['0']['teams']['1']['team'][0][1]['team_id']

					player1Name = first['matchup']['0']['teams']['0']['team'][0][2]['name']
					player2Name = first['matchup']['0']['teams']['1']['team'][0][2]['name']

					player1_stats = first['matchup']['0']['teams']['0']['team'][1]['team_stats']['stats']
					player2_stats = first['matchup']['0']['teams']['1']['team'][1]['team_stats']['stats']

					p1_final_list = {}
					p2_final_list = {}

					p1_final_list["name"] = player1Name
					p2_final_list["name"] = player2Name

					for stat_num in range(0, 11):
						p1_stat_line = player1_stats[stat_num]['stat']
						p2_stat_line = player2_stats[stat_num]['stat']
						p1_stat_id = self.stat_ids[p1_stat_line['stat_id']]
						p2_stat_id = self.stat_ids[p2_stat_line['stat_id']]
						p1_stat_value = p1_stat_line['value']
						p2_stat_value = p2_stat_line['value']
						p1_final_list[p1_stat_id] = p1_stat_value
						p2_final_list[p2_stat_id] = p2_stat_value
					stats[player1] = p1_final_list
					count += 1

					stats[player2] = p2_final_list
					count += 1
		return stats

	def stat_tuple(self, stat1, stat2):
		stat1 = stat1.split('/')
		stat2 = stat2.split('/')
		return int(stat1[0]) + int(stat2[0]), int(stat1[1]) + int(stat2[1])

	def combine_cat_stat(self, df1, df2, cat):
		return df1[cat].combine(df2[cat], self.combine_stat)

	def combine_cat_count(self, df1, df2, cat):
		return df1[cat].combine(df2[cat], self.combine_count_stat)

	def combine_stat(self, stat1, stat2):
		fma = self.stat_tuple(stat1, stat2)
		return round(fma[0]/fma[1], 3)

	def combine_count_stat(self, stat1, stat2):
		fma = self.stat_tuple(stat1, stat2)
		return str(fma[0]) + '/' + str(fma[1])

	def combine_weeks(self, df1, df2):
		df1 = df1.sort_index()
		df2 = df2.sort_index()

		str_df = df1[self.get_str_cols()]

		str_df.loc[:, ('FG%')] = self.combine_cat_stat(df1, df2, 'FGM/A')
		str_df.loc[:, ('FGM/A')] = self.combine_cat_count(df1, df2, 'FGM/A')
		str_df.loc[:, ('FT%')] = self.combine_cat_stat(df1, df2, 'FTM/A')
		str_df.loc[:, ('FTM/A')] = self.combine_cat_count(df1, df2, 'FTM/A')
		str_df.loc[:, ('name')] = df1['name']

		count_df = df1[self.get_num_cols()].apply(pd.to_numeric).add(df2[self.get_num_cols()].apply(pd.to_numeric))

		return pd.concat([str_df, count_df], axis=1)


