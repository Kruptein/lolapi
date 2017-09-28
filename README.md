lolapi
======

League of Legends Python 3.x API

This is an API written in python to communicate with the official Riot League of Legends API (http://developer.riotgames.com).

This product is not endorsed, certified or otherwise approved in any way by Riot Games, Inc. or any of its affiliates.


THIS CODE IS IN ACTIVE DEVELOPMENT, USE IT AT YOUR OWN RISK.

usage
-----

The lolapi.rawpi module provides a raw interface to all of the league of legends api methods,
it returns the raw requests response to all available endpoints.

Rate limiting is builtin and uses redis (this is at the moment of writing always on and the onyl option).

The lolapi.constants module provides some (this is not complete yet) of the constants provided by the league api.


dependencies
-------------

* requests for the network connection
* redis for rate limiting
