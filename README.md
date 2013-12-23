lolapi
======

League of Legends Python 3.x API

This is an API written in python to communicate with the official Riot League of Legends API (http://developer.riotgames.com).
This is mainly used as a local api for my own projects but can and is encouraged to be used by others.

This product is not endorsed, certified or otherwise approved in any way by Riot Games, Inc. or any of its affiliates.

usage
-----

instantiate the api as follows, key is required, region defaults to euw

api = lolapi.LolAPI(key = "YOUR KEY", region="euw")

To get an overview of the methods you should do a quick dir(api) for now.
All methods take an optional region argument that if not specified will use the default set when you called LolAPI

example:

summoner = api.get_summoner_by_name("Kruptein")