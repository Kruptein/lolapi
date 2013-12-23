import requests

class LolAPI:
	base = "https://prod.api.pvp.net/api/lol/"
	def __init__(self, key, region="euw"):
		self.key = key
		self.region = region #default region

	def get_champions(self, region="default", freetoplay=False):
		if region == "default":
			region = self.region
		return requests.get(LolAPI.base + "{}/v1.1/champion?freeToPlay={}&api_key={}".format(region, str(freetoplay).lower(), self.key)).json()

	def get_recent_games(self, summonerId, region="default"):
		if region == "default":
			region = self.region
		return requests.get(LolAPI.base + "{}/v1.2/game/by-summoner/{}/recent?api_key={}".format(region, summonerId, self.key)).json()

	def get_league(self, summonerId, region="default"):
		if region == "default":
			region = self.region
		return requests.get(LolAPI.base + "{}/v2.2/league/by-summoner/{}?api_key={}".format(region, summonerId, self.key)).json()

	def get_stats(self, summonerId, region="default"):
		if region == "default":
			region = self.region
		return requests.get(LolAPI.base + "{}/v1.2/stats/by-summoner/{}/summary?api_key={}".format(region, summonerId, self.key)).json()

	def get_ranked_stats(self, summonerId, region="default"):
		if region == "default":
			region = self.region
		return requests.get(LolAPI.base + "{}/v1.2/stats/by-summoner/{}/ranked?api_key={}".format(region, summonerId, self.key)).json()

	def get_masteries(self, summonerId, region="default"):
		if region == "default":
			region = self.region
		return requests.get(LolAPI.base + "{}/v1.2/summoner/{}/masteries?api_key={}".format(region, summonerId, self.key)).json()

	def get_runes(self, summonerId, region="default"):
		if region == "default":
			region = self.region
		return requests.get(LolAPI.base + "{}/v1.2/summoner/{}/runes?api_key={}".format(region, summonerId, self.key)).json()

	def get_summoner_by_name(self, name, region="default"):
		if region == "default":
			region = self.region
		return requests.get(LolAPI.base + "{}/v1.2/summoner/by-name/{}?&api_key={}".format(region, name, self.key)).json()

	def get_summoner_by_id(self, summonerId, region="default"):
		if region == "default":
			region = self.region
		return requests.get(LolAPI.base + "{}/v1.2/summoner/{}?api_key={}".format(region, summonerId, self.key)).json()

	def get_names(self, summonerIds, region="default"):
		if region == "default":
			region = self.region
		return requests.get(LolAPI.base + "{}/v1.2/summoner/{}/name&api_key={}".format(region, summonerIds, self.key)).json()

	def get_teams(self, summonerId, region="default"):
		if region == "default":
			region = self.region
		return requests.get(LolAPI.base + "{}/v2.2/team/by-summoner/{}&api_key={}".format(region, summonerId, self.key)).json()