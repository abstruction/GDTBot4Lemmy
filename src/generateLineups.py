import statsapi

def generateLineups( gamePk ):
    
    data = statsapi.boxscore_data(gamePk)
    markdown = ""

    for team in ("home", "away"):
        
        BOids = data[team]['battingOrder']
        if BOids:
            
            markdown += "Name|avg.|OPS|HR|RBI\n"
            markdown += ":--|--:|--:|--:|--:|\n"
   
            players = data[team]['players']
            ids = [f'ID{id}' for id in BOids]
            battingOrder = [players[id] for id in ids]

            for player in battingOrder:
                stats = player['seasonStats']['batting']
                markdown += f"{player['person']['fullName']} - {player['position']['abbreviation']}|"
                markdown += '|'.join( str(stats[stat]) for stat in ('avg', 'ops', 'homeRuns', 'rbi') )
                markdown += '\n'

        markdown += '\n\n'

    return markdown




