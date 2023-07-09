Baseball GDT Bot
=====================================

### Current Version: 5.0.0

The point of this project is to create a bot that will generate a
	game discussion thread that contains live linescore and boxscore,
	post it in the correct Lemmy forum for that team, and keep it
	updated throughout the game.

Version 5 is a fork from 4 altered to work on Lemmy rather than Reddit,
and with a completely rewritten main.py. Version 5 is also in Python 3.


---


### Configuration

To use the default settings, copy `sample_settings.json` into `src/settings.json`.
As of 5.0 most of these settings ARE NOT used.

#### Descriptions of Settings

* `BOT_TIME_ZONE` - time zone of the computer running the bot, uncomment the line that you want to use

* `TIME_ZONE` - time zone of the team. uncomment the line that you want to use

* `POST_TIME` - bot posts the thread POST_TIME hours before the game

* `SUBREDDIT` - subreddit that you want the threads posted to

* `TEAM_CODE` - three letter code that represents team, look this up

* `OFFDAY_THREAD` - do you want an offday discussion thread?

* `PREGAME_THREAD` - do you want a pre game thread?

* `POST_GAME_THREAD` - do you want a post game thread?

* `SUGGESTED_SORT` - what do you want the suggested sort to be? ("confidence", "top", "new", "controversial", "old", "random", "qa", "")

* `STICKY` - do you want the thread stickied? (mod only)

* `MESSAGE` - send submission shortlink to /u/baseballbot

* `INBOXREPLIES` - do you want to receive thread replies in the bot's inbox?

* `OFFDAY_THREAD_SETTINGS` - what to include in the offday threads

* `PRE_THREAD_SETTINGS` - what to include in the pregame threads

* `THREAD_SETTINGS` - what to include in game threads, example footer: "**Remember to sort by new to keep up!**"

* `POST_THREAD_SETTINGS` - what to include in postgame threads, example footer: "**Remember to sort by new to keep up!**"

---

If something doesn't seem right, feel free to message me or post it as a bug here.

This was written in Python 2.7, so beware if you are running Python 3 or
	above that it may not work correctly. Also make sure you install
	praw and simplejson before running!

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
