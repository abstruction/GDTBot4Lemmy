import statsapi
from datetime import datetime

def generateDivisionStandings( divisionCode=201 ):
    try:
        standingsData = statsapi.standings_data()
    except Exception as e:
        print(e)
        return ""
        
    standings = standingsData[divisionCode]
    timeString = datetime.now().strftime("%m/%d/%Y %H:%M")
    table  = f"{standings['div_name']} Standings\n"
    table += f"as of {timeString}\n\n"
    table += "|Rank|Team|W|L|GB|\n"
    table += ":--|:--|:--|:--|:--|\n"
    for team in standings['teams']:
        table += "|".join( [str(team[i]) for i in ('div_rank', 'name', 'w', 'l', 'gb')] )
        table += '\n'
    return table + '\n\n'
