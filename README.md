GDTBot4Lemmy
=====================================

### Current Version: 5.0.0

This is a fork of https://github.com/mattabullock/Baseball-GDT-Bot

This is a bot for Lemmy that creates Major League Baseball game day threads,
game threads, postgame threads, and an off-day threads.
Pregame and Game threads are updated periodically, and all stats are pulled
from MLB's (free, generous) API.

Version 5 is a fork from 4, altered to work on Lemmy rather than Reddit,
and with a completely rewritten main.py. Version 5 is also in Python 3.


---


### Configuration

To use the default settings, copy `sample_settings.json` into `src/settings.json`.
As of 5.0 most of these settings ARE NOT used.

#### Descriptions of Settings

* `LEMMY_INSTANCE` - which Lemmy site you're posting to

* `CLIENT_ID` - username

* `CLIENT_SECRET` - password

* `SUBREDDIT` - lemmy subforum that you want the threads posted to

* `TEAM_CODE` - three letter code that represents team, look this ./src/team IDs.txt

* `PRE_THREAD_SETTINGS` - what to include in the pregame threads

* `PRE_THREAD_TIME` - hour (in 24 hour format) at which pregame thread is posted

* `PRE_THREAD_UPDATE_PERIOD_SECONDS` - number of seconds between pregame thread updates

* `GAME_THREAD_UPDATE_PERIOD_SECONDS` - number of seconds between game thread updates

---

If something doesn't seem right, feel free to message me or post it as a bug here.

Modules being used:

	Lemmy - interfacing Lemmy, modified to allow post editing and stickying
	simplejson - JSON parsing
	urllib - pulling data from MLB servers


### Updates

#### v4.0.0
* Updated to new MLB stats API.

#### v3.1.0
* Updated to praw version v5.0.1

#### v3.0.2
* GUI added.

#### v3.0.1
* Now uses OAuth!

#### v3.0.0
* Modular - If you want a certain feature, just change a variable at the top!
* Easier to read - Cleaned up some code, started using more OOP.

#### v2.0.4
* Fixed crash caused by game not being aired on TV.
* Fixed another crash related to scoring plays.

#### v2.0.3
* Fixed the Diamondbacks' subreddit not working properly.
* Fixed crash related to scoring plays.

#### v2.0.2

* Fixed random crashing.
* Fixed bug where some teams names were not displayed correctly. (Though Chi White Sox White Sox is a great name...)

#### v2.0.1

* Fixed gamecheck not always working correctly.
* Fixed the TV media showing the same for both home and away.
* Fixed the timestamp on the game/time checks not displaying correctly.
