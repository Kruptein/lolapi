import requests
import inspect
import functools


#Decorators
def regionDecorator(func):
    
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        d = inspect.getcallargs(func, self, *args, **kwargs)
        if d["region"] == None:
            d["region"] = self.region
        del d["self"]
        return func(self, **d)
    return wrapper

class LolAPI:
    base = "https://prod.api.pvp.net/api/lol/"
    def __init__(self, key, region="euw", summonerId=-1):
        self.key = key
        self.region = region #default region

    @regionDecorator
    def get_champions(self, region=None, freetoplay=False):
        return requests.get(LolAPI.base + "{}/v1.1/champion?freeToPlay={}&api_key={}".format(region, str(freetoplay).lower(), self.key)).json()

    @regionDecorator
    def get_recent_games(self, summonerId, region=None):
        return requests.get(LolAPI.base + "{}/v1.2/game/by-summoner/{}/recent?api_key={}".format(region, summonerId, self.key)).json()

    @regionDecorator
    def get_league(self, summonerId, region=None):
        return requests.get(LolAPI.base + "{}/v2.2/league/by-summoner/{}?api_key={}".format(region, summonerId, self.key)).json()

    @regionDecorator
    def get_stats(self, summonerId, region=None):
        return requests.get(LolAPI.base + "{}/v1.2/stats/by-summoner/{}/summary?api_key={}".format(region, summonerId, self.key)).json()

    @regionDecorator
    def get_ranked_stats(self, summonerId, region=None):
        return requests.get(LolAPI.base + "{}/v1.2/stats/by-summoner/{}/ranked?api_key={}".format(region, summonerId, self.key)).json()

    @regionDecorator
    def get_masteries(self, summonerId, region=None):
        return requests.get(LolAPI.base + "{}/v1.2/summoner/{}/masteries?api_key={}".format(region, summonerId, self.key)).json()

    @regionDecorator
    def get_runes(self, summonerId, region=None):
        return requests.get(LolAPI.base + "{}/v1.2/summoner/{}/runes?api_key={}".format(region, summonerId, self.key)).json()

    @regionDecorator
    def get_summoner_by_name(self, name, region=None):
        return requests.get(LolAPI.base + "{}/v1.2/summoner/by-name/{}?&api_key={}".format(region, name, self.key)).json()

    @regionDecorator
    def get_summoner_by_id(self, summonerId, region=None):
        return requests.get(LolAPI.base + "{}/v1.2/summoner/{}?api_key={}".format(region, summonerId, self.key)).json()

    @regionDecorator
    def get_names(self, summonerIds, region=None):
        return requests.get(LolAPI.base + "{}/v1.2/summoner/{}/name?api_key={}".format(region, summonerIds, self.key)).json()
    
    @regionDecorator
    def get_teams(self, summonerId, region=None):
        return requests.get(LolAPI.base + "{}/v2.2/team/by-summoner/{}?api_key={}".format(region, summonerId, self.key)).json()