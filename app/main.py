import os
from telegram.ext import Application, CommandHandler
from app.handlers import start_command, help_command, fortune_command, info_command, stats_command
from app.database import init_db
from dotenv import load_dotenv # Импортируем новую библиотеку
from telegram import BotCommand


async def set_bot_commands(application):
    """Устанавливает меню команд для бота"""
    commands = [
        BotCommand("start", "Начать общение"),
        BotCommand("help", "Показать справку"),
        BotCommand("fortune", "Получить предсказание на сегодня"),
        BotCommand("info", "Личные данные"),
        BotCommand("stats", "Статистика предсказаний")
    ]
    await application.bot.set_my_commands(commands)


def main():
    init_db()
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("fortune", fortune_command))
    app.add_handler(CommandHandler("info", info_command))
    app.add_handler(CommandHandler("stats", stats_command))

    # Устанавливаем команды при запуске
    app.post_init = set_bot_commands

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()