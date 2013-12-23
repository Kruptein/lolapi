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