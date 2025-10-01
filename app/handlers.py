import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import random
from app.data import FORTUNES
from app.database import *
from telegram import ReplyKeyboardMarkup, KeyboardButton



# Функция-обработчик команды /start 
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start с клавиатурой"""
    # Создаем клавиатуру с кнопками
    keyboard = [
        [KeyboardButton("/fortune")],
        [KeyboardButton("/info"), KeyboardButton("/stats")],
        [KeyboardButton("/help")]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,  # Клавиатура подстраивается под размер экрана
        one_time_keyboard=False  # Клавиатура остается открытой
    )
    
    user = update.message.from_user


    if has_user_got_fortune_today(user.id):
        welcome_text = f"Привет, {user.first_name}! 👋 Я твой бот-предсказатель. \nЯ вижу ты уже получил свое предскозание на сегодня. \nК сожалению предсказание можно получить только один раз в день! \nЗавтра приходи еще 😉"
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup
    )
    
    welcome_text = f"""
    
    Привет, {user.first_name}! 👋 Я твой бот-предсказатель. Напиши мне /fortune, чтобы узнать, что тебя ждет сегодня.
    Так же если хочешь узнать что я умею, напиши мне /help.
    
    """
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup
    )

# Функция-обработчик команды /fortune 
async def fortune_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    # Проверяем, получал ли пользователь предсказание сегодня save_user_fortune
    if has_user_got_fortune_today(user.id):
        await update.message.reply_text("Извини, но предсказание можно получить только один раз в день! Завтра приходи еще 😉")
        return

    # Если не получал - продолжаем
    random_fortune = random.choice(FORTUNES)
    user_id = get_or_create_user(user.id, user.first_name, user.last_name)
    save_user_fortune(user_id, random_fortune, user.first_name) # Сохраняем в историю  

    await update.message.reply_text(f"🔮 Ваше предсказание на сегодня:\n\n*{random_fortune}*", parse_mode='Markdown')

# Функция-обработчик команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    Вот что я умею:
    /start ------ Начать общение.
    /help ------- Показать эту справку.
    /fortune ---- Получить предсказание на сегодня.
    /info ------- Личные данные.
    /stats ------ Статистика.
    """
    await update.message.reply_text(help_text)

# Функция-обработчик команды /info 
async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    # Более надежное форматирование
    info_text = (
        f"*Информация о вас:*\n\n"
        f"• *Имя*: {user.first_name or 'Не указано'}\n"
        f"• *Фамилия*: {user.last_name or 'Не указана'}\n"
        f"• *Username*: @{user.username or 'Не указан'}\n"
        f"• *ID*: `{user.id}`"
    )
    await update.message.reply_text(info_text, parse_mode='Markdown')


# Функция-обработчик команды /stats
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.id

    user_data = get_user_fortunes_count(user_name)

    await update.message.reply_text(str(*user_data))