import statsapi

def generateLineups( gamePk=717417 ):
    data = statsapi.boxscore_data(gamePk)
    
    homeBOids = data['home']['battingOrder']
    #print(data['home']['team']['id'])

    markdown = "Name|avg.|OPS|HR|RBI\n"
    markdown += ':--|' * 5
    markdown += '\n'
    
    if homeBOids:
        homePlayers = data['home']['players']
        ids = [f'ID{id}' for id in homeBOids]
        battingOrder = [homePlayers[id] for id in ids]

        for p in battingOrder:
            stats = p['seasonStats']['batting']
            markdown += f"{p['person']['fullName']} - {p['position']['abbreviation']}|"
            markdown += '|'.join( str(stats[stat]) for stat in ('avg', 'ops', 'homeRuns', 'rbi') )
            markdown += '\n'
    markdown += '\n\n'

    awayBOids = data['away']['battingOrder']
    markdown += "Name|avg.|OPS|HR|RBI\n"
    markdown += ':--|' * 5
    markdown += '\n'
    
    if awayBOids:
        awayPlayers = data['away']['players']
        ids = [f'ID{id}' for id in awayBOids]
        battingOrder = [awayPlayers[id] for id in ids]

        for p in battingOrder:
            stats = p['seasonStats']['batting']
            markdown += f"{p['person']['fullName']} - {p['position']['abbreviation']}|"
            markdown += '|'.join( str(stats[stat]) for stat in ('avg', 'ops', 'homeRuns', 'rbi') )
            markdown += '\n'
    markdown += '\n\n'
    
    #print(markdown)
    return markdown




