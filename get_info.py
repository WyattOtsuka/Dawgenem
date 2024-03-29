import calculate
import requests
import json
import pandas as pd
from pyrate_limiter import BucketFullException
import datetime as dt
import time
import asyncio
from aiohttp import ClientSession

limiter = None
data = None

with open('./secrets/secret.json') as f:
    data = json.load(f)

key = data['api_key']

base_url = data['base_url']
headers = {
    "X-Riot-Token": key
}

def get_summoner_puuid_by_name(name, prev_err = False):
    print(f'Entering get_summoner_puuid_by_name with uname {name}')
    try:
        limiter.try_acquire('identity')
        resp = requests.get(base_url + "summoner/v4/summoners/by-name/" + name, headers=headers)
    except BucketFullException as err:
        if not prev_err:
            print("\nRate Limited in get_summoner_puuid_by_name!")
            print(f"\t{err}")
            print(f"\tSleeping for {err.meta_info['remaining_time'] + 1}")
            loading(err.meta_info['remaining_time'] + 1)
            return get_summoner_puuid_by_name(name, True)
        else:
            print("Errored out twice on get_summoner_puuid_by_name!")
            print(f"\t{err}")

    if resp.status_code == 404:
        return "Summoner Not Found"
    elif resp.status_code != 200:
        print("Non-200 in get_summoner_puuid_by_name")
        print("\t" + resp.text)
        
    else:
        return resp.json()["puuid"]
        
def get_matches_by_puuid(puuid, start = 0, count = 10, prev_err = False):
    print(f'Entering get_matches_by_puuid with puuid {puuid}')
    url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids"
    url += f"?start={start}&count={count}"
    try:
        limiter.try_acquire('identity')
        resp = requests.get(url, headers=headers)
    except BucketFullException as err:
        if not prev_err:
            print("\nRate Limited in get_matches_by_puuid!")
            print(f"\t{err}")
            print(f"\tSleeping for {err.meta_info['remaining_time'] + 1}")
            loading(err.meta_info['remaining_time'] + 1)
            return get_matches_by_puuid(puuid, start, count, True)
        else:
            print("Errored out twice on get_matches_by_puuid!")
            print(f"\t{err}")

    if resp.status_code != 200:
        print("Non-200 in get_matches_by_puuid")
        print("\t" + resp.text)
    else:
        return resp.json()
    
async def get_match_by_match_id(id: str, session, count):
    url = "https://americas.api.riotgames.com/lol/match/v5/matches/" + id
    async with limiter.ratelimit('identity', delay = True):
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                print(f"Non-200 in get_match_by_match_id. Idx {count}")
                print("\t" + await resp.text())
            else:
                return await resp.json()
        
    

def process_match_data(match_data, puuid):
    '''
    Takes in a match to process, and a player id. Returns the following array: [overall score, dog/cat points, moon phase points, kda points].
    '''

    player_position = match_data['metadata']['participants'].index(puuid)
    player_stats = match_data['info']['participants'][player_position]
    kda = (player_stats['kills'] + player_stats['assists']) / player_stats['deaths'] if player_stats['deaths'] > 0 else (player_stats['kills'] + player_stats['assists']) * 2
    startdate = dt.datetime.utcfromtimestamp(match_data['info']['gameStartTimestamp'] / 1000).strftime("%Y/%m/%d")
    outcome = player_stats["nexusLost"] == 0
    champ = player_stats["championName"]

    return calculate.calculate(startdate, outcome, champ, kda)

    

async def get_data_and_calculate_score(username) -> str:
    print(f'Entering get_info with uname {username}')
    puuid = get_summoner_puuid_by_name(username)
    if puuid == None:
        print("Error in getting puuid")
        return "err"
    elif puuid == "Summoner Not Found":
        return "NotFound"
    else:
        start = 0
        matches = []
        count = 1

        match_list = get_matches_by_puuid(puuid)
        matches.extend(match_list)

        # Uncomment if you want to load more than 100 matches
        # while True:
        #    match_list = get_matches_by_puuid(puuid)
        #    matches.extend(match_list)
        #    count += 1
        # 
        #    if count % 4 == 0:
        #        loading = "\\"
        #    elif count % 4 == 1:
        #        loading = "|"
        #    elif count % 4 == 2:
        #        loading = "/"
        #    elif count % 4 == 3:
        #        loading = "-"
        #    print ("\r", " Completed ", count, " requests", end="")
        #    if len(match_list) < 100 or count > 2:
        #        print('\n')
        #        break

        tasks = []
        overall_score = 0
        moon_points = 0
        dog_cat_points = 0
        kda_points = 0
        async with ClientSession(trust_env=True) as session:
            for match_id in matches:
                count += 1
                task = asyncio.ensure_future(get_match_by_match_id(match_id, session, count))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
            for response in responses:
                results = process_match_data(response, puuid)
                overall_score += results[0]
                moon_points += results[1]
                dog_cat_points += results[2]
                kda_points += results[3]
        normalized_results = [100* points / (count - 1) for points in results]
        return(normalized_results)

def get_score(username, rate_limiter):
    global limiter
    limiter = rate_limiter    
    return asyncio.run(get_data_and_calculate_score(username))

def loading(max):
    count = 0
    while count < max:
        count += 1
        time.sleep(1)
        if count % 4 == 0:
            loading = "\\"
        elif count % 4 == 1:
            loading = "|"
        elif count % 4 == 2:
            loading = "/"
        elif count % 4 == 3:
            loading = "-"
        print ("\r", loading, end="")
