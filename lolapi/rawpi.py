import os
import json
import requests

from functools import wraps

from .limit import redis_wrap
from .utils import QueryBuilder

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# THIS HANDLES NO ERRORS AND IS JUST A RAW CONNECTION TO THE LOL API;
# USE THE API MODULE TO GET ERROR FALLBACK METHODS

with open(os.path.join(__location__, 'config'), 'r') as f:
    try:
        config = json.load(f)
    except ValueError: config = {'key': ""}

DEFAULT_VALUES = {
    'region': 'euw1',
    'locale': 'en_US'
}
GLOBAL_ENDPOINT = "https://global.api.pvp.net/api/lol/static-data/{0}/"
REGION_ENDPOINT = "https://{0}.api.riotgames.com/lol/"

HEADERS = { "X-Riot-Token": config["key"] }


def set_api_key(key, save=False):
    """
    Set the api key to the given value.
    If save is True, the key will be saved in the config file and
    will be automatically used when importing rawpi in the future.
    """
    global HEADERS
    if save:
        with open('config', 'w') as f:
            json.dump({"key": key}, f)
    HEADERS["X-Riot-Token"] = key


def set_default_value(key, value):
    global DEFAULT_VALUES
    DEFAULT_VALUES[key] = value


# DECORATORS

def default_values(func):
    @wraps(func)
    def wrapper(cls, *args, **kwargs):
        for key in func.__kwdefaults__:
            if key not in kwargs and key in DEFAULT_VALUES:
                kwargs[key] = DEFAULT_VALUES[key]
        return func(cls, *args, **kwargs)
    return wrapper


def ratelimit(cls):
    return redis_wrap(cls)
    # if ratelimits_apply():
    #     return RedisRateLimitedEndpoint
    # return cls


# ENDPOINTS

@ratelimit
class Endpoint:
    ENDPOINT = ''

    @classmethod
    def rget(cls, region: str, url: str):
        """
        Do a requests get call on the provided region endpoint an method url.
        """
        return requests.get((REGION_ENDPOINT + cls.ENDPOINT + url).format(region), headers=HEADERS)


class ChampionMastery(Endpoint):
    ENDPOINT = "champion-mastery"

    @classmethod
    @default_values
    def by_summoner(cls, summoner_id, *, region=None):
        """
        Get all champion mastery entries sorted by number of champion points descending.
        """
        return cls.rget(region, "/v3/champion-masteries/by-summoner/{}".format(summoner_id))

    @classmethod
    @default_values
    def by_champion(cls, summoner_id, champion_id, *, region=None):
        """
        Get a champion mastery by player ID and champion ID.
        """
        return cls.rget(region, "/v3/champion-masteries/by-summoner/{}/by-champion/{}".format(summoner_id, champion_id))

    @classmethod
    @default_values
    def score(cls, summoner_id, *, region=None):
        """
        Get a player's total champion mastery score, which is the sum of individual champion mastery levels.
        """
        return cls.rget(region, "/v3/scores/by-summoner/{}".format(summoner_id))


class Champion(Endpoint):
    ENDPOINT = "platform"
    
    @classmethod
    @default_values
    def champions(cls, *, freetoplay=False, region=None):
        """
        Retrieve all champions.
        """
        freetoplay = "true" if freetoplay else "false"
        return cls.rget(region, "/v3/champions?freetoplay=".format(freetoplay))

    @classmethod
    @default_values
    def by_id(cls, champion_id, *, region=None):
        """
        Retrieve champion by ID.
        """
        return cls.rget(region, "/v3/champions/{}".format(champion_id))


class League(Endpoint):
    ENDPOINT = 'league'

    @classmethod
    @default_values
    def challenger(cls, queue, *, region=None):
        """
        Get the challenger league for a given queue.
        """
        return cls.rget(region, "/v3/challengerleagues/by-queue/{}".format(queue))

    @classmethod
    @default_values
    def master(cls, queue, *, region=None):
        """
        Get the master league for a given queue.
        """
        return cls.rget(region, "/v3/masterleagues/by-queue/{}".format(queue))

    @classmethod
    @default_values
    def leagues(cls, summoner_id, *, region=None):
        """
        Get leagues in all queues for a given summoner ID.
        """
        return cls.rget(region, "/v3/leagues/by-summoner/{}".format(summoner_id))

    @classmethod
    @default_values
    def positions(cls, summoner_id, *, region=None):
        """
        Get leagues in all queues for a given summoner ID.
        """
        return cls.rget(region, "/v3/positions/by-summoner/{}".format(summoner_id))


class LolStaticData(Endpoint):
    ENDPOINT = "static-data"

    @classmethod
    @default_values
    def champions(cls, *,locale="", version=None, tags=None, data_by_id=False, region=None):
        """
        Retrieves champion list.
        """
        query = QueryBuilder()
        query.add_string(locale)
        query.add_string(version)
        query.add_set(tags)
        query.add_bool(data_by_id)
        return cls.rget(region, "/v3/champions{}".format(query.build()))

    @classmethod
    @default_values
    def champion(cls, champion_id, *,locale="", version=None, tags=None, region=None):
        """
        Retrieves champion ID.
        """
        query = QueryBuilder()
        query.add_string(locale)
        query.add_string(version)
        query.add_set(tags)
        return cls.rget(region, "/v3/champions/{}{}".format(champion_id, query.build()))

    @classmethod
    @default_values
    def items(cls, *,locale="", version=None, tags=None, region=None):
        """
        Retrieves item list.
        """
        query = QueryBuilder()
        query.add_string(locale)
        query.add_string(version)
        query.add_set(tags)
        return cls.rget(region, "/v3/items?{}".format(query.build()))

    @classmethod
    @default_values
    def item(cls, item_id, *,locale="", version=None, tags=None, region=None):
        """
        Retrieves item ID.
        """
        query = QueryBuilder()
        query.add_string(locale)
        query.add_string(version)
        query.add_set(tags)
        return cls.rget(region, "/v3/items/{}?{}".format(item_id, query.build()))

    @classmethod
    @default_values
    def language_strings(cls, *,locale="", version=None, region=None):
        """
        Retrieve language strings data.
        """
        query = QueryBuilder()
        query.add_string(locale)
        query.add_string(version)
        return cls.rget(region, "/v3/language-strings?{}".format(query.build()))

    @classmethod
    @default_values
    def languages(cls, *, region=None):
        """
        Retrieves supported languages data.
        """
        return cls.rget(region, "/v3/languages")

    @classmethod
    @default_values
    def maps(cls, *,locale="", version=None, region=None):
        """
        Retrieve map data.
        """
        query = QueryBuilder()
        query.add_string(locale)
        query.add_string(version)
        return cls.rget(region, "/v3/maps?{}".format(query.build()))

    @classmethod
    @default_values
    def masteries(cls, *,locale="", version=None, tags=None, region=None):
        """
        Retrieves mastery list.
        """
        query = QueryBuilder()
        query.add_string(locale)
        query.add_string(version)
        query.add_set(tags)
        return cls.rget(region, "/v3/masteries?{}".format(query.build()))

    @classmethod
    @default_values
    def mastery(cls, mastery_id, *,locale="", version=None, tags=None, region=None):
        """
        Retrieves mastery item by ID.
        """
        query = QueryBuilder()
        query.add_string(locale)
        query.add_string(version)
        query.add_set(tags)
        return cls.rget(region, "/v3/masteries/{}?{}".format(mastery_id, query.build()))

    @classmethod
    @default_values
    def profile_icons(cls, *,locale="", version=None, region=None):
        """
        Retrieve profile icons.
        """
        query = QueryBuilder()
        query.add_string(locale)
        query.add_string(version)
        return cls.rget(region, "/v3/profile_icons?{}".format(query.build()))

    @classmethod
    @default_values
    def realms(cls, *, region=None):
        """
        Retrieve realm data.
        """
        return cls.rget(region, "/v3/realms")

    @classmethod
    @default_values
    def runes(cls, *,locale="", version=None, tags=None, region=None):
        """
        Retrieves rune list.
        """
        query = QueryBuilder()
        query.add_string(locale)
        query.add_string(version)
        query.add_set(tags)
        return cls.rget(region, "/v3/runes?{}".format(query.build()))

    @classmethod
    @default_values
    def rune(cls, rune_id, *,locale="", version=None, tags=None, region=None):
        """
        Retrieves rune by ID.
        """
        query = QueryBuilder()
        query.add_string(locale)
        query.add_string(version)
        query.add_set(tags)
        return cls.rget(region, "/v3/runes/{}?{}".format(rune_id, query.build()))

    @classmethod
    @default_values
    def summoner_spells(cls, *,locale="", version=None, tags=None, data_by_id=False, region=None):
        """
        Retrieves summoner spell list.
        """
        query = QueryBuilder()
        query.add_string(locale)
        query.add_string(version)
        query.add_set(tags)
        query.add_bool(data_by_id)
        return cls.rget(region, "/v3/summoner-spells?{}".format(query.build()))

    @classmethod
    @default_values
    def summoner_spell(cls, summoner_spell_id, *,locale="", version=None, tags=None, region=None):
        """
        Retrieves summoner spell by ID.
        """
        query = QueryBuilder()
        query.add_string(locale)
        query.add_string(version)
        query.add_set(tags)
        return cls.rget(region, "/v3/summoner-spells/{}?{}".format(summoner_spell_id, query.build()))

    @classmethod
    @default_values
    def versions(cls, *, region=None):
        """
        Retrieve version data.
        """
        return cls.rget(region, "/v3/versions")


class LolStatus(Endpoint):
    ENDPOINT = "status"

    @classmethod
    @default_values
    def shard_data(cls, *, region=None):
        """
        Get League of Legends status for the given shard.
        """
        return cls.rget(region, "/v3/shard-data")


class Masteries(Endpoint):
    ENDPOINT = "platform"

    @classmethod
    @default_values
    def by_summoner(cls, summoner_id, *, region=None):
        """
        Get mastery pages for a given summoner ID.
        """
        return cls.rget(region, "/v3/masteries/by-summoner/{}".format(summoner_id))


class Match(Endpoint):
    ENDPOINT = "match"

    @classmethod
    @default_values
    def by_match(cls, match_id, *, region=None):
        """
        Get match by match ID.
        """
        return cls.rget(region, "/v3/matches/{}".format(match_id))

    @classmethod
    @default_values
    def by_account(cls, account_id, *, queue=None, endTime=None, beginIndex=None, beginTime=None, season=None, champion=None, endIndex=None, region=None):
        """
        Get match by account ID.
        """
        query = QueryBuilder()
        query.add_set(queue)
        query.add_int(endTime)
        query.add_int(beginIndex)
        query.add_int(beginTime)
        query.add_set(season)
        query.add_set(champion)
        query.add_int(endIndex)
        return cls.rget(region, "/v3/matchlists/by-account/{}{}".format(account_id, query.build()))

    @classmethod
    @default_values
    def recent(cls, account_id, *, region=None):
        """
        Get matchlist for last 20 matches played on given account ID and platform ID.
        """
        return cls.rget(region, "/v3/matchlists/by-account/{}/recent".format(account_id))

    @classmethod
    @default_values
    def timeline(cls, match_id, *, region=None):
        """
        Get match timeline by match ID.
        """
        return cls.rget(region, "/v3/timelines/by-match/{}".format(match_id))


class Runes(Endpoint):
    ENDPOINT = "platform"

    @classmethod
    @default_values
    def by_summoner(cls, summoner_id, *, region=None):
        """
        Get rune pages for a given summoner ID.
        """
        return cls.rget(region, "/v3/runes/by-summoner/{}".format(summoner_id))


class Spectator(Endpoint):
    ENDPOINT = "spectator"

    @classmethod
    @default_values
    def by_summoner(cls, summoner_id, *, region=None):
        """
        Get current game information for the given summoner ID.
        """
        return cls.rget(region, "/v3/active-games/by-summoner/{}".format(summoner_id))

    @classmethod
    @default_values
    def featured(cls, *, region=None):
        """
        Get list of featured games.
        """
        return cls.rget(region, "/v3/featured-games")


class Summoner(Endpoint):
    ENDPOINT = "summoner"

    @classmethod
    @default_values
    def by_account(cls, account_id, *, region=None):
        """
        Get a summoner by account ID.
        """
        return cls.rget(region, "/v3/summoners/by-account/{}".format(account_id))

    @classmethod
    @default_values
    def by_name(cls, summoner_name, *, region=None):
        """
        Get a summoner by summoner name.
        """
        return cls.rget(region, "/v3/summoners/by-name/{}".format(summoner_name))

    @classmethod
    @default_values
    def by_summoner(cls, summoner_id, *, region=None):
        """
        Get a summoner by summoner ID.
        """
        return cls.rget(region, "/v3/summoners/by-summoner/{}".format(summoner_id))
