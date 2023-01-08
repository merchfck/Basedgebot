from settings import bot_name, postgres_host, postgres_user, postgres_password, postgres_title
import random
from datetime import datetime
import psycopg2
import requests
import ast
from bs4 import BeautifulSoup

# TODO 1.почистить отладчик от twitchio.ext.commands.errors.CommandNotFound: No command "Смешнее" was found.
#      2.на каждый канал отдельный профиль

connection = psycopg2.connect(
    host=postgres_host,
    user=postgres_user,
    password=postgres_password,
    database=postgres_title
)

connection.autocommit = True
cursor = connection.cursor()

cursor.execute(
    f'''CREATE TABLE IF NOT EXISTS {bot_name}_base(
    id serial,
    username text PRIMARY KEY,
    display_name text,
    emote text
    );'''
)

def chat_output(message):
    return [datetime.utcnow().strftime('%H:%M:%S'), "#" + message.channel.name, message.author.display_name, message.content]

def prefix_emote(channel):
    global_emotes = ["reckH", "Stare", "PETPET", "SteerR", "PartyParrot", "ApuApustaja", "Gayge", "YEAHBUT7TV", "PepePls", "BillyApprove", "WAYTOODANK",
                     "peepoHappy", "peepoSad", "knaDyppaHopeep", "RoxyPotato", "AlienDance", "AYAYA", "BasedGod", "FeelsDankMan", "FeelsOkayMan", "forsenPls",
                     "gachiGASM", "FeelsStrongMan", "EZ", "FeelsWeirdMan", "gachiBASS", "ppL", "(7TV)"]

    url = f"https://emotes.adamcy.pl/v1/channel/{channel}/emotes/all"
    page = requests.get(url)
    emotes = BeautifulSoup(page.content, "html.parser").string
    emotes = ast.literal_eval(emotes)
    if len(emotes) != 0:
        emote = emotes[random.randint(0, len(emotes) - 1)]["code"]
    else:
        emote = random.choice(global_emotes)

    return emote


def debug(task, detail):
    cursor.execute(f"""SELECT * FROM {bot_name}_base WHERE username = '{detail}';""")
    status = cursor.fetchall()
    if len(status) == 0:
        cursor.execute(f"""SELECT * FROM {bot_name}_base WHERE display_name = '{detail}';""")
        status = cursor.fetchall()

    match task:
        case "exist":
            if status:
                return 1
        case "id":
            return status[0][0]
        case "display_name":
            return status[0][2]
        case "emote":
            return status[0][3]

def insert(task, detail):
    match task:
        case "reg": #
            channel = detail[2]

            cursor.execute(f"""INSERT INTO {bot_name}_base (id, username, display_name, emote) VALUES (DEFAULT, '{detail[0]}', '{detail[1]}', '{prefix_emote(channel)}');""")

def update(task, detail):
    match task:
        case "remove_emote":
            print(detail)
            cursor.execute(f"""UPDATE {bot_name}_base SET emote = '{prefix_emote(detail[0])}' WHERE emote = '{detail[1]}';""")