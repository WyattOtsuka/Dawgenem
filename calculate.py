import ephem
import math

gatech = ephem.Observer()
gatech.lon, gatech.lat = '41.8781', '87.6298'
moon = ephem.Moon()
moon.compute(gatech)

def phase_percent(year, month, day) -> float:
    '''
    Takes in a year, month, and day, and returns percent of moon that was illuminated
    during that time in Chicago. 

    TODO - implement allowing for different regions
    '''
    moon.compute('/'.join([year, month, day]))
    return moon.phase

def calculate(date, win, champ, kda) -> float:
    '''
    Takes in a date at which a game was played, whether the game was a win or a loss, 
    The champion played, and the KDA. Returns a score of how much dog in them.
    '''
    tally = 0
    year, month, day = date.split('/')
    moon_phase = phase_percent(year, month, day)

    if win:
        if champ == 'Warwick' or champ == 'Nasus': # +1 for playing dog
            if moon_phase > 50:
                tally += 2
        elif champ == 'Yuumi' or champ == 'Rengar': # -1 penalty for playing cat
            if moon_phase < 50:
                tally -= 2
        elif champ == 'Nidalee':
            if moon_phase > 50:
                tally += 0.5
            else:
                tally -= 1.5
        else:
            if moon_phase > 50:
                tally += 1
            else:
                tally -= 1
    else:
        if champ == 'Warwick' or champ == 'Nasus': # +1 for playing dog
            if moon_phase < 50:
                tally += 2
        elif champ == 'Yuumi' or champ == 'Rengar': # -1 penalty for playing cat
            if moon_phase > 50:
                tally -= 2
        elif champ == 'Nidalee': # Half the cat, half the penalty
            if moon_phase < 50:
                tally += 0.5
            else:
                tally -= 1.5
        else:
            if moon_phase < 50:
                tally += 1
            else:
                tally -= 1
        
    tally += math.atan(kda-2) * (2/math.pi)

    return tally * (moon_phase + 50) / 100