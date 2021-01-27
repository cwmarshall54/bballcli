from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa

from utils import Utils

yahoo_league_id = '402.l.70097'
yahoo_positions = ["PG", "SG", "SF", "PF", "C"]


class YahooAPI:
	def __init__(self):
		self.yahoo_league_id = yahoo_league_id
		self.League = None
		self.utils = Utils()

	# Get a league per a yahoo_league_id
	def get_league(self):
		if self.League is None:
			oauth = OAuth2(None, None, from_file=self.utils.get_yahoo_key_file())
			self.League = yfa.League(oauth, yahoo_league_id)
		return self.League

	# Get all fantasy teams in a league
	def get_teams(self):
		return self.get_league().teams()

	# Get all fantasy match ups for a given week with corresponding weekly stats
	def get_match_ups(self, week):
		return self.get_league().matchups(week)

	def ownership_of_taken_players(self):
		player_ids = self.utils.get_player_ids(self.get_taken_players())
		player_id_length = len(player_ids)

		ownership_lst = {}
		per_page = 24
		for i in range(0, int(len(player_ids)/per_page)+1):
			lower = i * 24
			higher = (24*i+24) if (24*i+24) < player_id_length else player_id_length
			lst_to_add = self.get_ownership(player_ids[lower:higher])
			ownership_lst = {**ownership_lst, **lst_to_add}

		return ownership_lst

	# Get all rostered players in a league MAX=25
	def get_ownership(self, player_ids):
		return self.get_league().ownership(player_ids)

	# Get all rostered players in a league
	def get_taken_players(self):
		return self.get_league().taken_players()

	# Get all players on waivers in a league
	def get_waivered_players(self):
		return self.get_league().waivers()

	# Get all players that are free agents in a league given a position
	def get_free_agent_positional_players(self, position):
		return self.get_league().free_agents(position)

	# Get all players that are free agents in a league	
	def get_all_free_players_with_dups(self):
		players = []
		for position in yahoo_positions:
			players = players + self.get_free_agent_positional_players(position)
		return players

	def create_player_with_key_attrs(self, player, status):
		return {
			'name': player['name'].lower(),
			'yahoo_id': player['player_id'],
			'roster_status': status,
			'injury_status': player['status'],
			'percent_owned': player['percent_owned'],
			'eligible_positions': player['eligible_positions']
		}

	# Get all players in yahoo (no dups)
	def get_all_players_no_dup(self):
		taken_players = self.get_taken_players()
		waived_players = self.get_waivered_players()
		free_agents = self.get_all_free_players_with_dups()
		player_name_list = []
		players = []
		for player in taken_players:
			player_name = player['name']
			if (player_name not in player_name_list):
				player_name_list.append(player_name)
				players.append(self.create_player_with_key_attrs(player, "R"))

		for player in waived_players:
			player_name = player['name']
			if (player_name not in player_name_list):
				player_name_list.append(player_name)
				players.append(self.create_player_with_key_attrs(player, "W"))

		for player in free_agents:
			player_name = player['name']
			if (player_name not in player_name_list):
				player_name_list.append(player_name)
				players.append(self.create_player_with_key_attrs(player, "F"))

		return players

	# Get season stats for all players in a list of player_ids
	def get_curr_season_player_stats(self, player_ids):
		return self.get_league().player_stats(player_ids, 'season')

	# Get player details given a player name
	def get_player_details(self, player_name):
		return self.get_league().player_details(player_name)
