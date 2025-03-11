import logging
import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8117149558:AAFCepivZDGfKZXlGV11T-Y_rq-24BkNDU0"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

USER_LEVEL = {}
USER_SCORE = {}
USER_ANSWER = {}
USER_MODE = {}  # "misol" yoki "masala"

MISOLLAR = {
     "1-sinf": [
    ("1 + 1", 2), ("2 + 1", 3), ("3 + 1", 4), ("4 + 2", 6), ("5 + 3", 8),
    ("6 + 4", 10), ("7 + 2", 9), ("8 + 3", 11), ("9 + 1", 10), ("10 + 5", 15),
    ("2 - 1", 1), ("4 - 2", 2), ("6 - 3", 3), ("8 - 4", 4), ("10 - 5", 5),
    ("12 - 6", 6), ("14 - 7", 7), ("16 - 8", 8), ("18 - 9", 9), ("20 - 10", 10)],
    # 980 ta yana shu tartibda davom etadi...
    "2-sinf": [
    ("2 × 2", 4), ("2 × 3", 6), ("2 × 4", 8), ("3 × 3", 9), ("3 × 4", 12),
    ("4 × 4", 16), ("5 × 2", 10), ("5 × 3", 15), ("6 × 2", 12), ("6 × 3", 18),
    ("10 ÷ 2", 5), ("12 ÷ 3", 4), ("15 ÷ 5", 3), ("18 ÷ 6", 3), ("20 ÷ 4", 5),
    ("24 ÷ 6", 4), ("30 ÷ 5", 6), ("36 ÷ 6", 6), ("40 ÷ 8", 5), ("50 ÷ 10", 5)],
    # 980 ta yana shu tartibda davom etadi...
    "3-sinf": [
    ("7 × 6", 42), ("8 × 7", 56), ("9 × 8", 72), ("10 × 9", 90), ("12 × 11", 132),
    ("14 × 12", 168), ("15 × 13", 195), ("16 × 14", 224), ("18 × 15", 270), ("20 × 16", 320),
    ("36 ÷ 6", 6), ("49 ÷ 7", 7), ("64 ÷ 8", 8), ("81 ÷ 9", 9), ("100 ÷ 10", 10),
    ("(3 + 2) × 4", 20), ("(5 + 3) × 6", 48), ("(7 + 2) × 8", 72), ("(9 + 1) × 5", 50), ("(10 + 5) × 2", 30)],
    # 980 ta yana shu tartibda davom etadi...
    "4-sinf": [
    ("25 × 4 + 10", 110), ("30 × 5 + 20", 170), ("40 × 6 + 30", 270), ("50 × 7 + 40", 390), ("60 × 8 + 50", 530),
    ("100 ÷ 5 - 2", 18), ("120 ÷ 6 - 3", 17), ("140 ÷ 7 - 4", 16), ("160 ÷ 8 - 5", 15), ("180 ÷ 9 - 6", 14),
    ("(12 + 8) × 5", 100), ("(15 + 5) × 6", 120), ("(20 + 10) × 7", 210), ("(25 + 15) × 8", 320), ("(30 + 20) × 9", 450)],
    # 980 ta yana shu tartibda davom etadi...
}

MASALALAR = {
     "1-sinf": [
    ("Ali 2 ta olma oldi, Anvar undan 3 taga ko‘p oldi. Anvar nechta olma oldi?", 5),
    ("Dada 5 ta qalam oldi, 2 tasini ukasiga berdi. Dadasida nechta qalam qoldi?", 3),
    ("Sardor 4 ta kitob o‘qidi, Asad undan 2 taga kam o‘qidi. Asad nechta kitob o‘qidi?", 2),
    ("Anvar 6 ta shokolad sotib oldi, 3 tasini ukasiga berdi. Unda nechta qoldi?", 3),
    ("Maktab hovlisida 8 ta daraxt bor, bog‘bon yana 2 ta qo‘shdi. Endi nechta daraxt bor?", 10)],
    # 495 ta yana shu tartibda davom etadi...
    "2-sinf": [
    ("Fermer 4 qatorga 5 tadan kartoshka ekdi. Jami nechta kartoshka ekildi?", 20),
    ("Bir qutida 6 ta olma bor. 3 ta qutida jami nechta olma bor?", 18),
    ("Bir haftada 7 kun bor. 4 haftada jami nechta kun bor?", 28),
    ("Sardor 20 dona konfet oldi va ularni 4 ta do‘stiga teng taqsimladi. Har biriga nechta tegdi?", 5),
    ("O‘quvchilar 30 ta daftarning har biriga 2 tadan rasm chizdilar. Jami nechta rasm chizildi?", 60)],
    # 495 ta yana shu tartibda davom etadi...
    "3-sinf": [
    ("Tomorqada 5 ta qator bor, har bir qatorda 6 tadan pomidor bor. Ularning 10 tasi yig‘ib olindi. Nechta pomidor qoldi?", 20),
    ("Bir sinfda 24 o‘quvchi bor. Ulardan 12 tasi futbol o‘ynaydi, 8 tasi basketbol o‘ynaydi, qolganlari esa shaxmat o‘ynaydi. Nechta o‘quvchi shaxmat o‘ynaydi?", 4),
    ("Anvar 36 ta olma terdi, ukasi undan 12 taga kam terdi. Ikkovining jami olmalar soni nechta?", 60),
    ("Do‘konda 5 quti sut bor edi. Har bir qutida 10 ta sut bor. Agar 15 tasi sotilsa, nechta qoladi?", 35),
    ("O‘qituvchi 45 ta daftar sotib oldi. Har bir o‘quvchiga 3 tadan berdi. Nechta o‘quvchi daftar oldi?", 15)],
    # 495 ta yana shu tartibda davom etadi...
    "4-sinf": [
    ("Bir yuk mashinasi 120 kg yuk olib keldi. Ikkinchisi undan 40 kg ko‘proq yuk olib keldi. Ikkinchi yuk mashinasi nechta yuk olib keldi?", 160),
    ("Bir bog‘chada 5 ta guruh bor, har bir guruhda 15 tadan bola bor. Agar 10 bola kasal bo‘lib kelmasa, bog‘chada nechta bola qoladi?", 65),
    ("Maktab kutubxonasida 240 ta kitob bor edi. Ulardan 60 tasi yangilar bilan almashtirildi. Endi nechta eski kitob qoldi?", 180),
    ("Bir hafta davomida magazinda har kuni 12 ta non sotildi. Agar shanba va yakshanba kunlari 20 tadan sotilgan bo‘lsa, jami nechta non sotilgan?", 104),
    ("Bir uyda 6 xonada har birida 4 tadan oyna bor. Agar 5 tasi sinib yangisiga almashtirilsa, jami nechta oyna bor?", 24)]
    # 495 ta yana shu tartibda davom etadi...
}

menu_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
menu_buttons.row(KeyboardButton("📝 Matematik misol yechish"), KeyboardButton("📖 Masala yechish"))
menu_buttons.row(KeyboardButton("📊 Darajani o‘zgartirish"), KeyboardButton("🏆 Reyting"))
menu_buttons.row(KeyboardButton("⬅️ Ortga"))

def create_answer_buttons(correct_answer):
    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    answers = [correct_answer, correct_answer + random.randint(1, 3), correct_answer - random.randint(1, 3)]
    random.shuffle(answers)
    for ans in answers:
        buttons.add(KeyboardButton(str(ans)))
    buttons.row(KeyboardButton("🔄 Keyingi misol"), KeyboardButton("🔄 Keyingi masala"), KeyboardButton("⬅️ Ortga"))
    return buttons

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    USER_LEVEL[message.from_user.id] = "1-sinf"
    USER_SCORE[message.from_user.id] = 0
    await message.reply("🤖 Xush kelibsiz! Matematik misollar va masalalarni yechishingiz mumkin.", reply_markup=menu_buttons)

@dp.message_handler(lambda message: message.text in ["📝 Matematik misol yechish", "🔄 Keyingi misol"])
async def send_math_problem(message: types.Message):
    level = USER_LEVEL.get(message.from_user.id, "1-sinf")
    USER_MODE[message.from_user.id] = "misol"
    misol, javob = random.choice(MISOLLAR[level])
    USER_ANSWER[message.from_user.id] = javob
    await message.reply(f"📌 Misol: {misol}\n✍️ To‘g‘ri javobni tanlang:", reply_markup=create_answer_buttons(javob))

@dp.message_handler(lambda message: message.text in ["📖 Masala yechish", "🔄 Keyingi masala"])
async def send_masala(message: types.Message):
    level = USER_LEVEL.get(message.from_user.id, "1-sinf")
    USER_MODE[message.from_user.id] = "masala"
    masala, javob = random.choice(MASALALAR[level])
    USER_ANSWER[message.from_user.id] = javob
    await message.reply(f"📖 Masala: {masala}\n✍️ To‘g‘ri javobni tanlang:", reply_markup=create_answer_buttons(javob))

@dp.message_handler(lambda message: message.text.isdigit())
async def check_answer(message: types.Message):
    user_answer = int(message.text)
    user_id = message.from_user.id
    correct_answer = USER_ANSWER.get(user_id)

    if correct_answer is not None:
        if user_answer == correct_answer:
            USER_SCORE[user_id] = USER_SCORE.get(user_id, 0) + 5
            response_text = f"✅ To‘g‘ri! 🎉 +5 ball\n🏅 Joriy ball: {USER_SCORE[user_id]}"
        else:
            USER_SCORE[user_id] = USER_SCORE.get(user_id, 0) - 2
            response_text = f"❌ Xato! To‘g‘ri javob: {correct_answer}\n🏅 Joriy ball: {USER_SCORE[user_id]}"

        await message.reply(response_text)

        USER_ANSWER[user_id] = None

        if USER_MODE.get(user_id) == "misol":
            await send_math_problem(message)
        elif USER_MODE.get(user_id) == "masala":
            await send_masala(message)
        else:
            await message.reply("❗ Avval misol yoki masala tanlang!", reply_markup=menu_buttons)
    else:
        await message.reply("⚠️ Avval misol yoki masala tanlang!", reply_markup=menu_buttons)

@dp.message_handler(lambda message: message.text == "📊 Darajani o‘zgartirish")
async def change_level(message: types.Message):
    level_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    for level in MISOLLAR.keys():
        level_buttons.add(KeyboardButton(level))
    level_buttons.row(KeyboardButton("⬅️ Ortga"))
    await message.reply("📚 Darajani tanlang:", reply_markup=level_buttons)

@dp.message_handler(lambda message: message.text in MISOLLAR.keys())
async def set_level(message: types.Message):
    USER_LEVEL[message.from_user.id] = message.text
    await message.reply(f"✅ Darajangiz o‘zgartirildi: {message.text}", reply_markup=menu_buttons)

@dp.message_handler(lambda message: message.text == "🏆 Reyting")
async def show_score(message: types.Message):
    score = USER_SCORE.get(message.from_user.id, 0)
    await message.reply(f"🏅 Sizning joriy reytingingiz: {score} ball.", reply_markup=menu_buttons)

@dp.message_handler(lambda message: message.text == "⬅️ Ortga")
async def go_back(message: types.Message):
    await message.reply("🔙 Asosiy menyuga qaytdingiz.", reply_markup=menu_buttons)

async def main():
    await dp.start_polling()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())