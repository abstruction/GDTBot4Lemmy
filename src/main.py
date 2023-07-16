#gameData['status']['abstractGameState'] goes Preview -> Live -> Final
#if 'Delayed' in gameData['status']['detailedState']


import time
from datetime import datetime, timedelta
import urllib.request, urllib.error, urllib.parse
import simplejson as json
import jplaw
import os

import markdownGenerator


class Game:
    def __init__( self, gameData, mediaData, liveFeedURL ):
        self.gameData = gameData
        self.mediaData = mediaData
        self.liveFeedURL = liveFeedURL
        
        timeData = gameData["gameData"]["datetime"]
        if "timeDate" in timeData:
            timeString = timeData["timeDate"] + " " + timeData["ampm"]
            self.startTime = datetime.strptime(timeString, "%Y/%m/%d %I:%M %p")
        else:
            timeString = " ".join((timeData["originalDate"], timeData["time"], timeData["ampm"]))
            self.startTime = datetime.strptime(timeString, "%Y-%m-%d %I:%M %p")

    def isFinished( self ):
        return "Final" in self.gameData['gameData']['status']['abstractGameState']

    def updateGameData( self, gameData ):
        self.gameData = gameData
        

class BotState:
    initial = 'initial'
    waitingForPregame = 'waitingForPregame'
    waitingForGametime = 'waitingForGametime'
    duringGame = 'duringGame'
    waitingForTomorrow = 'waitingForTomorrow'


class GDTBot:

    def __init__( self ):
        
        self.state = BotState.initial
        now = datetime.now()
        self.gameTime = now
        self.pregameTime = datetime(now.year, now.month, now.day, 9)
        self.todaysGames = []
        self.currentGame = None

        self.readSettings()
        
        self.mg = markdownGenerator.MarkdownGenerator( division_code=self.DIVISION_CODE )        
        
        try:
            self.lem = jplaw.Lemmy(self.LEMMY_INSTANCE, self.CLIENT_ID, self.CLIENT_SECRET)
        except Exception as e:
            print(e)
            print(f"Failed to log in to {self.LEMMY_INSTANCE}")
            return
        try:
            self.community_id = self.lem.Community.get(self.SUBREDDIT)['community']['id']
        except Exception as e:
            print(e)
            print(f'Failed to obtain community id for {self.SUBREDDIT}')
            return
        self.currentlyFeaturedThreadHandle = self.getHandleOnFeaturedThread()

        self.getTodaysGames()
        
        # We have to account for any period during which the bot is started
        if self.todaysGames:

            now = datetime.now()
            startTime = self.currentGame.startTime

            if now.hour >= self.PRE_THREAD_TIME and now < startTime:
                self.postPregameThread()
                self.changeState(BotState.waitingForGametime)
            elif startTime < now and not self.currentGame.isFinished():
                self.postGameThread()
                self.changeState(BotState.duringGame)
            elif now.hour < self.PRE_THREAD_TIME:
                self.changeState(BotState.waitingForPregame)
            elif self.currentGame.isFinished():
                self.postPostgameThread()
                self.changeState(BotState.waitingForTomorrow)
            else:
                print('Failed to figure out first state, defaulting to waitingForPregame')
                self.changeState(BotState.waitingForPregame)

        else:
            self.postOffDayThread()
            self.changeState(BotState.waitingForTomorrow)

    def readSettings( self ):
        with open(os.getcwd() + '/settings.json') as data:
            settings = json.load(data)
            self.LEMMY_INSTANCE = settings.get('LEMMY_INSTANCE')
            self.CLIENT_ID = settings.get('CLIENT_ID')
            self.CLIENT_SECRET = settings.get('CLIENT_SECRET')
            self.SUBREDDIT = settings.get('SUBREDDIT')
            self.TEAM_CODE = settings.get('TEAM_CODE')
            self.DIVISION_CODE = settings.get('DIVISION_CODE')
            self.PRE_THREAD_TIME = settings.get('PRE_THREAD_SETTINGS').get('PRE_THREAD_TIME')
            self.PREGAME_THREAD_UPDATE_PERIOD_SECONDS = settings.get('PRE_THREAD_SETTINGS').get('PRE_THREAD_UPDATE_PERIOD_SECONDS')
            self.GAME_THREAD_UPDATE_PERIOD_SECONDS = settings.get("THREAD_SETTINGS").get("GAME_THREAD_UPDATE_PERIOD_SECONDS")

    def getTodaysGames( self ):

        today = datetime.today()
        self.todaysGames = []
        self.currentGame = None

        baseURL = "https://statsapi.mlb.com"
        # Year schedule URL
        url = baseURL + "/api/v1/schedule?language=en&sportId=1&date="
        url += today.strftime("%m/%d/%Y")

        response = ""
        while not response:
            try:
                response = urllib.request.urlopen(url)
                schedule = json.load(response)                
            except:
                print("Failed to access stats API or bad json from API, trying again in 20 seconds...")
                time.sleep(20)

        if schedule['totalGames'] == 0:
            self.todaysGames = []
            self.currentGame = None
            return
        
        todaysGames = schedule["dates"][0]["games"]
        teamsGames = []
        for game in todaysGames:
            if game["teams"]["away"]["team"]["id"] == self.TEAM_CODE\
            or game["teams"]["home"]["team"]["id"] == self.TEAM_CODE:
                teamsGames.append( (baseURL + game['link'], f'{baseURL}/api/v1/game/{game["gamePk"]}/content') )

        if teamsGames:
            for gameURL, mediaURL in teamsGames:
                print(f"{gameURL}")
                response = urllib.request.urlopen(gameURL)
                gameData = json.load(response)
                response = urllib.request.urlopen(mediaURL)
                mediaData = json.load(response)
                self.todaysGames.append( Game(gameData, mediaData, gameURL) )
                if len(teamsGames) > 1: time.sleep(5)
            self.todaysGames.sort(key = lambda g: g.startTime)
            self.currentGame = self.todaysGames[0]


#event: ---4am-------self.PRE_THREAD_TIMEam--------game time----------game ends---
#state:     w4pregame                      w4gametime       duringGame       w4tomorrow

    def mainLoop( self ):

        while True:
    
            if self.state == BotState.waitingForPregame:
                time.sleep(60)
                if datetime.now() > self.pregameTime:
                    self.getTodaysGames()
                    if self.todaysGames:
                        self.postPregameThread()
                        self.changeState(BotState.waitingForGametime)
                    else:
                        self.postOffDayThread()
                        self.changeState(BotState.waitingForTomorrow)

            elif self.state == BotState.waitingForGametime:
                time.sleep( self.PREGAME_THREAD_UPDATE_PERIOD_SECONDS )
                if datetime.now() > self.currentGame.startTime - timedelta(minutes=60):
                    self.postGameThread()
                    self.changeState(BotState.duringGame)
                else:
                    self.updateGameData()
                    self.updatePregameThread()

            elif self.state == BotState.duringGame:
                time.sleep( self.GAME_THREAD_UPDATE_PERIOD_SECONDS )
                self.updateGameData()
                if self.currentGame.isFinished():
                    if len(self.todaysGames) == 1:
                        self.postPostgameThread()
                        self.changeState(BotState.waitingForTomorrow)
                    else:
                        #sort out doubleheadders THIS IS UNTESTED AS OF v.5.0
                        self.currentGame = self.todaysGames[1]
                        self.todaysGames = [self.currentGame]
                        self.postGameThread()
                        self.changeState(BotState.duringGame)
                else:
                    self.updateGameThread()

            elif self.state == BotState.waitingForTomorrow:
            
                if datetime.now() < self.tomorrow:
                    time.sleep(600)
                else:
                    print('NEW DAY')
                    self.getTodaysGames()
                    if self.todaysGames:
                        now = datetime.now()
                        self.pregameTime = datetime(now.year, now.month, now.day, self.PRE_THREAD_TIME)
                        self.changeState(BotState.waitingForPregame)
                    else:
                        self.postOffDayThread()
                        self.changeState(BotState.waitingForTomorrow)
            else:
                break


    def changeState( self, newState ):

        print(f'> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Changing state from {self.state} to {newState}')

        if newState == BotState.waitingForPregame:
            print(f"Waiting to post pregame thread at {self.PRE_THREAD_TIME}...")
            self.state = newState
    
        elif newState == BotState.waitingForGametime:
            print(f'Waiting for gametime at {self.currentGame.startTime}...')
            print(f'Updating pregame thread every {self.PREGAME_THREAD_UPDATE_PERIOD_SECONDS} seconds...')
            self.state = newState

        elif newState == BotState.duringGame:
            print(f'Updating thread every {self.GAME_THREAD_UPDATE_PERIOD_SECONDS} seconds...')
            self.state = newState

        elif newState == BotState.waitingForTomorrow:
            print('Waiting for tomorrow...')
            now = datetime.now()
            tomorrow = now + timedelta(hours=24)
            if now.hour < 4:
                self.tomorrow = datetime(now.year, now.month, now.day, 4)
            else:
                self.tomorrow = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 4)
            self.state = newState


    def updateGameData( self ):
        response = urllib.request.urlopen(self.currentGame.liveFeedURL)
        self.currentGame.updateGameData( json.load(response) )

    def postThread( self, title, body, featured=True ):
        try:
            posts = self.lem.Post.list(community_id=self.community_id)
        except:
            posts = []
        for post in posts:
            if post['post']['name'] == title:
                print(f"Thread '{title}' already posted")
                return post

        postSuccess = False
        while not postSuccess:
            try:
                sub = self.lem.Post.create(community_id=self.community_id, title=title, body=body)
                self.lem.Post.feature(post_id=sub['post']['id'], featured=featured, feature_type=jplaw.types.PostFeatureType.Community )
                print(f"Posted thread\n{title}")
                postSuccess = True
            except Exception as e:
                print(e)
                print(f"Failed to post or feature thread {title}\nTrying again in 20 seconds...\n")
                time.sleep(20)

        return sub


    def updateThread( self, handle, body ):
        if not handle:
            handle = self.getHandleOnFeaturedThread()
        if handle:
            try:
                self.lem.Post.edit(post_id = handle['post']['id'], body=body)
            except:
                print("Failed to update thread, try again on next iteration")
        else:
            print("Could not update thread, no featured post on Lemmy")
        
    def unfeatureThread( self, handle ):
        # check, just in case the bot is restarted and it doesn't have the handle
        if handle:
            try:
                self.lem.Post.feature(post_id=handle['post']['id'], featured=False, feature_type=jplaw.types.PostFeatureType.Community )
            except:
                print(f'Failed to unfeature thread {handle["post"]["name"]}')

    def getHandleOnFeaturedThread( self ):
        try:
            posts = self.lem.Post.list(community_id=self.community_id)
        except:
            return None
            
        for post in posts:
            if post['post']['featured_community'] and 'THREAD]' in post['post']['name']:
                return post
        return None

        
    def postPregameThread( self ):
        title = self.mg.generateTitle( self.currentGame, 'pre')
        ft = self.getHandleOnFeaturedThread()
        if ft and ft['post']['name'] == title:
            print('Pregame thread already posted')
            self.currentlyFeaturedThreadHandle = ft
            return
        body = self.mg.generatePreMarkdown( self.todaysGames )
        self.unfeatureThread( self.currentlyFeaturedThreadHandle )
        self.currentlyFeaturedThreadHandle = self.postThread( title, body )

    def updatePregameThread( self ):
        timeString = datetime.now().strftime("^%Y-%m-%d^ ^%H:%M:%S^")
        body = self.mg.generatePreMarkdown( self.todaysGames )
        body += f"\n\n^Last^ ^updated^ {timeString}"
        self.updateThread( self.currentlyFeaturedThreadHandle, body )

    def postGameThread( self ):
        title = self.mg.generateTitle( self.currentGame, 'game' )
        ft = self.getHandleOnFeaturedThread()
        if ft and ft['post']['name'] == title:
            print('Game thread already posted')
            self.currentlyFeaturedThreadHandle = ft
            return
        body = self.mg.generateBodyMarkdown( self.currentGame, 'game' )
        self.unfeatureThread( self.currentlyFeaturedThreadHandle )
        self.currentlyFeaturedThreadHandle = self.postThread( title, body )
        
    def updateGameThread( self ):
        timeString = datetime.now().strftime("^%Y-%m-%d^ ^%H:%M:%S^")
        body = self.mg.generateBodyMarkdown( self.currentGame, 'game' )
        body += f"\n\n^Last^ ^updated^ {timeString}"
        self.updateThread( self.currentlyFeaturedThreadHandle, body )

    def postPostgameThread( self ):
        title = self.mg.generateTitle( self.currentGame, 'post' )
        body = self.mg.generateBodyMarkdown( self.currentGame, 'post' )
        self.unfeatureThread( self.currentlyFeaturedThreadHandle )
        self.currentlyFeaturedThreadHandle = self.postThread( title, body )

    def postOffDayThread( self ):
        body = self.mg.generateOffDayMarkdown()
        dateString = datetime.now().strftime("%m/%d/%Y")
        title = f"[OFF DAY THREAD] {dateString}"
        self.unfeatureThread( self.currentlyFeaturedThreadHandle )        
        self.currentlyFeaturedThreadHandle = self.postThread( title, body )


if __name__ == '__main__':
    bot = GDTBot()
    bot.mainLoop()