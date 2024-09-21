import aiohttp
import asyncio

url = 'https://api.hamsterkombatgame.io/interlude/withdraw/set-exchange-as-default'
token = 'Bearer 1726906759241lJh990fZfFHhdVwQfN6mJ0nFTSsbpHtI34Q6ijfboKdNxG87ZXrBUhuqxgiiSsAk5527705092'

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

async def send_request(session):
    async with session.post(url, headers=headers, json=payload) as response:
        if response.status == 200:
            print("success")
        else:
            print(f"Error: {response.status}, {await response.text()}")

async def run_requests():
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [send_request(session) for _ in range(10)]  # Создаём 10 задач без задержек
            await asyncio.gather(*tasks)  # Выполняем их параллельно

if __name__ == "__main__":
    asyncio.run(run_requests())
