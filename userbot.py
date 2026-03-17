from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.errors import FloodWait, RPCError, BadRequest
from pyrogram.enums import ChatAction
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
from datetime import date
import time
import random
import threading

font_user = ImageFont.truetype("font/Sjz.ttf", 50)
font_text = ImageFont.truetype("font/Sjz.ttf", 65)
font_id = ImageFont.truetype("font/Sjz.ttf", 40)

name = "ждун ᴢᴀʟᴏᴋs.ʜᴛᴍʟ | #ɢɴᴢs #ждуᴧᴇᴛо"
bio = "𝙵𝟺𝙲𝙺 𝚉𝟺𝚕𝟶𝙺𝚂 | #ждулето"
avatar = "avatar.png"

troll_active = {}
typing_active = {}

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
string_session = os.getenv("STRING_SESSION")

app = Client("session", api_id=API_ID, api_hash=API_HASH, session_string=string_session)

@app.on_message(filters.me & filters.command("help", prefixes='.'))
def help(client, message):
    message.edit_text(
        """
Команды userbot:

<code>.help</code> — список команд
<code>.ping</code> — проверить скорость 
<code>.info</code> — показать информацию о пользователе

<code>.anim</code> — анимация текста 
<code>.user</code> — найти информацию по юзу 
<code>.copy</code> — копировать профиль 

<code>.back</code> — вернуть профиль
<code>.prof</code> — изменить что-то в профиле 
<code>.q</code> — сделать цитату текста фотографией

<code>.troll(1,2,3)</code> — тролл текстом 
<code>.dox</code> — доксинг 
<code>.spam</code> — спам сообщениями 

<code>.addbul</code> — троллинг ответом на каждое сообщение пользователя
<code>.fake</code> — фейк сообщение фотографией
<code>.summer</code> — сколько дней осталось до ЛЕТА

<code>.typing</code> — включение бесконечного тайпинга
<code>.stoptyping</code> — выключение бесконечного тайпинга 
""", parse_mode=enums.ParseMode.HTML)

# --------- TYPING ---------

def typing_loop(client, chat_id):

    while typing_active.get(chat_id):
        client.send_action(chat_id, "typing")
        time.sleep(10)
        
@app.on_message(filters.me & filters.command("typing", prefixes='.'))
def typing_start(client, message):

    chat_id = message.chat.id

    typing_active[chat_id] = True

    threading.Thread(target=typing_loop, args=(client, message)).start()

    message.edit("Бесконечный тайпинг включен")

@app.on_message(filters.me & filters.command("stoptypinf", prefixes='.'))
def stop_typ(client, message):
    chat_id = message.chat.id

    typing_active[chat_id] = False

    message.edit("Бесконечный тайпинг выключен")

# --------------------------------------------

# --------- SUMMER ---------

@app.on_message(filters.me & filters.command("summer", prefixes='.'))
def check_summer(client, message):

    today = date.today()

    start_summer = date(today.year, 6, 1)

    if today > start_summer:
        start_summer = date(today.year + 1, 6, 1)

        message.edit(f"Лето уже прошло, до следующего лета осталось: {start_summer} дней")
    
    delta = start_summer - today

    if delta == 0:
        message.edit("Поздравляю с наступлением лета!")
    else:
        message.edit(f"До лета осталось: {delta.days} дней")

# --------- --------- ---------

# --------- ПИНГ --------- 

@app.on_message(filters.me & filters.command("ping", prefixes='.'))
def ping(client, message):

    start = time.time()
    message.edit("Считаю...")
    end = time.time()

    result = round((end - start) * 1000)

    message.edit_text(
        f"<b>🏓 ПОНГ! Комнанда сработала за: {result} мс</b>",
        parse_mode=enums.ParseMode.HTML
    )

# --------- --------- ---------

# --------- INFO ---------

@app.on_message(filters.me & filters.command("info", prefixes='.'))
def info(client, message):


    if message.reply_to_message:
        user = message.reply_to_message.from_user
    if not message.reply_to_message:
        user = message.from_user

    user_full = client.get_users(user.id)
    chat = client.get_chat(user.id)

    id = user_full.id
    name = user_full.first_name
    username = f"@{user_full.username}" if user_full.username else "Нету"
    bio = chat.bio or "Нету"

    bot = "✔ Бот" if user_full.is_bot else "❌ Не бот"

    message.edit(
        f"""
👤 Информация о пользователе:
                 
ID: <code>{id}</code>
NAME: <code>{name}</code>
USERNAME: {username}
BIO: <code>{bio}</code>
BOT: <code>{bot}</code>

CHAT: <code>{message.chat.id}</code>
""",
        parse_mode=enums.ParseMode.HTML
    )
    
# --------- --------- ---------

# --------- USER ---------

@app.on_message(filters.me & filters.command("user", prefixes='.'))
def info(client, message):

    args = message.text.split( maxsplit=1)

    if len(args) < 2:
        message.edit("Используй .user @username")
        return
    target = args[1].strip()
    try:
        if target.startswith("@"):
            user = client.get_users(target)
        elif target.isdigit:
            user = client.get_users(int(target))

        message.edit(f"""

🔍 ПОИСК ПО USERNAME:

USERNAME: {f"@{user.username}" if user.username else "Нету"}
NAME: <code>{user.first_name}</code>
ID: <code>{user.id}</code>

""", parse_mode=enums.ParseMode.HTML)

    except (RPCError, IndexError, ValueError):
        message.edit("Ничего не найдено")
    
# --------- --------- ---------

# --------- ANIM ---------

@app.on_message(filters.me & filters.command("anim", prefixes='.'))
def anim1(client, message):
    parts = message.text.split(maxsplit=2)
    orig_text = parts[2] if len(parts) > 1 else ""

    if not orig_text:
        message.edit("Используй: .anim <время> текст")
        return
    
    delay = float(parts[1])
    
    tbp = ""
    symbol = "|"

    for ch in orig_text:
        try:
            message.edit(tbp + symbol)
            time.sleep(delay)
            tbp += ch
            message.edit(tbp)
            time.sleep(delay)

        except FloodWait as e:
            time.sleep(e.value)

# --------- --------- ---------

# --------- DOX ---------

@app.on_message(filters.me & filters.command("dox", prefixes='.'))
def dox(client, message):
    if message.reply_to_message:
        for i in range(0, 90, 10):
            try:
                message.edit(f"Начинаю искать пользователя {i}%...")
                time.sleep(0.02)
            except FloodWait as e:
                time.sleep(e.value)

        for i in range(90, 101, 1):
            try:
                message.edit(f"Начинаю искать пользователя {i}%...")
                time.sleep(0.02)
            except FloodWait as e:
                time.sleep(e.value)

        for i in range(0, 101, 50):
            try:
                message.edit(f"Пользователь найден! Начинаю искать ФИО {i}%...")
                time.sleep(0.1)
            except FloodWait as e:
                time.sleep(e.value)
        
        for i in range(0, 101, 25):
            try:
                message.edit(f"ФИО найдено! Начинаю искать адресс {i}%...")
                time.sleep(0.07)
            except FloodWait as e:
                time.sleep(e.value)
        
        for i in range(0, 101, 20):
            try: 
                message.edit(f"Адресс найден! Начинаю собирать информация воедино {i}%...")
                time.sleep(0.05)
            except FloodWait as e:
                time.sleep(e.value)
        

        message.edit("""
<b>ВСЯ ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ:</b>
                     
<i>ФИО: в паспорте
ВОЗРАСТ: дата твоего рождения
ТЕЛЕФОН: +7 дальше сам
АДРЕС: где-то за Земле
ИНН: в госуслугах

МАМА: сам знаешь
ПАПА: сам знаешь
                     
ТГ: запрещен
ВК: если есть то знаешь сам
ПОЧТА: посмотри в гугле</i>

""", parse_mode=enums.ParseMode.HTML)

    else:
        message.edit("Используй ответом на пользователя")

# --------- --------- ---------

# --------- SPAM ---------

@app.on_message(filters.me & filters.command("spam", prefixes='.'))
def spam(client, message):

    args = message.text.split(maxsplit=2)

    if len(args) > 3:
        message.edit("Используй: .spam <число> <текст>")
        return

    if not args[1].isdigit():
        message.edit("Неверно указано число сообщений")
        return
    
    count = int(args[1])
    text = args[2]

    message.delete()

    for _ in range(count):
        try:
            client.send_message(message.chat.id, text)
            time.sleep(0.04)
        except FloodWait as e:
            time.sleep(e.value)

# --------- --------- ---------

# --------- PROFILE ---------

@app.on_message(filters.me & filters.command("prof", prefixes='.'))
def upd_prof(client, message):

    args = message.text.split(maxsplit=2)

    if len(args) < 3:
        message.edit("Используй: .prof name|user|bio text")
        return
    
    field = args[1].lower()
    value = args[2].strip()

    try:
        if field == "name":
            client.update_profile(first_name=value)
            message.edit(f"Имя изменено на: <code>{value}</code>", parse_mode=enums.ParseMode.HTML)
            return
        elif field == "user":
            username = value.lstrip("@")
            client.set_username(username)
            message.edit(f"Юзернейм изменен на: @{username}")
            return
        elif field == "bio":
            client.update_profile(bio=value)
            message.edit(f"Био изменено на: <code>{value}</code>", parse_mode=enums.ParseMode.HTML)
            return
        else:
            message.edit("Неизвестный параметр")
            return
    except RPCError as e:
        message.edit(f"Ошибка: {e}")

# --------- TROLL ---------

@app.on_message(filters.me & filters.command("troll1", prefixes='.'))
def troll(client, message):
    args = message.text.split(maxsplit=1)

    delay = float(args[1]) if len(args) > 1 else 0.3

    try:
        with open("TROLL/Troll.txt", 'r', encoding='utf-8') as file:
            text = file.read().strip()
    except:
        message.edit("Файл для троллинга не найден")
        return
    
    words = text.split()

    if not words:
        message.edit("Файл пустой")
        return
    
    troll_active[message.chat.id] = True
    message.delete()

    for w in words:
        if not troll_active.get(message.chat.id, False):
            break
        try:
            client.send_message(message.chat.id, w)
            time.sleep(delay)
        except FloodWait as e:
            time.sleep(e.value)
    
    troll_active[message.chat.id] = False

@app.on_message(filters.me & filters.command("troll2", prefixes='.'))
def troll(client, message):
    args = message.text.split(maxsplit=2)

    delay = float(args[1]) if len(args) > 1 else 0.3

    try:
        with open("TROLL/Troll2.txt", "r", encoding="utf-8") as file:
            text = file.read().strip()
    except:
        message.edit("Файл для троллинга не найден")
        return
    
    words = text.split()

    if not words:
        message.edit("Файл пустой")
        return
    
    troll_active[message.chat.id] = True
    message.delete()

    for w in words:
        if not troll_active.get(message.chat.id, False):
            break
        try:
            client.send_message(message.chat.id, w)
            time.sleep(delay)
        except FloodWait as e:
            time.sleep(e.value)

@app.on_message(filters.me & filters.command("troll3", prefixes="."))
def troll(client, message):

    args = message.text.split(maxsplit=2)

    delay = float(args[1]) if len(args) > 1 else 0.3

    try:
        with open("TROLL/Troll3.txt", "r", encoding="utf-8") as file:
            text = file.read().strip()
    except:
        message.edit("Файл для троллинга не найден")
        return
    
    words = text.split()

    if not words:
        message.edit("Файл пустой")
        return
    
    troll_active[message.chat.id] = True
    message.delete()

    for w in words:
        if not troll_active.get(message.chat.id, False):
            break
        try:
            client.send_message(message.chat.id, w)
            time.sleep(delay)
        except FloodWait as e:
            time.sleep(e.value)


@app.on_message(filters.me & filters.command("stop", prefixes='.'))
def stop_troll(client, message):
    troll_active[message.chat.id] = False
    message.edit("Троллинг завершен")

# --------- --------- --------

# --------- COPY PROFILE ---------

@app.on_message(filters.me & filters.command("copy", prefixes="."))
def copy(client, message):

    if not message.reply_to_message or not message.reply_to_message.from_user:
        message.edit("Используй ответив на сообщение")
        return
    
    target = message.reply_to_message.from_user

    try:
        user = client.get_users(target.id)
        chat = client.get_chat(target.id)

        client.update_profile(
            first_name = user.first_name,
            bio = chat.bio or ""
        )

        message.edit("Имя и био скопированы")

        avatar = list(client.get_chat_photos(target.id, limit=1))
        if avatar:
            file_path = client.download_media(avatar[0].file_id)
            client.set_profile_photo(photo=file_path)
        
        target_name = f"@{target.username}" if target.username else target.first_name
        message.edit(
            f"Профиль <code>{target_name}</code> успешно скопиован",
            parse_mode=enums.ParseMode.HTML
        )

    except RPCError as e:
        message.edit(f"Ошибка: {e}")

# --------- --------- ---------

# --------- BACK PROFILE ---------

@app.on_message(filters.me & filters.command("back", prefixes="."))
def back(client, message):

    client.update_profile(
        first_name = name,
        bio = bio
    )

    message.edit("Имя и био восставновлены")

    ava = list(client.get_chat_photos("me", limit=1))
    if ava:
        client.delete_profile_photos([p.file_id for p in ava])
        return

    client.set_profile_photo(photo=avatar)

    message.delete()

# --------- --------- ---------

# --------- FAKE ---------

@app.on_message(filters.me & filters.command("fake", prefixes='.'))
def fake(client, message):

    if not message.reply_to_message:
        message.edit("Используй ответив на сообщение пользователя")
        return


    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        message.edit("Используй: .fake text")
        return

    # Текст после команды приводим к одной строке.
    fake_text = " ".join(parts[1].split())
    target = message.reply_to_message
    user = target.from_user

    wrap_text = textwrap.fill(fake_text, width=50)

    avatar_path = None
    avatar = list(client.get_chat_photos(user.id, limit=1))
    if avatar:
        avatar_path = client.download_media(avatar[0].file_id, file_name = "fake_user_avatar.jpeg")
    else:
        avatar_path = "image.png"
    
    raw_img = Image.open(avatar_path).convert("RGBA")
    bg = raw_img.resize((1280, 720))
    bg = bg.filter(ImageFilter.BoxBlur(radius=15))
    bg = bg.convert("RGBA")

    overlay = Image.new("RGBA", bg.size, (0, 0, 0, 160))
    bg = Image.alpha_composite(bg, overlay)

    draw = ImageDraw.Draw(bg)
    draw.text((640, 50), f"{user.username or user.first_name}", font=font_user, anchor="mm", fill="white")
    draw.text((640, 360), wrap_text, font=font_text, anchor="mm", fill="white")
    draw.text((640, 670), f"ID: {user.id}", font=font_id, anchor="mm", fill="white")

    final_buffer = BytesIO()
    bg.convert("RGB").save(final_buffer, "JPEG", quality=85)
    final_buffer.seek(0)
    final_buffer.name = "fake_quote.jpg"

    try:
        client.send_photo(message.chat.id, photo=final_buffer)
        message.delete()
    except BadRequest as e:
        if "TOPIC_CLOSED" in str(e):
            message.edit("Топик закрыт. Недоступно")
        else:
            raise

    if avatar_path != "image.png":
        os.remove(avatar_path)

# --------- --------- ---------

# --------- QUOTE ---------

@app.on_message(filters.me & filters.command("q", prefixes='.'))
def q_cmd(client, message):

    if not message.reply_to_message:
        message.edit("Ответь на сообщение пользователя")

    target = message.reply_to_message
    user = target.from_user
    text = textwrap.fill(target.text, width=50)

    avatar_path = None

    avatar = list(client.get_chat_photos(user.id, limit=1))
    if avatar:
        avatar_path = client.download_media(avatar[0].file_id, file_name="user_avatar.jpeg")

    else:
        avatar_path = "image.png"

    raw_img = Image.open(avatar_path).convert("RGBA")

    bg = raw_img.resize((1280, 720))
    bg = bg.filter(ImageFilter.BoxBlur(radius=15))
    bg = bg.convert("RGBA")

    overlay = Image.new("RGBA", bg.size, (0, 0, 0, 160))

    bg = Image.alpha_composite(bg, overlay)

    draw = ImageDraw.Draw(bg)

    draw.text((640, 50), f"{user.username or user.first_name}", font=font_user, anchor="mm", fill="white")
    draw.text((645, 360), text, font=font_text, anchor="mm", fill="white")
    draw.text((640, 670), f"ID: {user.id}", font=font_id, anchor="mm", fill="white")

    final_buffer = BytesIO()
    bg.convert("RGB").save(final_buffer, "JPEG", quality=85)
    final_buffer.seek(0)
    final_buffer.name = "quote.jpeg"

    client.send_photo(message.chat.id, photo=final_buffer)

    message.delete()
    
    if avatar_path != "image.png":
        os.remove(avatar_path)

# --------- --------- ---------

# --------- ADDBUL ---------

def load_users():
    with open("BUL/users_bul.txt", "r", encoding="utf-8") as file:
        return set(str(line.strip()) for line in file)
    
auto_users = load_users()

def save_users(user_id):

    with open("BUL/users_bul.txt", "a+", encoding="utf-8") as file:
        file.write(str(user_id) + "\n")

@app.on_message(filters.me & filters.command("addbul", prefixes='.'))
def addbul(client, message):

    if message.reply_to_message.from_user.id == 1891318329:
        message.edit("Ты не можешь троллить самого себя")
        return
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id

        if user_id not in auto_users:
            auto_users.add(user_id)
            save_users(user_id)
            message.edit("Пользователь добавлен")
            return

        if user_id in auto_users:
            message.edit("Пользователь уже добавлен")
            return

@app.on_message(filters.me & filters.command("stopbul", prefixes='.'))
def stopbul(client, message):

    if not message.reply_to_message:
        message.edit("Ответь на сообщение пользователя")

    user_id = message.reply_to_message.from_user.id

    if user_id in auto_users:
        auto_users.remove(user_id)

        with open("BUL/users_bul.txt", "w", encoding='utf-8') as file:
            for uid in auto_users:
                file.write(str(uid) + "\n")

        message.edit("Пользователь удален")
    
    else:
        message.edit("Пользователь уже удален или не найден")

@app.on_message(filters.text)
def auto(cient, message):

    with open("BUL/phrases.txt", "r", encoding='utf-8') as f:
        phrases = [line.strip() for line in f if line.strip()]

    if message.from_user.id in auto_users:
        phrases = random.choice(phrases)

        message.reply_text(phrases)

# --------- --------- ---------


print("ZALOKS USERBOT START")

app.run()
