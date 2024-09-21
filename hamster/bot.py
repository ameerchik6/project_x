import asyncio
import aiohttp

async def check_withdraw(session, token):
    url = 'https://api.hamsterkombatgame.io/interlude/sync'
    headers = {
        'Authorization': token,
        'Accept': '*/*',
    }

    async with session.post(url, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            print('Response:', data["interludeUser"]["withdraw"])
            try:
                return data["interludeUser"]["withdraw"]['info']['Binance']['memo']
            except:
                return "reset"
        else:
            print('Error:', response.status, await response.text())

async def reset_withdraw(session, token):
    url = 'https://api.hamsterkombatgame.io/interlude/withdraw/reset'
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    async with session.post(url, headers=headers, json={}) as response:
        if response.status == 200:
            print('Reset success')
        else:
            print('Error:', response.status, await response.text())

async def set_exchange_as_default(session, token):
    reset_withdraw(session, token)
    url = 'https://api.hamsterkombatgame.io/interlude/withdraw/set-exchange-as-default'
    payload = {
        "id": "Binance",
        "depositAddress": "EQD5mxRgCuRNLxKxeOjG6r14iSroLF5FtomPnet-sgP5xNJb",
        "memo": "106671155"
    }

    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    async with session.post(url, headers=headers, json=payload) as response:
        if response.status == 200:
            print("Exchange set as default successfully")
        else:
            await reset_withdraw(session, token)
            print('Error:', response.status, await response.text())

async def main():
    token = 'Bearer 1726906759241lJh990fZfFHhdVwQfN6mJ0nFTSsbpHtI34Q6ijfboKdNxG87ZXrBUhuqxgiiSsAk5527705092'
    
    async with aiohttp.ClientSession() as session:
        while True:
            if check_withdraw(session, token) == 106671155:
                continue
            await set_exchange_as_default(session, token)
            await check_withdraw(session, token)
            await set_exchange_as_default(session, token)
            await reset_withdraw(session, token)
            await set_exchange_as_default(session, token)
            # await asyncio.sleep(10)  # Задержка между итерациями

if __name__ == '__main__':
    asyncio.run(main())
