from utils import Utils


class Formatter:
	def __init__(self):
		self.utils = Utils()

	def combine_player_stats_dic(self, player_dic):
		print("Started data formatting")
		clean_lst = []
		for player in player_dic.items():
			if "games" in player[1]:
				clean_lst = clean_lst + [player[1]]

		averages = []
		games_stats_num = 0
		for player in clean_lst:

			no_missed = self.remove_missed_games(player['games'])
			all_player_games = self.remove_todays_games(no_missed)

			new_player = {
					"Name": player["name"],
					"Roster status": player['owner_team_name'] if "owner_team_name" in player else "FA",
					"IS": player["injury_status"],
					"Eligible positions": self.remove_some_positions(player["eligible_positions"]),
					'GP': len(all_player_games)
				}

			game_stats = self.merge_game_stats(all_player_games)

			games_stats_num = games_stats_num + len(game_stats)

			new_player = {**new_player, **game_stats}

			averages.append(new_player)

		print("Finished data formatting")
		print("Players: " + str(len(averages)))
		return averages

	def remove_some_positions(self, position_list):
		removable_positions = ["Util", "G", "F", "IL"]
		new_list = []
		for position in position_list:
			if position not in removable_positions:
				new_list.append(position)
		return new_list

	def remove_missed_games(self, games):
		new_games = []
		for game in games:
			if game['min'] != "" and game["min"] != "0" and game['min'] != '0:00':
				new_games.append(game)
		return new_games

	def remove_todays_games(self, games):
		return games
		# new_games = []
		# for game in games:
		# 	if game['game']['date'] != '2021-01-10T00:00:00.000Z':
		# 		new_games.append(game)
		# return new_games

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







