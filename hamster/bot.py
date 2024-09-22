import asyncio
import aiohttp
import random

TOKEN = 'Bearer 1726906759241lJh990fZfFHhdVwQfN6mJ0nFTSsbpHtI34Q6ijfboKdNxG87ZXrBUhuqxgiiSsAk5527705092'

async def check_withdraw(session):
    url = 'https://api.hamsterkombatgame.io/interlude/sync'
    headers = {
        'Authorization': TOKEN,
        'Accept': '*/*',
    }

    try:
        async with session.post(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data["interludeUser"]["withdraw"]['info']['Binance']['memo']
            else:
                print('Error:', response.status, await response.text())
                return None
    except Exception as e:
        print(f"Ошибка при проверке вывода: {e}")
        return None

async def reset_withdraw(session):
    url = 'https://api.hamsterkombatgame.io/interlude/withdraw/reset'
    headers = {
        'Authorization': TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    try:
        async with session.post(url, headers=headers, json={}) as response:
            if response.status == 200:
                print('Успешно сброшено')
            else:
                print('Error:', response.status, await response.text())
    except Exception as e:
        print(f"Ошибка при сбросе вывода: {e}")

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

    try:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                print("Успешно установлено по умолчанию")
            else:
                print('Error:', response.status, await response.text())
    except Exception as e:
        print(f"Ошибка при установке обмена по умолчанию: {e}")

async def task():
    async with aiohttp.ClientSession() as session:
        while True:
            memo = await check_withdraw(session)
            print(memo)

            if memo == "106671155":
                print("Пропущено")
                await asyncio.sleep(random.uniform(0.1, 0.5))  # Задержка перед следующим запросом
                continue
            elif memo == "reset" or memo is None:
                await reset_withdraw(session)

            await set_default_exchange(session)

            # Случайная задержка между запросами
            await asyncio.sleep(random.uniform(0.1, 0.5))

async def main():
    tasks = [asyncio.create_task(task()) for _ in range(10)]  # Создаем 10 задач
    await asyncio.gather(*tasks)

# Запускаем основной цикл
if __name__ == "__main__":
    asyncio.run(main())
