import statsapi

def generateDivisionStandings( divisionCode=201 ):
    try:
        standingsData = statsapi.standings_data()
    except Exception as e:
        print(e)
        return ""
        
    standings = standingsData[divisionCode]
    table = f"{standings['div_name']} Standings\n\n"
    table += "|Rank|Team|W|L|GB|\n"
    table += ":--|:--|:--|:--|:--|\n"
    for team in standings['teams']:
        # table += "|".join((team['div_rank'], team['name'], team['w'], team['l'], team['gb']))
        table += "|".join( [str(team[i]) for i in ('div_rank', 'name', 'w', 'l', 'gb')] )
        # table += f"{team['div_rank']}|{team['name']}|{team['w']}|{team['l']}|{team['gb']}"
        table += '\n'
    return table
    
