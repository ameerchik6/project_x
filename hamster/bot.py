import asyncio
import aiohttp
import time
import random

TOKEN = 'Bearer 1726906759241lJh990fZfFHhdVwQfN6mJ0nFTSsbpHtI34Q6ijfboKdNxG87ZXrBUhuqxgiiSsAk5527705092'

async def check_withdraw(session):
    url = 'https://api.hamsterkombatgame.io/interlude/sync'
    headers = {
        'Authorization': TOKEN,
        'Accept': '*/*',
    }

    async with session.post(url, headers=headers) as response:
        if response.status == 200:
            try:
                data = await response.json()
                return data["interludeUser"]["withdraw"]['info']['Binance']['memo']
            except:
                return "reset"
        else:
            print('Error:', response.status, await response.text())
            return None

async def reset_withdraw(session):
    url = 'https://api.hamsterkombatgame.io/interlude/withdraw/reset'
    headers = {
        'Authorization': TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    async with session.post(url, headers=headers, json={}) as response:
        if response.status == 200:
            print('success reseted')
        else:
            print('Error:', response.status, await response.text())

async def set_default_exchange(session):
    url = 'https://api.hamsterkombatgame.io/interlude/withdraw/set-exchange-as-default'
    payload = {
        "id": "Binance",
        "depositAddress": "EQD5mxRgCuRNLxKxeOjG6r14iSroLF5FtomPnet-sgP5xNJb",
        "memo": "106671155"
    }
    headers = {
        'Authorization': TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    async with session.post(url, headers=headers, json=payload) as response:
        if response.status == 200:
            print("success")
        else:
            # print('Error:', response.status, await response.text())
            pass

async def task():
    async with aiohttp.ClientSession() as session:
        while True:
            memo = await check_withdraw(session)
            print(memo)

            if memo == 106671155:
                print("skipped")
                continue
            elif memo == "reset":
                await reset_withdraw(session)
            else:
                await reset_withdraw(session)

            await set_default_exchange(session)

            # Случайная задержка между запросами
            await asyncio.sleep(random.uniform(0.1, 0.5))

async def main():
    tasks = []
    
    # Создаем 10 задач, которые будут выполняться параллельно
    for _ in range(10):
        tasks.append(asyncio.create_task(task()))

    await asyncio.gather(*tasks)

# Запускаем основной цикл
asyncio.run(main())
