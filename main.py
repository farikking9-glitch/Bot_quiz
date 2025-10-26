from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

import buttons
from custom_filters import button_filter
from database import init_db, add_user, add_score, get_user_score, get_rating
from keyboards import main_keyboard, settings_keyboard
from quiz import get_question
from http_client import HttpClient
import config

# === Инициализация ===
bot = Client("quiz_bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)
http_client = HttpClient()
init_db()

# === /start ===
@bot.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    add_user(message.from_user.id, message.from_user.first_name)

    text = (
        "👋 Привет! Это бот-викторина.\n\n"
        "Используй меню ниже, чтобы начать игру!"
    )

    await message.reply(text, reply_markup=main_keyboard)  # main_keyboard теперь ReplyKeyboardMarkup

# === Викторина ===
@bot.on_message(filters.command("quiz") | button_filter(buttons.start_quiz_button))
async def quiz_handler(client, message: Message):
    q = get_question()
    options_text = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(q["options"])])
    await message.reply(f"{q['question']}\n\n{options_text}\n\nОтветь номером правильного ответа!")

    # Сохраняем правильный ответ для проверки
    bot.correct_answer = q["answer"]

# === Проверка ответа ===
@bot.on_message(filters.regex(r"^[1-4]$"))
async def answer_handler(client, message: Message):
    if not hasattr(bot, "correct_answer"):
        return await message.reply("Сначала начни викторину кнопкой 'Начать викторину'", reply_markup=main_keyboard)

    index = int(message.text) - 1
    q_options = get_question()["options"]
    chosen_answer = q_options[index]
    correct_answer = bot.correct_answer

    if chosen_answer == correct_answer:
        add_score(message.from_user.id, 1)
        await message.reply("✅ Верно! +1 очко", reply_markup=main_keyboard)
    else:
        await message.reply(f"❌ Неверно! Правильный ответ: {correct_answer}", reply_markup=main_keyboard)

    del bot.correct_answer

# === Счёт ===
@bot.on_message(filters.command("score") | button_filter(buttons.score_button))
async def score_handler(client, message: Message):
    score = get_user_score(message.from_user.id)
    await message.reply(f"🏆 У тебя {score} очков", reply_markup=main_keyboard)

# === Рейтинг ===
@bot.on_message(filters.command("rating") | button_filter(buttons.rating_button))
async def rating_handler(client, message: Message):
    data = get_rating()
    if not data:
        return await message.reply("😅 Пока нет игроков", reply_markup=main_keyboard)

    text = "🏅 *Топ игроков:*\n\n"
    for i, (name, score) in enumerate(data, start=1):
        text += f"{i}. {name} — {score} очков\n"
    await message.reply(text, reply_markup=main_keyboard)

# === Настройки / помощь ===
@bot.on_message(filters.command(["settings", "help"]) | button_filter(buttons.settings_button) | button_filter(buttons.help_button))
async def settings_command(client, message: Message):
    text = "⚙️ Здесь настройки.\n\nТы можешь изменить ник или посмотреть статистику."
    await message.reply(text, reply_markup=settings_keyboard)

@bot.on_message()
async def unknown_message(client: Client, message: Message):
    await message.reply("Неизвестная команда")
# === Запуск ===
print("✅ Бот запущен и ждёт команды...")
bot.run()
