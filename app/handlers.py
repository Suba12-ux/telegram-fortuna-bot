import os, asyncio, json, random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from app.data import FORTUNES_Giga
from app.database import *
from telegram import ReplyKeyboardMarkup, KeyboardButton


# Функция-обработчик команды /start 
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #reply_markup = get_main_keyboard()  # Уже получаем готовую клавиатуру 
    user = update.message.from_user

    if has_user_got_fortune_today(user.id):
        welcome_text = f"Привет, {user.first_name}! 👋 Я твой бот-предсказатель.\nЯ вижу ты уже получил свое предсказание на сегодня.\nК сожалению предсказание можно получить только один раз в день!\nЗавтра приходи еще 😉"
        await update.message.reply_text(welcome_text) # reply_markup=reply_markup
    else:
        welcome_text = f"""Привет, {user.first_name}! 👋 Я твой бот-предсказатель. Нажми кнопку ниже или напиши /fortune, чтобы узнать, что тебя ждет сегодня."""
        await update.message.reply_text(welcome_text ) # reply_markup=reply_markup

# Функция-обработчик команды /fortune 
async def fortune_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    #reply_markup = get_main_keyboard()

    # Проверяем, получал ли пользователь предсказание сегодня save_user_fortune
    if has_user_got_fortune_today(user.id):
        await update.message.reply_text("Извини, но предсказание можно получить только один раз в день! Завтра приходи еще 😉" ) # reply_markup=reply_markup
        return

    # Если не получал - продолжаем
    await update.message.reply_text(f"🔮 Заглядываем в будущее, пожалуйста подождите...")
     
    random_fortune1 = FORTUNES_Giga(user.first_name)
    if random_fortune1 is None:
        await update.message.reply_text(f"🔮 Простите сегодян магнитные бури, пердсказание сломалось.")
    
    user_id = get_or_create_user(user.id, user.first_name, user.last_name, user.username)
    save_user_fortune(user_id, random_fortune1, user.first_name)

    await update.message.reply_text(
        f"🔮 Ваше предсказание на сегодня:\n\n*{random_fortune1}*"
    )

# Функция-обработчик команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #reply_markup = get_main_keyboard()
    help_text = """
    Вот что я умею:
    /start ------ Начать общение.
    /help ------- Показать эту справку.
    /fortune ---- Получить предсказание на сегодня.
    /info ------- Личные данные.
    /stats ------ Статистика.
    """
    await update.message.reply_text(help_text) # reply_markup=reply_markup

# Функция-обработчик команды /info 
async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    #reply_markup = get_main_keyboard()
    
    info_text = (
        f"*Информация о вас:*\n\n"
        f"• *Имя*: {user.first_name or 'Не указано'}\n"
        f"• *Фамилия*: {user.last_name or 'Не указана'}\n"
        f"• *Username*: @{user.username or 'Не указан'}\n"
        f"• *ID*: `{user.id}`"
    )
    await update.message.reply_text(info_text)

# Функция-обработчик команды /stats
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #reply_markup = get_main_keyboard()
    user_id = update.message.from_user.id

    user_data = get_user_fortunes_count(user_id)
    # Предполагая, что user_data возвращает (count,)
    stats_text = f"📊 *Ваша статистика:*\n\n• Получено предсказаний: {user_data[0] if user_data else 0}"
    
    await update.message.reply_text(stats_text)
