from utils import Utils


class BBallParser:
	def __init__(self):
		self.utils = Utils()

	def merge_player_stat_indexs(self, all_player_stats_index, new_player_stats_index):
		keys = list(all_player_stats_index.keys())
		replace_count = 0
		new_count = 0
		older_count: int = 0

		for player in new_player_stats_index.values():
			bball_id = str(player['bball_id'])
			if bball_id in keys:
				index_player = all_player_stats_index[bball_id]
				if "games" in player and "games" in index_player:
					index_player['games'] = self.merge_game_list(index_player['games'], player['games'])
					replace_count += 1
				elif "games" in player:
					index_player['games'] = player['games']
					new_count += 1
				else:
					older_count += 1
			else:
				if "games" in player:
					all_player_stats_index[bball_id] = player
					new_count += 1

		return all_player_stats_index

	@staticmethod
	def merge_game_list(old_games_list, new_game_list):
		changed_games_ids_list = []
		changed_games = []
		for old_game in old_games_list:
			for new_game in new_game_list:
				if str(new_game['id']) == str(old_game['id']):
					changed_games_ids_list.append(str(new_game['id']))
					changed_games.append(new_game)

		combined_list = old_games_list + new_game_list
		refreshed_list = []
		for game in combined_list:
			if game['id'] not in changed_games_ids_list:
				game['id'] = str(game['id'])
				refreshed_list.append(game)

		return refreshed_list + changed_games

	def clean_and_index_player_stats(self, player_info_list, player_stats):
		index_list = {}
		for info in player_info_list:
			if "bball_id" in info:
				index_list[str(info['bball_id'])] = info
		return self.add_to_index_list(index_list, player_stats)

	@staticmethod
	def add_to_index_list(index_list, player_stats):
		keys = index_list.keys()
		for game in player_stats:
			game_player_id = str(game['player']['id'])

			if game_player_id in keys:
				if "games" not in (index_list[game_player_id].keys()):
					index_list[game_player_id]['games'] = [game]
				else:
					index_list[game_player_id]['games'] = index_list[game_player_id]['games'] + [game]

		return index_list



