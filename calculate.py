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
    The champion played, and the KDA. Returns [overall score, moon phase points, dog/cat points, kda points].
    '''
    tally = 0
    dog_cat = 0
    year, month, day = date.split('/')
    moon_phase = phase_percent(year, month, day)

    if win:
        if champ == 'Warwick' or champ == 'Nasus' or champ == 'Naafiri': # +1 for playing dog
            dog_cat = 1
            if moon_phase > 50:
                tally += 2
        elif champ == 'Yuumi' or champ == 'Rengar': # -1 penalty for playing cat
            dog_cat = -1
            if moon_phase < 50:
                tally -= 2
        elif champ == 'Nidalee':
            dog_cat = -0.5
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
        if champ == 'Warwick' or champ == 'Nasus' or champ == 'Naafiri': # +1 for playing dog
            dog_cat = 1
            if moon_phase < 50:
                tally += 2
        elif champ == 'Yuumi' or champ == 'Rengar': # -1 penalty for playing cat
            dog_cat = -1
            if moon_phase > 50:
                tally -= 2
        elif champ == 'Nidalee': # Half the cat, half the penalty
            dog_cat = -0.5
            if moon_phase < 50:
                tally += 0.5
            else:
                tally -= 1.5
        else:
            if moon_phase < 50:
                tally += 1
            else:
                tally -= 1
    
    kda_points = math.atan(kda-2) * (2/math.pi)

    tally += kda_points

    overall_score = tally * (moon_phase + 50) / 100
    moon_phase_points = 0
    if win: 
        moon_phase_points = 2 * (moon_phase - 50) / 100
    else: 
        moon_phase_points = 2 * (50 - moon_phase) / 100
    return [overall_score, moon_phase_points, dog_cat, kda_points]


# Dog Skins:
# Pug'maw 
# (prestige) Fuzz Fizz
# Corgi Corki
#  
# 
# Cat Skins:
# Meowrick
# Meowkai
# Kitty Katarina
# Space Groove Blitz
# (presitge) battle cat jinx
