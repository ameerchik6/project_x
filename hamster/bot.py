import requests
import time
def check_withdraw():
    url = 'https://api.hamsterkombatgame.io/interlude/sync'
    token = 'Bearer 1726906759241lJh990fZfFHhdVwQfN6mJ0nFTSsbpHtI34Q6ijfboKdNxG87ZXrBUhuqxgiiSsAk5527705092'

    headers = {
        'Authorization': token,
        'Accept': '*/*',
    }

    # Отправляем POST-запрос с пустым телом
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            return data["interludeUser"]["withdraw"]['info']['Binance']['memo']
        except:
            return "reset"
    else:
        print('Error:', response.status_code, response.text)


def reset_withdraw():
    url = 'https://api.hamsterkombatgame.io/interlude/withdraw/reset'
    token = 'Bearer 1726906759241lJh990fZfFHhdVwQfN6mJ0nFTSsbpHtI34Q6ijfboKdNxG87ZXrBUhuqxgiiSsAk5527705092'

    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    response = requests.post(url, headers=headers, json={})

    if response.status_code == 200:
        # print('Response:', response.json())
        print('success reseted')
    else:
        print('Error:', response.status_code, response.text)



while True:
    print(check_withdraw())
    if check_withdraw() == 106671155:
        continue
    elif check_withdraw() == "reset":
        reset_withdraw()

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

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        # print('Response:', response.json())
        print("success")
    else:
        print('Error:', response.status_code, response.text)
    

