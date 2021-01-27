import pandas as pd

from utils import Utils


class Formatter:
	def __init__(self):
		self.utils = Utils()
	
	@staticmethod
	def all_stats_raw_with_owner(player_stats, owner_list):
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
		
	def pandas_player_games(self, player_stats, owner_list):
		all_stats_raw_with_owner = self.all_stats_raw_with_owner(player_stats, owner_list)
		games = self.get_player_games(all_stats_raw_with_owner)
		
		return pd.DataFrame(games)
	
	def get_player_games(self, all_stats_raw_with_owner):
		games_list = []
		for player in self.get_players_with_min_one_game(all_stats_raw_with_owner):
			all_played_games = self.remove_missed_games(player['games'])
			for game in all_played_games:
				new_game = {
					#"yahoo_id": player["yahoo_id"],
					"name": player["name"],
					"fg_pct": game["fg_pct"],
					"ft_pct": game["ft_pct"],
					"fg3m": game["fg3m"],
					"pts": game["pts"],
					"reb": game["reb"],
					"ast": game["ast"],
					"stl": game["stl"],
					"blk": game["blk"],
					"to": game["turnover"],
					"date": game["game"]["date"][0:10]
				}
				games_list.append(new_game)
		return games_list
		
	def pandas_player_averages(self, player_stats, owner_list):
		raw_stats = self.all_stats_raw_with_owner(player_stats, owner_list)
		combined = self.get_player_averages(raw_stats)
		return pd.DataFrame(combined)

	def get_player_averages(self, player_dic):
		averages = []
		for player in self.get_players_with_min_one_game(player_dic):

			all_played_games = self.remove_missed_games(player['games'])

			new_player = {
					"Name": player["name"],
					"Roster status": player['owner_team_name'] if "owner_team_name" in player else "FA",
					"IS": player["injury_status"],
					"Eligible positions": self.remove_some_positions(player["eligible_positions"]),
					'GP': len(all_played_games)
				}

			averages.append({**new_player, **self.merge_game_stats(all_played_games)})  # Merge player with averages

		print("Players: " + str(len(averages)))
		return averages

	@staticmethod
	def get_players_with_min_one_game(player_dic):
		clean_lst = []
		for player in player_dic.items():
			if "games" in player[1]:
				clean_lst = clean_lst + [player[1]]
		return clean_lst

	@staticmethod
	def remove_some_positions(position_list):
		removable_positions = ["Util", "G", "F", "IL"]
		new_list = []
		for position in position_list:
			if position not in removable_positions:
				new_list.append(position)
		return new_list

	@staticmethod
	def remove_missed_games(games):
		new_games = []
		for game in games:
			if game['min'] != "" and game["min"] != "0" and game['min'] != '0:00':
				new_games.append(game)
		return new_games

	def merge_game_stats(self, games):
		entry = { 
				'pts': 0,
				'fg3m': 0,
				'reb': 0,
				'ast': 0,
				'stl': 0,
				'blk': 0,
				# 'dreb': 0,
				# 'fg3a': 0,
				'fga': 0,
				'fgm': 0,
				'ftm': 0,
				'fta': 0,
				'min': 0,
				# 'oreb': 0,
				# 'pf': 0,
				'TO': 0
		}
		if len(games) == 0:
			return entry

		for game in games:
			for key in entry.keys():
				if key == "min":
					entry[key] = entry[key] + self.get_sec(game[key])
				elif key == "TO":
					entry[key] = int(entry[key]) + int(game["turnover"])
				else:
					entry[key] = int(entry[key]) + int(game[key])

		for key in entry.keys():
			if key == "min":
				entry[key] = round(entry[key]/len(games)/60, 2)
			else:
				entry[key] = round(entry[key]/len(games), 2)

		return entry

	def get_sec(self, time_str):
		if str(time_str) == "0":
			return 0
		m, s = str(time_str).split(':')
		return int(m) * 60 + int(s)

