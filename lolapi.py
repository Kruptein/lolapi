import requests


class LolAPI:
	base = "https://prod.api.pvp.net/api/lol/"
	def __init__(self, key):
		self.key = key