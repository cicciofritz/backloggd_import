# backloggd_import
Unofficial backloggd script to import games from a .csv file into your Backloggd account

This is only the beginning, something working here! Sorry

Script to import as a backlog in backloggd site games listed in a csv (i.e. from steam or epic library)

How works:
you have to fill an auth.py file with the requested token for twitch and backloggd; alternatively you can directly fill the variable inside the script

First each game is searched in IGDB database by name using their API.

Authentication through Twitch is required: please follow the "Account Creation" section here https://api-docs.igdb.com/#getting-started

Actual search finds multiple results. Documentation can be found here https://igdb-openapi.s-crypt.co/#/

The script prompt the user to choose between multiple options.

Once a list of gameID file is ready, a POST request to a backloggd authenticated section can be performed.

Stay tuned.

NB. I'm not a professional python/web developer, I'm something between a pywhat? and a beginner with python/web. I use this small project to learn and more likely to make mistakes, any suggestions are welcome

