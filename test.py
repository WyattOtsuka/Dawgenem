import calculate

new_moon_date = '2022/1/2'
full_moon_date = '2022/1/17'
kdas = [0.5, 2, 5]
champs = ['Warwick', 'Yuumi', 'Nidalee', 'Other']
outcomes = [True, False]
moons = [new_moon_date, full_moon_date]
for champ in champs:
    for kda in kdas:
        for moon in moons:
            for outcome in outcomes:
            
                score = calculate.calculate(moon, outcome, champ, kda)
                if outcome:
                    game = "win"
                else:
                    game = "Loss"
                if moon == new_moon_date:
                    phase = "NM: "
                else:
                    phase = "FM: "
                print(" ".join([phase, champ, game, str(kda)]) + ": " + str(score))