import requests

class LolAPI:
	base = "https://prod.api.pvp.net/api/lol/"
	def __init__(self, key, region="euw"):
		self.key = key
		self.region = region #default region

	