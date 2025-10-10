import os
from telegram.ext import Application, CommandHandler
from app.handlers import start_command, help_command, fortune_command, info_command, stats_command
from app.admin import admin
from app.database import init_db
from dotenv import load_dotenv 
from telegram import BotCommand
import asyncio

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

async def set_bot_commands(application):
    """Устанавливает меню команд для бота"""
    commands = [
        BotCommand('start', "🚀 Начать общение"),
        BotCommand('fortune', "🔮 Получить предсказание"),
        BotCommand('info', "👤 Личные данные"),
        BotCommand('stats', "📊 Статистика"),
        BotCommand('admin', "👨🏻‍💻 Админка")
    ]
    await application.bot.set_my_commands(commands)

def main():
    # Инициализация базы данных
    init_db()
    
    # Создание приложения
    app = Application.builder().token(BOT_TOKEN).post_init(set_bot_commands).build()

    # Добавление обработчиков команд
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("fortune", fortune_command))
    app.add_handler(CommandHandler("info", info_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("admin", admin))
    #app.add_handler(CommandHandler("help", help_command))
    

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()