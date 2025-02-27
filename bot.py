import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor

TOKEN = "7609318887:AAEGDt1PsiF3XjCXi-OtPhNK5a5sC-yJmtE"  # Telegram bot tokeningizni shu yerga yozing
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

players = {}  # O‘yinchilar ro‘yxati
roles = {}  # Rollarni saqlash
game_started = False  # O'yin holati

# Qo‘shimcha rollar (shifokor va hamshira qo‘shildi)
extra_roles = [
    "Doktor", "Медсестра",  # Shifokor va Hamshira
    "Komissar",
    "Zombe", "Meyyasiz odam", "Kamekaze",
    "Sautsed", "Alkash", "Tepsatebranmas"
]


@dp.message_handler(commands=["start"])
async def start_game(message: Message):
    global game_started
    if game_started:
        await message.reply("O‘yin allaqachon boshlangan!")
        return

    players.clear()
    roles.clear()
    game_started = False

    await message.reply("🎭 **Mafiya (Hazil versiya) O‘yiniga xush kelibsiz!**\n\n/join bilan qo‘shiling. O‘yin boshlash uchun /startgame ni bosing.")


@dp.message_handler(commands=["join"])
async def join_game(message: Message):
    if game_started:
        await message.reply("O‘yin allaqachon boshlangan. Keyingi o‘yinga kuting!")
        return

    user_id = message.from_user.id
    if user_id not in players:
        players[user_id] = message.from_user.full_name
        await message.reply(f"✅ {message.from_user.full_name} o‘yinga qo‘shildi!")
    else:
        await message.reply("Siz allaqachon o‘yindasiz!")


@dp.message_handler(commands=["startgame"])
async def start_game_command(message: Message):
    global game_started
    if game_started:
        await message.reply("O‘yin allaqachon boshlangan!")
        return

    if len(players) < 3:
        await message.reply("O‘yin boshlash uchun kamida 3 kishi kerak!")
        return

    game_started = True
    await assign_roles()
    await message.reply("🎭 O‘yin boshlandi! Shaxsiy xabaringizni tekshiring!")


async def assign_roles():
    global roles
    user_ids = list(players.keys())
    random.shuffle(user_ids)

    num_players = len(user_ids)

    # Mafiya soni
    if num_players <= 12:
        num_mafia = 3
    elif num_players <= 19:
        num_mafia = 4
    elif num_players <= 24:
        num_mafia = 5
    else:
        num_mafia = 6

    # Maxfiy rollar soni (Saturn ham shu toifaga kiradi)
    if num_players <= 12:
        num_extra_roles = 2  # **Shifokor va Hamshira har doim bo‘ladi**
    elif num_players <= 19:
        num_extra_roles = 3
    elif num_players <= 24:
        num_extra_roles = 4
    else:
        num_extra_roles = 5

    # Rollarni tayyorlash
    game_roles = ["Mafiya"] * num_mafia + ["Saturn"]  # Saturn har doim bo‘ladi
    selected_extra_roles = random.sample(extra_roles, min(len(extra_roles), num_extra_roles))
    game_roles.extend(selected_extra_roles)

    # Qolganlar fuqaro bo‘ladi
    num_civilians = num_players - len(game_roles)
    game_roles.extend(["Fuqaro"] * num_civilians)

    # Tasodifiy taqsimlash
    assigned_roles = random.sample(game_roles, len(user_ids))

    for uid, role in zip(user_ids, assigned_roles):
        roles[uid] = role
        await bot.send_message(uid, f"🔑 **Sizning rolingiz:** {role}\n\n{get_role_description(role)}")


@dp.message_handler(commands=["role"])
async def check_role(message: Message):
    user_id = message.from_user.id
    if user_id in roles:
        await message.reply(f"🔍 **Sizning rolingiz:** {roles[user_id]}\n\n{get_role_description(roles[user_id])}")
    else:
        await message.reply("Siz o‘yinchi emassiz yoki o‘yin boshlanmagan.")


def get_role_description(role):
    descriptions = {
        "Mafiya": "🕵️ **Mafiya** – Kechasi yashirincha odamlarni o‘ldiradi.",
        "Saturn": "🪐 **Saturn** – Har kuni kimnidir Autogonlega'ga chaqirib, uni o‘ldirishga harakat qiladi!",
        "Doktor": "💉 **Doktor** – Har kecha kimnidir o‘limdan qutqarishi mumkin.",
        "Медсестра": "💊 **Медсестра (Hamshira)** – Shifokorga yordam beradi va u o‘lsa, uning rolini davom ettiradi.",
        "Komissar": "🔍 **Komissar** – Har kecha kimnidir tekshirishi mumkin.",
        "Zombe": "🧟 **Zombe** – O‘lgandan keyin ham yashab qolishi mumkin!",
        "Meyyasiz odam": "🤪 **Meyyasiz odam** – Tasodifiy odamlarni chalg‘itadi.",
        "Kamekaze": "💣 **Kamekaze** – O‘z joniga qasd qilib, bir kishini o‘ldirishi mumkin!",
        "Sautsed": "🍷 **Sautsed** – Kechasi mast bo‘lib, tasodifiy ish qiladi.",
        "Alkash": "🍺 **Alkash** – Kimdir unga hujum qilsa, tirik qoladi!",
        "Tepsatebranmas": "💤 **Tepsatebranmas** – Uni o‘ldirish juda qiyin!"
    }
    return descriptions.get(role, "❓ Noma'lum rol")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
    