import requests

from utils import Utils
from APIs.bball_parser import BBallParser

# https://api.the-odds-api.com/odds?sport=americanfootball_nfl&region=us&apiKey=...
BASE_ENDPOINT = "https://api.the-odds-api.com/v3/odds?"
key = "e449e0807324a72e80c20c5d5f405356"


class OddsAPI:
	def __init__(self):
		self.base_Endpoint = BASE_ENDPOINT
		self.utils = Utils()
		self.bball_parser = BBallParser()
		
	def command(self, refresh=False):
		self.get_in_season_sports(refresh)
		
	def get(self, prefix, headers):
		try:
			r = requests.get(self.base_Endpoint + prefix + '?', data=headers)
			self.utils.print(r)
			return r
		except ValueError as e:
			self.utils.print(e)
		except requests.exceptions.RequestException as e:
			self.utils.print(e)
			
	def create_in_season_sports_header(self):
		return {
			'api_key': key
		}
	
	def get_in_season_sports(self, refresh=False):
		prefix = "sports"
		if refresh:
			in_season_sports = self.get(prefix, self.create_in_season_sports_header())
			self.utils.write_file('in_season_sports.json', in_season_sports)
			return in_season_sports
		
		in_season_sports = self.utils.read_file('in_season_sports.json')
		self.utils.print(in_season_sports)
		return in_season_sports
