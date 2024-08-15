import sqlite3
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from httpx import AsyncClient
import uuid
import random
import time
import os
import httpx
from loguru import logger

from dotenv import load_dotenv
import os

load_dotenv()  # env
git_token = os.getenv("GIT_TOKEN")
print("start hamster FAM")



API_TOKEN = '6786830495:AAHTn9FrVW65LfMzr2nOGZmCM4UyL26UsrU'
dev = 5527705092

from github import Github
import hashlib

# def is_file_changed_locally():
#     # Инициализация объекта GitHub с использованием персонального токена
#     g = Github(git_token)
    
#     # Получаем репозиторий
#     repo = g.get_user().get_repo('hamster_fam_db')
    
#     # Получаем содержимое файла game_keys.db с GitHub
#     contents = repo.get_contents('game_keys.db')
    
#     # Получаем MD5 текущего содержимого на GitHub
#     github_content_md5 = hashlib.md5(contents.decoded_content).hexdigest()
    
#     # Читаем локальный файл и вычисляем его MD5
#     with open('game_keys.db', 'rb') as file:
#         local_content = file.read()
#         local_content_md5 = hashlib.md5(local_content).hexdigest()
    
#     # Сравниваем MD5
#     if local_content_md5 != github_content_md5:
#         return True
#     else:
#         return False




# def download_file_from_github():
#     try:
#         if is_file_changed_locally():
#             # Инициализация объекта GitHub с использованием персонального токена
#             g = Github(git_token)
            
#             # Получаем репозиторий
#             repo = g.get_user().get_repo('hamster_fam_db')
            
#             # Получаем содержимое файла game_keys.db
#             contents = repo.get_contents('game_keys.db')
            
#             # Скачиваем файл
#             with open('game_keys.db', 'wb') as file:
#                 file.write(contents.decoded_content)
#                 print('File downloaded successfully.')
#         else:
#             pass
#     except Exception as e:
#         if "No such file or directory: 'game_keys.db'" in str(e):
#             g = Github(git_token)
            
#             # Получаем репозиторий
#             repo = g.get_user().get_repo('hamster_fam_db')
            
#             # Получаем содержимое файла game_keys.db
#             contents = repo.get_contents('game_keys.db')
            
#             # Скачиваем файл
#             with open('game_keys.db', 'wb') as file:
#                 file.write(contents.decoded_content)
#                 print('File downloaded successfully.')

# def upload_file_to_github():
#     if is_file_changed_locally():
#         # Инициализация объекта GitHub с использованием персонального токена
#         g = Github(git_token)
        
#         # Получаем репозиторий
#         repo = g.get_user().get_repo('hamster_fam_db')
        
#         # Читаем локальный файл game_keys.db
#         with open('game_keys.db', 'rb') as file:
#             content = file.read()
        
#         # Получаем содержимое файла game_keys.db на GitHub
#         contents = repo.get_contents('game_keys.db')
        
#         # Обновляем файл на GitHub
#         repo.update_file(contents.path, "Updated successfully", content, contents.sha)
#         print('File updated successfully.')
#     else:
#         pass

# Включаем логирование
logging.basicConfig(level=logging.INFO)
httpx_log = logging.getLogger("httpx")
httpx_log.setLevel(logging.ERROR)  # Устанавливаем уровень логирования для httpx

bot = Bot(token=API_TOKEN)
dp = Dispatcher()



games = {
    1: {'name': 'Riding Extreme 3D', 'appToken': 'd28721be-fd2d-4b45-869e-9f253b554e50', 'promoId': '43e35910-c168-4634-ad4f-52fd764a843f'},
    2: {'name': 'Chain Cube 2048', 'appToken': 'd1690a07-3780-4068-810f-9b5bbf2931b2', 'promoId': 'b4170868-cef0-424f-8eb9-be0622e8e8e3'},
    3: {'name': 'My Clone Army', 'appToken': '74ee0b5b-775e-4bee-974f-63e7f4d5bacb', 'promoId': 'fe693b26-b342-4159-8808-15e3ff7f8767'},
    4: {'name': 'Train Miner', 'appToken': '82647f43-3f87-402d-88dd-09a90025313f', 'promoId': 'c4480ac7-e178-4973-8061-9ed5b2e17954'},
    5: {'name': 'Merge Away','appToken': '8d1cc2ad-e097-4b86-90ef-7a27e19fb833','promoId': 'dc128d28-c45b-411c-98ff-ac7726fbaea4'}
}
chosen_game = {}
chosen_quantity = {}

EVENTS_DELAY = 20000 / 1000  # converting milliseconds to seconds


def get_users():
    # Установка соединения с базой данных
    conn = sqlite3.connect("game_keys.db")
    cursor = conn.cursor()

    try:
        # Выборка всех записей из таблицы MultiText
        cursor.execute(
            "SELECT id, full_name, username Content FROM users")
        rows = cursor.fetchall()

        # Формирование списка пар Id и Content
        id_content_pairs = [(row[0], row[1], row[2],) for row in rows]

        return id_content_pairs

    except sqlite3.Error as e:
        conn.commit()
        conn.close()
        print("Ошибка при выборке данных из базы данных:", e)
        return []
    finally:
        # Закрытие соединения
        conn.commit()
        conn.close()

filename = "users_data.txt"

def save_users_to_file(filename):
    try:
        with open(filename, 'w', encoding='utf-16') as file:
            file.write(f"Юзеры:\n")
            for user in get_users():
                file.write(f"ID: {user[0]}, ")
                file.write(f"Full Name: {user[1]}, ")
                file.write(f"Username: {user[2]}, ")
                file.write("\n")  # Добавляем пустую строку между записями
    except IOError as e:
        print(f"Ошибка при сохранении данных в файл {filename}: {e}")

def insert_or_update_user(id, full_name, username="-"):
    # Подключаемся к базе данных
    conn = sqlite3.connect('game_keys.db')
    cursor = conn.cursor()

    # Проверяем, существует ли пользователь с таким именем
    cursor.execute('''SELECT id FROM users WHERE id = ?''', (id,))
    existing_id = cursor.fetchone()

    if existing_id:
        # Если пользователь уже существует, обновляем время и имя пользователя
        cursor.execute(
            f'''UPDATE users SET full_name = "{full_name}", username = "{username}" WHERE id = {id}''')
    else:
        # Если пользователь не существует, добавляем новую запись с текущим временем
        cursor.execute('''INSERT INTO users (id, full_name, username) VALUES (?, ?, ?)''',
                       (id, full_name, username))

    # Закрываем соединение
    conn.commit()
    conn.close()


def setup_database():
    conn = sqlite3.connect('game_keys.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_name TEXT NOT NULL,
            promo_code TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS used_keys (
            count INTEGER NOT NULL
        )
    ''')
    conn.commit()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users
                      (id INTEGER NOT NULL,
                       full_name TEXT NOT NULL,
                       username TEXT)
    ''')
    conn.commit()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_limits (
            user_id INTEGER NOT NULL,
            game_name TEXT NOT NULL,
            keys_given INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (user_id, game_name)
        )
    ''')
    conn.commit()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reset_info (
            last_reset_date DATE NOT NULL
        )
    ''')
    conn.commit()
    
    # Инициализируем таблицу reset_info, если она пуста
    cursor.execute('SELECT COUNT(*) FROM reset_info')
    result = cursor.fetchone()[0]
    if result == 0:
        cursor.execute('INSERT INTO reset_info (last_reset_date) VALUES (DATE("1970-01-01"))')
        conn.commit()

    cursor.execute('SELECT COUNT(*) FROM used_keys')
    result = cursor.fetchone()[0]
    # print(result)
    if result != 1:
        # Если запись не найдена, вставляем новую запись
        cursor.execute('''
            INSERT INTO used_keys (count)
            VALUES (?)
        ''', (0,))
        conn.commit()
    conn.close()

def check_and_update_user_limit(user_id, game_name, quantity):
    conn = sqlite3.connect('game_keys.db')
    cursor = conn.cursor()
    
    # Проверка текущего количества выданных ключей
    cursor.execute('''
        SELECT keys_given
        FROM user_limits
        WHERE user_id = ? AND game_name = ?
    ''', (user_id, game_name))
    
    result = cursor.fetchone()
    if result:
        keys_given = result[0]
    else:
        # Если записи нет, создаем ее
        keys_given = 0
        cursor.execute('''
            INSERT INTO user_limits (user_id, game_name, keys_given)
            VALUES (?, ?, ?)
        ''', (user_id, game_name, keys_given))
    
    conn.commit()
    
    # Проверка, можем ли выдать еще ключи
    if keys_given + quantity > 4:  # Пример: лимит 5 ключей на пользователя в день
        conn.close()
        return False
    
    # Обновляем количество выданных ключей
    cursor.execute('''
        UPDATE user_limits
        SET keys_given = keys_given + ?
        WHERE user_id = ? AND game_name = ?
    ''', (quantity, user_id, game_name))
    
    conn.commit()
    conn.close()
    return True


    

def get_last_reset_date():
    conn = sqlite3.connect('game_keys.db')
    cursor = conn.cursor()
    cursor.execute('SELECT last_reset_date FROM reset_info LIMIT 1')
    result = cursor.fetchone()[0]
    conn.close()
    import datetime
    return datetime.datetime.strptime(result, '%Y-%m-%d').date()
def update_last_reset_date(date):
    conn = sqlite3.connect('game_keys.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE reset_info SET last_reset_date = ?', (date,))
    conn.commit()
    conn.close()


async def reset_daily_limits():
    # Ваш код для сброса лимитов здесь
    conn = sqlite3.connect('game_keys.db')
    cursor = conn.cursor()
    # Обновляем значение keys_given на 0 для всех записей
    cursor.execute('UPDATE user_limits SET keys_given = 0')
    conn.commit()
    conn.close()
    print("Сброс лимитов выполнен.")
    import datetime
    # Обновляем дату последнего сброса
    today = datetime.date.today()
    update_last_reset_date(today)


async def schedule_daily_reset():
    while True:
        import datetime
        now = datetime.datetime.now()
        last_reset_date = get_last_reset_date()
        next_reset = datetime.datetime.combine(last_reset_date + datetime.timedelta(days=1), datetime.time(5, 0))
        
        if now >= next_reset:
            # Выполняем сброс и обновляем дату последнего сброса
            await reset_daily_limits()
            next_reset += datetime.timedelta(days=1)
        
        # Рассчитываем количество секунд до следующего сброса
        seconds_until_reset = (next_reset - now).total_seconds()
        await asyncio.sleep(seconds_until_reset)



def get_key_statistics():
    conn = sqlite3.connect('game_keys.db')
    cursor = conn.cursor()
    
    # Получаем общее количество ключей
    cursor.execute('SELECT COUNT(*) FROM keys')
    total_keys = cursor.fetchone()[0]
    
    # Получаем количество ключей для каждой игры
    cursor.execute('SELECT DISTINCT game_name FROM keys')
    games = [row[0] for row in cursor.fetchall()]
    
    result = {'total_keys': total_keys}
    cursor.execute('''
        SELECT count
        FROM used_keys
        WHERE count IS NOT NULL
        LIMIT 1
    ''')
    count_used_keys = cursor.fetchone()[0]
    result['used_keys'] = str(count_used_keys)
    
    for game in games:
        cursor.execute('SELECT COUNT(*) FROM keys WHERE game_name = ?', (game,))
        count = cursor.fetchone()[0]
        result[game] = {'name':game, 'count':count}
    
    # print(result)

    conn.close()
    return result


def fetch_games(games=games):
    # conn = sqlite3.connect('game_keys.db')
    # cursor = conn.cursor()
    # cursor.execute('SELECT DISTINCT game_name FROM keys')
    # games = [row[0] for row in cursor.fetchall()]
    # conn.close()
    games_list = [game['name'] for game in games.values()]
    return games_list

def fetch_key_from_db(game_name):
    conn = sqlite3.connect('game_keys.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT promo_code
        FROM keys
        WHERE game_name = ?
        LIMIT 1
    ''', (game_name,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

def delete_key_from_db(game_name, promo_code):
    conn = sqlite3.connect('game_keys.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM keys
        WHERE game_name = ? AND promo_code = ?
    ''', (game_name, promo_code))

    cursor.execute('''
        UPDATE used_keys
        SET count = count + 1
        WHERE count IS NOT NULL
    ''')
    conn.commit()
    conn.close()

async def generate_client_id():
    timestamp = int(time.time() * 1000)
    random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(19))
    return f"{timestamp}-{random_numbers}"

async def login(client_id, app_token, proxy=None):
    async with AsyncClient(proxies=proxy) as client:
        response = await client.post(
            'https://api.gamepromo.io/promo/login-client',
            json={'appToken': app_token, 'clientId': client_id, 'clientOrigin': 'deviceid'}
        )
        response.raise_for_status()
        data = response.json()
        return data['clientToken']

async def emulate_progress(client_token, promo_id, proxy=None):
    async with AsyncClient(proxies=proxy) as client:
        response = await client.post(
            'https://api.gamepromo.io/promo/register-event',
            headers={'Authorization': f'Bearer {client_token}'},
            json={'promoId': promo_id, 'eventId': str(uuid.uuid4()), 'eventOrigin': 'undefined'}
        )
        response.raise_for_status()
        data = response.json()
        return data['hasCode']

async def generate_key(client_token, promo_id, proxy=None):
    async with AsyncClient(proxies=proxy) as client:
        response = await client.post(
            'https://api.gamepromo.io/promo/create-code',
            headers={'Authorization': f'Bearer {client_token}'},
            json={'promoId': promo_id}
        )
        response.raise_for_status()
        data = response.json()
        return data['promoCode']

async def generate_key_process(app_token, promo_id, proxy=None):
    client_id = await generate_client_id()
    try:
        client_token = await login(client_id, app_token, proxy)
    except httpx.HTTPStatusError as e:
        logging.error(f"Failed to login: {e.response.json()}")
        return None

    for _ in range(11):
        await asyncio.sleep(EVENTS_DELAY * (random.random() / 3 + 1))
        try:
            has_code = await emulate_progress(client_token, promo_id, proxy)
        except httpx.HTTPStatusError as e:
            continue

        if has_code:
            break

    try:
        key = await generate_key(client_token, promo_id, proxy)
        return key
    except httpx.HTTPStatusError as e:
        logging.error(f"Failed to generate key: {e.response.json()}")
        return None

async def save_key_to_db(game_name, key):
    conn = sqlite3.connect('game_keys.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO keys (game_name, promo_code)
        VALUES (?, ?)
    ''', (game_name, key))
    conn.commit()
    conn.close()

async def generate_keys_for_game(game_choice, proxy):
    game = games[game_choice]
    game_name = game['name']
    while True:
        key = await generate_key_process(game['appToken'], game['promoId'], proxy)
        if key:
            logging.info(f"Generated key for {game_name}: {key}")
            await save_key_to_db(game_name, key)
        else:
            logging.error(f"No key was generated for {game_name}.")
        await asyncio.sleep(EVENTS_DELAY * (random.random() / 3 + 1))


@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    static_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Получить ключ")],[KeyboardButton(text="Количество ключей")]],
        resize_keyboard=True
    )
    await message.answer(
        "Нажмите кнопку ниже, чтобы получить ключ.", 
        reply_markup=static_keyboard
    )
    try:
        username = f"{message.from_user.username}" if message.from_user.username is None else f"@{message.from_user.username}"
        insert_or_update_user(
            message.from_user.id, message.from_user.full_name, f"{username}")
    except Exception as e:
        print(f"{message.from_user.id}, {message.from_user.full_name}, {message.from_user.username}\n\n{e}")
        await message.bot.send_message(chat_id=dev, text="Ошибка в базе данных при добавлении!")

@dp.message(lambda msg: msg.text == "Получить ключ")
async def ask_for_game(message: types.Message):
    games = fetch_games()
    if games:
        game_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=game, callback_data=f"choose_game_{game}")] for game in games
            ]
        )
        await message.answer(
            text="Выберите игру:",
            reply_markup=game_keyboard
        )
        await message.delete()
    else:
        await message.answer(
            text="Нет доступных игр."
        )
    try:
        username = f"{message.from_user.username}" if message.from_user.username is None else f"@{message.from_user.username}"
        insert_or_update_user(
            message.from_user.id, message.from_user.full_name, f"{username}")
    except Exception as e:
        print(f"{message.from_user.id}, {message.from_user.full_name}, {message.from_user.username}\n\n{e}")
        await message.bot.send_message(chat_id=dev, text="Ошибка в базе данных при добавлении!")

@dp.callback_query(lambda c: c.data.startswith("choose_game_"))
async def choose_game(callback_query: types.CallbackQuery):
    game_name = callback_query.data[len("choose_game_"):]
    chosen_game[callback_query.from_user.id] = game_name
    user_id = callback_query.from_user.id
    # Проверяем количество доступных ключей для выбранной игры
    conn = sqlite3.connect('game_keys.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT keys_given
        FROM user_limits
        WHERE game_name = ? AND user_id = ?
    ''', (game_name, user_id,))
    available_keys = cursor.fetchone()
    conn.close()
    print(f"{available_keys}\n{user_id}")
    if available_keys == None:
        available_keys = 4
    else:
        available_keys = abs(available_keys[0] - 4)
    print(available_keys)
    # ####Устанавливаем максимальное количество ключей на пользователя
    if available_keys == 0:
        await bot.edit_message_text(
            text=f"Вы превысили лимит ключей {game_name} на сегодня, приходите завтра!",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id
        )
        return
    # elif available_keys ==
    
    quantity_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=str(i), callback_data=f"choose_quantity_{i}") for i in range(1, available_keys+1)]
        ]
    )
    
    await bot.edit_message_text(
        text=f"Вы выбрали {game_name}. Выберите количество ключей:",
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=quantity_keyboard
    )

@dp.callback_query(lambda c: c.data.startswith("choose_quantity_"))
async def choose_quantity(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    quantity = int(callback_query.data[len("choose_quantity_"):])
    game_name = chosen_game.get(user_id)
    
    if game_name:
        # Проверяем лимиты
        if not check_and_update_user_limit(user_id, game_name, quantity):
            await bot.edit_message_text(
                message_id=callback_query.message.message_id,
                chat_id=callback_query.message.chat.id,
                text="Вы превысили лимит ключей на сегодня.",
                reply_markup=None
            )
            return
        
        keys_sent = 0
        keys_to_send = []
        
        while keys_sent < quantity:
            key = fetch_key_from_db(game_name)
            if key:
                delete_key_from_db(game_name, key)
                keys_to_send.append(f"`{key}`")
                keys_sent += 1
            else:
                await bot.edit_message_text(
                    message_id=callback_query.message.message_id,
                    chat_id=callback_query.message.chat.id,
                    text=f"Ключи для {game_name} закончились.",
                    parse_mode="MarkdownV2"
                )
                break
        
        if keys_to_send:
            keys_message = f"Ваши {quantity} ключа для **{game_name}**:\n\n" + "\n".join(keys_to_send)
            await bot.edit_message_text(
                message_id=callback_query.message.message_id,
                chat_id=callback_query.message.chat.id,
                text=keys_message,
                parse_mode="MarkdownV2"
            )
        
        chosen_game.pop(user_id, None)
        chosen_quantity.pop(user_id, None)
    else:
        await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text="Произошла ошибка при выборе игры.",
            reply_markup=None
        )



    
    # await bot.edit_message_text(
    #     text="Количество ключей выбрано.",
    #     chat_id=callback_query.message.chat.id,
    #     message_id=callback_query.message.message_id,
    #     reply_markup=None
    # )



@dp.message(lambda msg: msg.text == "Количество ключей")
async def keys_for_game(message: types.Message):
    games = get_key_statistics()
    text = ""
    msggg = ""
    try:   
        for game in games:
            if game == 'total_keys':
                text += f"Общие ключи: {games[game]}\n"
            elif game == 'used_keys':
                text += f"Использованные ключи: {games[game]}\n"
            else:
                # Правильный доступ к вложенным словарям
                if not "Статистика по играм:\n" in text:
                    text += f"Статистика по играм:\n"
                msggg += f"{games[game]['name']}: {games[game]['count']}\n"
    except Exception as e:
        text = f"Ошибка доступа к ключу: {e}\n"
    text = f"{text}```\n{msggg}```"
    await message.answer(text, parse_mode="MarkdownV2")
    await message.delete()
    try:
        username = f"{message.from_user.username}" if message.from_user.username is None else f"@{message.from_user.username}"
        insert_or_update_user(
            message.from_user.id, message.from_user.full_name, f"{username}")
    except Exception as e:
        print(f"{message.from_user.id}, {message.from_user.full_name}, {message.from_user.username}\n\n{e}")
        await message.bot.send_message(chat_id=dev, text="Ошибка в базе данных при добавлении!")


    

@dp.message(Command("users"))
async def without_puree(message: types.Message):
    if message.from_user.id == dev:
        save_users_to_file(filename)
        document = FSInputFile(filename)
        await bot.send_document(
            chat_id=message.from_user.id,
            caption=f"Юзеры",
            document=document,
            parse_mode="MarkdownV2"
        )
    else:
        await message.reply("У вас недостаточно прав чтобы выполнить эту команду!")

            

async def load_proxy(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                proxy = file.read().strip()
                return proxy
        else:
            logger.info(f"Proxy file {file_path} not found. No proxy will be used.")
            return None
    except Exception as e:
        logger.error(f"Error reading proxy file {file_path}: {e}")
        return None

async def main(proxy):
    tasks = [asyncio.create_task(generate_keys_for_game(game_id, proxy)) for game_id in games.keys()]
    tasks.append(asyncio.create_task(schedule_daily_reset()))
    await dp.start_polling(bot)
    await asyncio.gather(*tasks)

# async def bot_main():

if __name__ == "__main__":
    setup_database()
    # proxy_file = input("Enter the proxy file path (leave empty to use 'proxy.txt'): ") or 'proxy.txt'
    # proxy_file = "proxy.txt"
    proxy_file = ""
    proxy = asyncio.run(load_proxy(proxy_file))

    logging.info(f"Generating keys for all games using proxy from {proxy_file if proxy else 'no proxy'}")
    asyncio.run(main(proxy))
    # asyncio.run(bot_main())
