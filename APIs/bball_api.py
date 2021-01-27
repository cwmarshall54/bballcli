import requests

from utils import Utils
from APIs.bball_parser import BBallParser

BASE_ENDPOINT = "https://www.balldontlie.io/api/v1/"


class BBallAPI:
	def __init__(self):
		self.base_Endpoint = BASE_ENDPOINT
		self.utils = Utils()
		self.bball_parser = BBallParser()

	def refresh_2021_season_player_stats(self):
		all_player_stats_index = self.utils.read_file("player_stats_index.json")
		last_update_date = self.utils.read_file('last_update.json')[0]
		current_date = self.utils.get_curr_date()

		player_info_list = self.utils.read_file("merged_player_list.json")

		new_player_stats_raw = self.get_player_stats_raw(player_info_list, last_update_date, current_date)
		new_player_stats_index = self.bball_parser.clean_and_index_player_stats(player_info_list, new_player_stats_raw)

		self.utils.write_file("last_update.json", [current_date])

		return self.bball_parser.merge_player_stat_indexs(all_player_stats_index, new_player_stats_index)

	# Gets all game stats for a given player_id
	def get_player_stats_raw(self, player_info_list, last_update_date, current_date):
		player_bball_ids = [player['bball_id'] for player in player_info_list]

		first_set = self.get_player_list_game_stats(player_bball_ids[0:250], last_update_date, current_date, True)

		removed_dups = self.remove_player_list_dups(first_set, self.get_player_list_game_stats(player_bball_ids[250:], last_update_date, current_date))

		return removed_dups

	def remove_player_list_dups(self, player_list_1, player_list_2):
		game_ids = []
		new_player_list = []
		combined_game_stats = player_list_1 + player_list_2

		for game in combined_game_stats:
			if str(game['id']) not in game_ids:
				game['id'] = str(game['id'])
				new_player_list = new_player_list + [game]
				game_ids = game_ids + [str(game['id'])]
		return new_player_list

	# Gets all game stats for a given player_id
	def get_player_list_game_stats(self, player_ids, last_update_date, current_date, first=False):
		game_list = []
		more_pages = True
		curr_page = 1
		total_pages = -1
		
		while more_pages:
			raw_json = self.get_player_game_stats(curr_page, '2020', last_update_date, current_date, player_ids)
			try:
				total_pages = raw_json['meta']['total_pages']
				curr_page = raw_json['meta']['current_page']
				game_list = game_list + raw_json['data']

				if first and curr_page == 1:
					print("Total pages to download: " + str(total_pages * 2))
					first = False

			except TypeError as e:
				self.utils.print(e)
				print('Parsing JSON has failed')

			more_pages = not curr_page == total_pages
			curr_page += 1
			print("Downloading...")
		return game_list

	def get_player_game_stats(self, page, season, start_date, end_date, player_ids):
		try:
			return requests.get(self.base_Endpoint + 'stats?', data={
				'season': season,
				'per_page': 99,  # max
				'page': page,
				'start_date': start_date,
				'end_date': end_date,
				'player_ids': player_ids
			}).json()
		except ValueError as e:
			self.utils.print(e)
		except requests.exceptions.RequestException as e:
			self.utils.print(e)

	# Gets all player ids for every player since 1979
	def get_all_player_ids(self):
		def add_player_to_dict(player_dict, new_player_list):
			for player in new_player_list:
				player_name = (player['first_name'] + player['last_name']).lower().replace(" ", "").replace(".", "").replace("'", "")
				player_dict[player_name] = player['id']
			return player_dict

		page = 1
		player_dict = {}

		json = requests.get(self.base_Endpoint + 'players?per_page=99&page=' + str(page)).json()

		data = json['data']
		meta = json['meta']
		total_pages = meta['total_pages']

		player_dict = add_player_to_dict(player_dict, data)

		for i in range(2, total_pages+1):
			json = requests.get(self.base_Endpoint + 'players?per_page=99&page=' + str(i)).json()
			data = json['data']
			player_dict = add_player_to_dict(player_dict, data)

		return player_dict
