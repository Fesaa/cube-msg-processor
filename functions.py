import time
import json
import asyncio
import requests
from typing import Union
from constants import STAFF_ROLES

config = json.load(open('json/config.json', encoding='utf-8'))
TOKEN = config.get('TOKEN')

def check_staff(roles_list: list) -> bool:
    return bool(set(roles_list) & set(STAFF_ROLES))

def font_size(length: int) -> str:
    if length in range(0,10):
        return 'smaller'
    elif length in range(10,20):
        return 'small'
    elif length in range(20,30):
        return 'x-small'
    else:
        return 'xx-small'

def inv_dict(d: dict) -> dict:
    return {value: key for key, value in d.items()}

def colour_list(l: list[Union[float, int]]) -> list:
    ma = max(l)
    mi = min(l)
    out = []

    for entry in l:
        if entry >= 80/100 * (ma - mi) + mi:
            out.append('crimson')
        elif entry >= 60/100 * (ma - mi) + mi:
            out.append('sandybrown')
        elif entry >= 40/100 * (ma - mi) + mi:
            out.append('khaki')
        elif entry >= 20/100 * (ma - mi) + mi:
            out.append('chartreuse')
        else:
            out.append('royalblue')
    
    return out

ID_CACHE = {}
EXTERNAL_ID_CACHE = json.load(open('json/external_id_cache.json', encoding='ISO 8859-1'))
ID_LOAD_TIME = []

async def get_name_from_id(user_id: int, external: bool) -> str:
    start = time.time()

    if external:
        if str(user_id) in EXTERNAL_ID_CACHE:
            ID_LOAD_TIME.append(time.time() - start)
            return EXTERNAL_ID_CACHE[str(user_id)]
    
    if user_id in ID_CACHE:
        return ID_CACHE[user_id]
    else:
        while True:
            res = requests.get(f"https://discord.com/api/v9/users/{user_id}", headers={"Authorization": TOKEN})

            if str(res) == "<Response [429]>":
                time_out = res.json()['retry_after']
                print(f'Rate limited while fetching discord username, trying again in {time_out} ...')
                await asyncio.sleep(time_out)

            elif str(res) == "<Response [200]>":
                username = res.json()['username']

                if len(username) > 18:
                    username = username[:15] + '...'

                ID_CACHE[user_id] = username
                ID_LOAD_TIME.append(time.time() - start)

                return username

            else:
                return user_id

async def correct_dict_for_id(d: dict, external: bool) -> dict:
    return {await get_name_from_id(int(key), external) if key.isdigit() else key: value for key, value in d.items()}    