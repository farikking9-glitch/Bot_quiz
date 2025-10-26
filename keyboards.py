from pyrogram.types import ReplyKeyboardMarkup
import buttons

# === Главное меню ===
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [buttons.start_quiz_button],
        [buttons.score_button, buttons.rating_button],
        [buttons.settings_button, buttons.help_button]
    ],
    resize_keyboard=True
)

# === Меню настроек ===
settings_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [buttons.help_button],
        [buttons.start_quiz_button],
        [buttons.score_button, buttons.rating_button]
    ],
    resize_keyboard=True
)
