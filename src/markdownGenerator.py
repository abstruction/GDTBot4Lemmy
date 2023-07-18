#Generates markdown for threads
#import player

#import xml.etree.ElementTree as ET
#import urllib.request, urllib.error, urllib.parse
#import simplejson as json
from datetime import datetime, timedelta
#import time
import player
import generateDivisionStandings
import generateLineups

class MarkdownGenerator:

    options = {
            "Twins": { "sub": "/c/minnesotatwins", "tag": "[MIN](/c/minnesotatwins)", "notes": "min" },
            "White Sox": { "sub": "/c/WhiteSox", "tag": "[CWS](/c/WhiteSox)", "notes": "cws" },
            "Tigers": { "sub": "/c/MotorCityKitties", "tag": "[DET](/c/MotorCityKitties)", "notes": "det" },
            "Royals": { "sub": "/c/KCRoyals", "tag": "[KCR](/c/KCRoyals)", "notes": "kc" },
            "Indians": { "sub": "/c/WahoosTipi", "tag": "[CLE](/c/WahoosTipi)", "notes": "cle" },
            "Rangers": { "sub": "/c/TexasRangers", "tag": "[TEX](/c/TexasRangers)", "notes": "tex" },
            "Astros": { "sub": "/c/Astros", "tag": "[HOU](/c/Astros)", "notes": "hou" },
            "Athletics": { "sub": "/c/OaklandAthletics", "tag": "[OAK](/c/OaklandAthletics)", "notes": "oak" },
            "Angels": { "sub": "/c/AngelsBaseball", "tag": "[LAA](/c/AngelsBaseball)", "notes": "ana" },
            "Mariners": { "sub": "/c/Mariners", "tag": "[SEA](/c/Mariners)", "notes": "sea" },
            "Red Sox": { "sub": "/c/RedSox", "tag": "[BOS](/c/RedSox)", "notes": "bos" },
            "Yankees": { "sub": "/c/NYYankees", "tag": "[NYY](/c/NYYankees)", "notes": "nyy" },
            "Blue Jays": { "sub": "/c/TorontoBlueJays", "tag": "[TOR](/c/TorontoBlueJays)", "notes": "tor" },
            "Rays": { "sub": "/c/TampaBayRays", "tag": "[TBR](/c/TampaBayRays)", "notes": "tb" },
            "Orioles": { "sub": "/c/Orioles", "tag": "[BAL](/c/Orioles)", "notes": "bal" },
            "Cardinals": { "sub": "/c/Cardinals", "tag": "[STL](/c/Cardinals)", "notes": "stl" },
            "Reds": { "sub": "/c/Reds", "tag": "[CIN](/c/Reds)", "notes": "cin" },
            "Pirates": { "sub": "/c/Buccos", "tag": "[PIT](/c/Buccos)", "notes": "pit" },
            "Cubs": { "sub": "/c/CHICubs", "tag": "[CHC](/c/CHICubs)", "notes": "chc" },
            "Brewers": { "sub": "/c/Brewers", "tag": "[MIL](/c/Brewers)", "notes": "mil" },
            "Giants": { "sub": "/c/SFGiants", "tag": "[SFG](/c/SFGiants)", "notes": "sf" },
            "Diamondbacks": { "sub": "/c/azdiamondbacks", "tag": "[ARI](/c/azdiamondbacks)", "notes": "ari" },
            "D-backs": { "sub": "/c/azdiamondbacks", "tag": "[ARI](/c/azdiamondbacks)", "notes": "ari" },
            "Rockies": { "sub": "/c/ColoradoRockies", "tag": "[COL](/c/ColoradoRockies)", "notes": "col" },
            "Dodgers": { "sub": "/c/Dodgers", "tag": "[LAD](/c/Dodgers)", "notes": "la" },
            "Padres": { "sub": "/c/Padres", "tag": "[SDP](/c/Padres)", "notes": "sd" },
            "Phillies": { "sub": "/c/Phillies", "tag": "[PHI](/c/Phillies)", "notes": "phi" },
            "Mets": { "sub": "/c/NewYorkMets", "tag": "[NYM](/c/NewYorkMets)", "notes": "nym" },
            "Marlins": { "sub": "/c/letsgofish", "tag": "[MIA](/c/letsgofish)", "notes": "mia" },
            "Nationals": { "sub": "/c/Nationals", "tag": "[WSH](/c/Nationals)", "notes": "was" },
            "Braves": { "sub": "/c/Braves", "tag": "[ATL](/c/Braves)", "notes": "atl"}
        }

##    def __init__(self, time_info, pre_thread_settings, thread_settings, post_thread_settings):
##        
##        (self.time_zone, self.time_change,) = time_info
##        (self.pre_thread_tag, self.pre_thread_time,
##            (self.pre_probables, self.pre_first_pitch)
##        ) = pre_thread_settings
##        (self.thread_tag,
##            (self.header, self.box_score,
##             self.line_score, self.scoring_plays,
##             self.highlights, self.footer)
##        ) = thread_settings
##        (self.post_thread_tag,
##            (self.post_header, self.post_box_score,
##             self.post_line_score, self.post_scoring_plays,
##             self.post_highlights, self.post_footer)
##        ) = post_thread_settings

    def __init__( self, division_code=201, time_zone='ET' ):
        self.pre_probables = True
        self.time_change = 0
        self.time_zone = time_zone
        self.division_code = division_code
        self.header = True
        self.box_score = True
        self.line_score = True
        self.scoring_plays = True
        self.post_header = True
        self.post_box_score = True
        self.post_line_score = True
        self.post_scoring_plays = True
        self.post_highlights = True
        self.post_footer = True

    
    def generateTitle(self, game, threadType):
##        if threadType == "pre": title = self.pre_thread_tag + " "
##        elif threadType == "game": title = self.thread_tag + " "
##        elif threadType == "post": title = self.post_thread_tag + " "
        if threadType == "pre": title = "[GAMEDAY THREAD] "
        elif threadType == "game": title = "[GAME THREAD] "
        elif threadType == "post": title = "[POSTGAME THREAD] "
        else: title = "[UH OH] "

        gameData = game.gameData['gameData']
        timeData = gameData["datetime"]
        if "timeDate" in timeData:
            timestring = timeData["timeDate"] + " " + timeData["ampm"]
            date_object = datetime.strptime(timestring, "%Y/%m/%d %I:%M %p")
        else:
            timestring = timeData["originalDate"] + " " + timeData["time"] + " " + timeData["ampm"]
            date_object = datetime.strptime(timestring, "%Y-%m-%d %I:%M %p")
        awayTeamName = gameData["teams"]["away"]["name"] if isinstance(gameData["teams"]["away"]["name"], str) else gameData["teams"]["away"]["name"]["full"]
        homeTeamName = gameData["teams"]["home"]["name"] if isinstance(gameData["teams"]["home"]["name"], str) else gameData["teams"]["home"]["name"]["full"]
        
        if threadType in ('pre', 'game'):
            title += awayTeamName + " (" + str(gameData["teams"]["away"]["record"]["wins"]) + "-" + str(gameData["teams"]["away"]["record"]["losses"]) + ")"
            title += " @ "
            title += homeTeamName + " (" + str(gameData["teams"]["home"]["record"]["wins"]) + "-" + str(gameData["teams"]["home"]["record"]["losses"]) + ")"
            
        elif threadType == 'post':
            homeTeamScore = game.gameData['liveData']['linescore']['teams']['home']['runs']
            awayTeamScore = game.gameData['liveData']['linescore']['teams']['away']['runs']
            if homeTeamScore > awayTeamScore:
                title += f"The {homeTeamName} Defeated the {awayTeamName} by a score of {homeTeamScore}-{awayTeamScore}"
            else:
                title += f"The {awayTeamName} Defeated the {homeTeamName} by a score of {awayTeamScore}-{homeTeamScore}"
        title += " - "
        title += date_object.strftime("%B %d, %Y")
        #print("Returning title " + title)
        return title

    def generatePreMarkdown( self, games ):
        markdown = generateDivisionStandings.generateDivisionStandings(self.division_code)
        #markdown ++ "\n\n"
        for g in games:
            markdown += self.generateHeader( g.gameData, g.mediaData )
            #markdown += self.generatePreFirstPitch( g.gameData )
            if self.pre_probables:
                markdown += self.generatePreProbables(g.gameData)
            markdown += generateLineups.generateLineups(g.gameData['gameData']['game']['pk'])
            #if self.pre_first_pitch: markdown += self.generate_pre_first_pitch(gameData)
            markdown += "\n\n"
        # print("Returning all markdown")
        return markdown

    def generatePreProbables(self, gameData):
        #print("generating pregame probables")
        probables = ""
        try:
            homeTeamName = gameData["gameData"]["teams"]["home"]["teamName"]
            awayTeamName = gameData["gameData"]["teams"]["away"]["teamName"]
            #homeSub = self.options[homeTeamName]["sub"]
            #awaySub = self.options[awayTeamName]["sub"]

            homePitcherID = str(gameData["gameData"]["probablePitchers"]["home"]["id"])
            awayPitcherID = str(gameData["gameData"]["probablePitchers"]["away"]["id"])
            #print(homePitcherID)
            #print(awayPitcherID)
            homePitcherName = gameData["gameData"]["probablePitchers"]["home"]["fullName"]
            awayPitcherName = gameData["gameData"]["probablePitchers"]["away"]["fullName"]
            homePitcherStats = gameData["liveData"]["boxscore"]["teams"]["home"]["players"]["ID" + homePitcherID]["seasonStats"]["pitching"]
            awayPitcherStats = gameData["liveData"]["boxscore"]["teams"]["away"]["players"]["ID" + awayPitcherID]["seasonStats"]["pitching"]

            homePitcher = "[" + homePitcherName + "](" + "http://mlb.mlb.com/team/player.jsp?player_id=" + homePitcherID + ")"
            homePitcher += " (" + str(homePitcherStats["wins"]) + "-" + str(homePitcherStats["losses"]) + ", " + str(homePitcherStats["era"]) + ")"
            awayPitcher = "[" + awayPitcherName + "](" + "http://mlb.mlb.com/team/player.jsp?player_id=" + awayPitcherID + ")"
            awayPitcher += " (" + str(awayPitcherStats["wins"]) + "-" + str(awayPitcherStats["losses"]) + ", " + str(awayPitcherStats["era"]) + ")"

            probables  = "| |Starting Pitcher|Report\n"
            probables += "|-|-|-|\n"
            # probables += "[" + awayTeamName + "](" + awaySub + ")|" + awayPitcher + "| No report posted" + "\n"
            probables += awayTeamName + "|" + awayPitcher + "| No report posted" + "\n"
            # probables += "[" + homeTeamName + "](" + homeSub + ")|" + homePitcher + "| No report posted" + "\n"
            probables += homeTeamName + "|" + homePitcher + "| No report posted" + "\n"

            probables += "\n\n"

            return probables
        
        except Exception as e:
            print("Exception generating probables, returning partial string")
            print(e)
            return probables

    def generatePreFirstPitch(self, game):
        first_pitch = ""
        try:
            # Get time data
            timeData = game['gameData']["datetime"]
            if "timeDate" in timeData:
                timestring = timeData["timeDate"] + " " + timeData["ampm"]
                date_object = datetime.strptime(timestring, "%Y/%m/%d %I:%M %p")
            else:
                timestring = timeData["originalDate"] + " " + timeData["time"] + " " + timeData["ampm"]
                date_object = datetime.strptime(timestring, "%Y-%m-%d %I:%M %p")
            t = timedelta(hours=self.time_change)
            timezone = self.time_zone
            date_object = date_object - t
            first_pitch = "**First Pitch:** " + date_object.strftime("%I:%M %p ") + timezone + "\n\n"

            return first_pitch
        
        except Exception as e:
            print(e)
            print("Missing data for first_pitch, returning empty string")
            return first_pitch

    def generateBodyMarkdown(self, game, threadType):
        
        #print("Entering editor.generateBodyMarkdown")
        markdown = ""
        gameData = game.gameData
        mediaData = game.mediaData

        if threadType == "game":
            #print("Generating markdown for game thread...")
            if self.header: markdown += self.generateHeader(gameData, mediaData)
            if self.box_score: markdown += self.generateBoxscore(gameData)
            if self.line_score: markdown += self.generateLinescore(gameData)
            if self.scoring_plays: markdown += self.generateScoringPlays(gameData)
            #if self.highlights: markdown += self.generateHighlights(mediaData)
            #if self.footer: markdown += self.footer + "\n\n"
            #print("Done generating game thread body")
            
        elif threadType == "post":
            #print("Generating markdown for post-game thread...")
            #if self.post_header: markdown += self.generateHeader(gameData, mediaData)
            if self.post_box_score: markdown += self.generateBoxscore(gameData)
            if self.post_line_score: markdown += self.generateLinescore(gameData)
            if self.post_scoring_plays: markdown += self.generateScoringPlays(gameData)
            #if self.post_highlights: markdown += self.generateHighlights(mediaData)
            #if self.post_footer: markdown += self.postFooter + "\n\n"
            
        #print("Past body generation")
        markdown += self.generateStatus(gameData)
        #print("Returning all markdown from generate_markdown")
        return markdown

    def generateHeader(self, data, mediaData):
        #print("Generating header...")
        header = ""
        # try:
        gameData = data["gameData"]
        #game = gameData["game"]
        timeData = gameData["datetime"]
        weather = gameData["weather"]
        # print(weather.keys())
        #teams = gameData["teams"]
        videoBroadcast = mediaData["media"]["epg"][0]
        audioBroadcast = mediaData["media"]["epg"][2]

        #print('floof')
        # Get time data
        if "timeDate" in timeData:
            timestring = timeData["timeDate"] + " " + timeData["ampm"]
            date_object = datetime.strptime(timestring, "%Y/%m/%d %I:%M %p")
        else:
            timestring = timeData["originalDate"] + " " + timeData["time"] + " " + timeData["ampm"]
            date_object = datetime.strptime(timestring, "%Y-%m-%d %I:%M %p")
        t = timedelta(hours=self.time_change)
        timezone = self.time_zone
        date_object = date_object - t

        #print('kool and the gang')
        # Build out header
        #header = "**First Pitch:** " + date_object.strftime("%I:%M %p ") + timezone + "\n\n"
        #header += "[Preview](http://mlb.mlb.com/mlb/gameday/index.jsp?gid=" + str(game["id"]) + ")\n\n"
        header += "|Game Info|Links|\n"
        header += "|:--|:--|\n"
        header += "|**First Pitch:** " + date_object.strftime("%I:%M %p ") + timezone + " @ " + gameData["venue"]["name"] + "|[Gameday](https://www.mlb.com/gameday/" + str(gameData["game"]["pk"]) + ")|\n"
        if weather:
            header += "|**Weather:** " + weather["condition"] + ", " + weather["temp"] + " F, " + "Wind " + weather["wind"] + f"|[Statcast Game Preview](https://baseballsavant.mlb.com/preview?game_pk={gameData['game']['pk']})\n"
        else:
            header += "|**Weather:** " + f"|[Statcast Game Preview](https://baseballsavant.mlb.com/preview?game_pk={gameData['game']['pk']})\n"

        header += "|**TV:** "
        video = False
        for item in videoBroadcast["items"]:
            if item["callLetters"]:
                header += item["callLetters"] + ", "
                video = True
        if video:
            header = header[:-2]

        header += "  **Radio:** "
        audio = False
        for item in audioBroadcast["items"]:
            if item["callLetters"]:
                header += item["callLetters"] + ", "
                audio = True
        if audio:
            header = header[:-2]
        header += "|\n\n"
        #print("Returning header")
        return header
        # except Exception e:
            # print "Missing data for header, returning empty string..."
            # return header

    def generateBoxscore(self, data):
        #print("Generating box scores")
        boxscore = ""
        # try:
        unorderedAwayBatters = {}
        unorderedHomeBatters = {}
        awayBatters = []
        homeBatters = []
        awayPitchers = []
        homePitchers = []

        awayTeam = data["liveData"]["boxscore"]["teams"]["away"]
        homeTeam = data["liveData"]["boxscore"]["teams"]["home"]
        awayTeamInfo = data["gameData"]["teams"]["away"]
        homeTeamInfo = data["gameData"]["teams"]["home"]

        # Get unordered batters
        for batterID in awayTeam["players"]:
            batter = awayTeam["players"][batterID]
            playersStatsForThisGame = batter["stats"]["batting"]
            seasonStats = batter["seasonStats"]["batting"]
            if "battingOrder" in batter.keys() and batter["battingOrder"] is not None:
                bo = batter['battingOrder']
                batterName = batter["person"]["fullName"].strip()
                unorderedAwayBatters[bo] = \
                    player.Batter(batterName, batter["position"]["abbreviation"], playersStatsForThisGame["atBats"],
                    playersStatsForThisGame["runs"], playersStatsForThisGame["hits"], playersStatsForThisGame["rbi"],
                    playersStatsForThisGame["baseOnBalls"],
                    playersStatsForThisGame["strikeOuts"], seasonStats["avg"],
                    seasonStats["obp"], seasonStats["ops"], batter["person"]["id"])

        for batterID in homeTeam["players"]:
            batter = homeTeam["players"][batterID]
            playersStatsForThisGame = batter["stats"]["batting"]
            seasonStats = batter["seasonStats"]["batting"]
            if "battingOrder" in batter.keys() and batter["battingOrder"] is not None:
                batterName = batter["person"]["fullName"].strip()
                unorderedHomeBatters[batter["battingOrder"]] = \
                    player.Batter(batterName, batter["position"]["abbreviation"], playersStatsForThisGame["atBats"],
                    playersStatsForThisGame["runs"], playersStatsForThisGame["hits"], playersStatsForThisGame["rbi"],
                    playersStatsForThisGame["baseOnBalls"],
                    playersStatsForThisGame["strikeOuts"], seasonStats["avg"],
                    seasonStats["obp"], seasonStats["ops"], batter["person"]["id"])

        # Order batters in correct order
        for battingOrder in sorted(unorderedAwayBatters):
            awayBatters.append(unorderedAwayBatters[battingOrder])
        for battingOrder in sorted(unorderedHomeBatters):
            homeBatters.append(unorderedHomeBatters[battingOrder])

        # Get ordered pitchers
        for pitcherID in awayTeam["pitchers"]:
            pitcher = awayTeam["players"]["ID" + str(pitcherID)]
            gameStats = pitcher['stats']['pitching']
            seasonStats = pitcher["seasonStats"]["pitching"]
            pitcherName = pitcher["person"]["fullName"].strip()
            if not 'pitchesThrown' in gameStats: gameStats['pitchesThrown'] = 0            
            awayPitchers.append(
                    player.Pitcher(pitcherName, gameStats["inningsPitched"], gameStats["hits"],
                        gameStats["runs"], gameStats["earnedRuns"], gameStats["baseOnBalls"],
                        gameStats["strikeOuts"], gameStats["pitchesThrown"], gameStats["strikes"],
                        seasonStats["era"], pitcher['person']["id"])
                    )

        for pitcherID in homeTeam["pitchers"]:
            pitcher = homeTeam["players"]["ID" + str(pitcherID)]
            gameStats = pitcher["stats"]["pitching"]
            seasonStats = pitcher["seasonStats"]["pitching"]
            pitcherName = pitcher["person"]["fullName"].strip()
            if not 'pitchesThrown' in gameStats: gameStats['pitchesThrown'] = 0
            homePitchers.append(
                    player.Pitcher(pitcherName, gameStats["inningsPitched"], gameStats["hits"],
                        gameStats["runs"], gameStats["earnedRuns"], gameStats["baseOnBalls"],
                        gameStats["strikeOuts"], gameStats["pitchesThrown"], gameStats["strikes"],
                        seasonStats["era"], pitcher['person']["id"])
                    )

        # Make home and away same size for the chart
        while len(homeBatters) < len(awayBatters):
            homeBatters.append(player.Batter())
        while len(awayBatters) < len(homeBatters):
            awayBatters.append(player.Batter())
        while len(homePitchers) < len(awayPitchers):
            homePitchers.append(player.Pitcher())
        while len(awayPitchers) < len(homePitchers):
            awayPitchers.append(player.Pitcher())

        #print(awayTeamInfo.keys())
        #print(awayTeamInfo["abbreviation"])
        boxscore += awayTeamInfo["abbreviation"] + "|Pos|AB|R|H|RBI|BB|SO||"
        boxscore += homeTeamInfo["abbreviation"] + "|Pos|AB|R|H|RBI|BB|SO||"
        boxscore += "\n"
        boxscore += ":--|:--|:--|:--|:--|:--|:--|:--|:--|"
        boxscore += ":--|:--|:--|:--|:--|:--|:--|:--|:--|"
        boxscore += "\n"
        for i in range(0, len(homeBatters)):
            boxscore += str(awayBatters[i]) + "|" + str(homeBatters[i]) + "\n"
        boxscore += "\n"
        boxscore += awayTeamInfo["abbreviation"] + "|IP|H|R|ER|BB|SO|P-S|ERA|"
        boxscore += homeTeamInfo["abbreviation"] + "|IP|H|R|ER|BB|SO|P-S|ERA|"
        boxscore += "\n"
        boxscore += ":--|:--|:--|:--|:--|:--|:--|:--|:--|"
        boxscore += ":--|:--|:--|:--|:--|:--|:--|:--|:--|"
        boxscore += "\n"
        for i in range(0, len(homePitchers)):
            boxscore += str(awayPitchers[i]) + "|" + str(homePitchers[i]) + "\n"
        boxscore += "\n\n"

        #print("Returning boxscore")
        return boxscore
        # except:
            # print "Missing data for boxscore, returning blank text..."
            # return boxscore

    def generateLinescore(self, data):
        #print("Generating line scores...")
        linescore = ""
        # try:
        game = data["gameData"]
        awayTeamName = game["teams"]["away"]["name"]
        homeTeamName = game["teams"]["home"]["name"]

        lineInfo = data["liveData"]["linescore"]
        inningsInfo = data["liveData"]["linescore"]["innings"]
        numInnings = lineInfo["currentInning"] if lineInfo["currentInning"] > 9 else 9

       # Table headers
        linescore += "Linescore|"
        for i in range(1, numInnings + 1):
            linescore += str(i) + "|"
        linescore += "R|H|E\n"
        for i in range(0, numInnings + 4):
            linescore += ":--|"

        # Away team linescore
        linescore += "\n" + awayTeamName + "|"
        for i in range( numInnings ):
            if i < lineInfo['currentInning'] and 'runs' in inningsInfo[i]['away']:
                linescore += f"{inningsInfo[i]['away']['runs']}|"
            else:
                linescore += '|'
        linescore += f"{lineInfo['teams']['away']['runs']}|{lineInfo['teams']['away']['hits']}|{lineInfo['teams']['away']['errors']}"

        # Home team linescore
        linescore += "\n" + homeTeamName + "|"
        for i in range( numInnings ):
            if i < lineInfo['currentInning'] and 'runs' in inningsInfo[i]['home']:
                linescore += f"{inningsInfo[i]['home']['runs']}|"
            else:
                linescore += '|'
        linescore += f"{lineInfo['teams']['home']['runs']}|{lineInfo['teams']['home']['hits']}|{lineInfo['teams']['home']['errors']}"

        linescore += "\n\n"
        #print("Returning linescore")
        return linescore
        # except:
            # print "Missing data for linescore, returning blank text..."
            # return linescore


    def generateScoringPlays(self, data):
        #print("Generating scoring plays")
        scoringPlays = ""

        allPlays = data["liveData"]["plays"]["allPlays"]
        teams = data["gameData"]["teams"]

        scoringPlays += "Inning|Scoring Play Description|Score\n"
        scoringPlays += ":--|:--|:--\n"

        for play in allPlays:
            if not "isScoringPlay" in play["about"].keys():
                continue
            if play["about"]["isScoringPlay"]:
                scoringPlays += f'{play["about"]["halfInning"]} {play["about"]["inning"]} | {play["result"]["description"]} |'

                # Put winning team's score first
                if int(play["result"]["homeScore"]) > int(play["result"]["awayScore"]):
                    scoringPlays += f'{play["result"]["homeScore"]}-{play["result"]["awayScore"]} {teams["home"]["abbreviation"]}'
                elif int(play["result"]["homeScore"]) < int(play["result"]["awayScore"]):
                    scoringPlays += f'{play["result"]["awayScore"]}-{play["result"]["homeScore"]} {teams["away"]["abbreviation"]}'
                else:
                    scoringPlays += f'{play["result"]["awayScore"]} - {play["result"]["homeScore"]}'
                scoringPlays += "\n"

        scoringPlays += "\n\n"
        #print("Returning scoringPlays")
        return scoringPlays

    def generateHighlights(self, data):
        #print("Generating highlights")
        highlightMarkdown = ""
        try:
            highlights = data["highlights"]["live"]["items"]
            highlightMarkdown += "|Team|Highlight|SD|HD|\n"
            highlightMarkdown += "|:--|:--|:--|:--|\n"
            for highlight in highlights:
                try:
                    highlightMarkdown += "|" + MarkdownGenerator.options[highlight["kicker"].replace("Highlights ", "").replace("Top Play ", "")]["tag"]
                except:
                    highlightMarkdown += "|[](/MLB)"
                SDHighlightURL = ""
                HDHighlightURL = ""
                for playback in highlight["playbacks"]:
                    if playback["name"] == "FLASH_1200K_640X360":
                        SDHighlightURL = playback["url"]
                    elif playback["name"] == "FLASH_2500K_1280X720":
                        HDHighlightURL = playback["url"]
                highlightMarkdown += "|" + highlight["headline"] + "|[SD](" + SDHighlightURL + ")|[HD](" + HDHighlightURL + ")|\n"

            highlightMarkdown += "\n\n"
            #print("Returning highlight")
            return highlightMarkdown
        except:
            print("Missing data for highlight, returning blank text")
            return highlightMarkdown

    def generateDecisions(self, data):
        #print('generating decisions...')
        decisions = ""
        # try:
        #homepitchers = []
        #awaypitchers = []
        decisionsData = data["liveData"]["decisions"]#["pitchers"]
        liveDataTeams = data["liveData"]["boxscore"]["teams"]
        gameDataTeams = data["gameData"]["teams"]
        winningPitcherID = str(decisionsData["winner"]["id"])
        losingPitcherID = str(decisionsData["loser"]["id"])
        #savePitcherID = str(decisionsData["save"]["id"])

        if "ID" + str(decisionsData["winner"]["id"]) in liveDataTeams["home"]["players"]:
            winningPitcher = liveDataTeams["home"]["players"]["ID" + winningPitcherID]
            losingPitcher = liveDataTeams["away"]["players"]["ID" + losingPitcherID]
            #if decisionsData["save"] is not None:
            #    savePitcher = liveDataTeams["home"]["players"]["ID" + savePitcherID]
            #else:
            #    savePitcher = None
            winningTeam = gameDataTeams["home"]["abbreviation"]
            losingTeam = gameDataTeams["away"]["abbreviation"]
        else:
            winningPitcher = liveDataTeams["away"]["players"]["ID" + winningPitcherID]
            losingPitcher = liveDataTeams["home"]["players"]["ID" + losingPitcherID]
            #if decisionsData["save"] is not None:
            #    savePitcher = liveDataTeams["away"]["players"]["ID" + savePitcherID]
            #else:
            #    savePitcher = None
            winningTeam = gameDataTeams["away"]["abbreviation"]
            losingTeam = gameDataTeams["home"]["abbreviation"]

        decisions += "|Decisions||" + "\n"
        decisions += "|:--|:--|" + "\n"
##        decisions += "|" + "[" + winningTeam + "](" + Editor.options[winningTeam]["sub"] + ")|"
        decisions += "|" + winningTeam + "|"
        decisions += "[" + winningPitcher["person"]["fullName"] + "](http://mlb.mlb.com/team/player.jsp?player_id=" + str(winningPitcher["person"]["id"]) + ")"
##        decisions += " " + winningPitcher["gameStats"]["pitching"]["note"]
        decisions += "\n"

##        decisions += "|" + "[" + losingTeam + "](" + Editor.options[losingTeam]["sub"] + ")|"
        decisions += "|" + losingTeam + "|"
        decisions += "[" + losingPitcher["person"]["fullName"] + "](http://mlb.mlb.com/team/player.jsp?player_id=" + str(losingPitcher["person"]["id"]) + ")"
##        decisions += " " + losingPitcher["gameStats"]["pitching"]["note"]
        decisions += "\n\n"
        #print("Returning decisions")
        return decisions
        # except:
            # print "Missing data for decisions, returning blank text..."
            # return decisions

    def generateDivisionStandings( self ):
        return generateDivisionStandings.generateDivisionStandings( self.division_code )

    def generateOffDayMarkdown( self ):
        body = generateDivisionStandings.generateDivisionStandings()
        body += "\n\nTalk amongst yourselves."
        return body
        

    def generateStatus(self, data):
        #print('generating status')
        #print("Entering editor.generate_status")
        status = ""
        # try:
        gameStatus = data["gameData"]["status"]["abstractGameState"]
        linescore = data["liveData"]["linescore"]
        homeTeamRuns = str(linescore["teams"]["home"]["runs"])
        awayTeamRuns = str(linescore["teams"]["away"]["runs"])
        homeTeamName = data["gameData"]["teams"]["home"]["abbreviation"]
        awayTeamName = data["gameData"]["teams"]["away"]["abbreviation"]

        if gameStatus in ("Game Over", "Final"):
            status += "## FINAL: "
            if int(homeTeamRuns) < int(awayTeamRuns):
                status += awayTeamRuns + "-" + homeTeamRuns + " " + awayTeamName + "\n\n"
                #status += self.generateDecisions(data)
                #print("Returning status")
                # return status
            elif int(homeTeamRuns) > int(awayTeamRuns):
                status += homeTeamRuns + "-" + awayTeamRuns + " " + homeTeamName + "\n\n"
                #status += self.generateDecisions(data)
                #print("Returning status")
                # return status
            elif int(homeTeamRuns) == int(awayTeamRuns):
                status += "TIE"
                #print(f"Returning status {status}")
                # return status
            
        elif gameStatus == "Completed Early":
            status += "## COMPLETED EARLY: "
            if int(homeTeamRuns) < int(awayTeamRuns):
                status += awayTeamRuns + "-" + homeTeamRuns + " " + awayTeamName + "\n\n"
                status += self.generateDecisions(data)
                #print(f"Returning status {status}")
                # return status
            elif int(homeTeamRuns) > int(awayTeamRuns):
                status += homeTeamRuns + "-" + awayTeamRuns + " " + homeTeamName + "\n\n"
                status += self.generateDecisions(data)
                #print(f"Returning status {status}")
                # return status
            elif int(homeTeamRuns) == int(awayTeamRuns):
                status += "TIE"
                #print(f"Returning status {status}")
                # return status
            
        elif gameStatus == "Postponed":
            status += "## POSTPONED\n\n"
            #print(f"Returning status {status}")
            # return status
        elif gameStatus == "Suspended":
            status += "## SUSPENDED\n\n"
            #print(f"Returning status {status}")
            # return status
        elif gameStatus == "Cancelled":
            status += "## CANCELLED\n\n"
            #print(f"Returning status {status}")
            # return status
        else:
            #print("Status not final or postponed, returning empty string")
            return ""
        return status
        # except:
            # print "Missing data for status, returning blank text..."
            # return status
