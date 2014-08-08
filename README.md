lolapi
======

League of Legends Python 3.x API

This is an API written in python to communicate with the official Riot League of Legends API (http://developer.riotgames.com).

This product is not endorsed, certified or otherwise approved in any way by Riot Games, Inc. or any of its affiliates.

usage
-----

For now only the rawpi module is available, it contains the raw results of a connection to the api.
No exception checks or anything.
It uses requests, a popular networking lib, and returns the requests objects.

You'll need to set your key in the config file or use the rawpi.set_api_key(key) method.
