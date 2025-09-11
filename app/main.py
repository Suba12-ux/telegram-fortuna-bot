import os
from telegram.ext import Application, CommandHandler
from app.handlers import start_command, help_command, fortune_command, info_command, stats_command
from app.database import init_db
from dotenv import load_dotenv # Импортируем новую библиотеку

# Загружаем переменные из файла .env
load_dotenv()

# Получаем токен из переменной окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("Ошибка: Не задана переменная окружения BOT_TOKEN")

def main():
    init_db()
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("fortune", fortune_command))
    app.add_handler(CommandHandler("info", info_command))
    app.add_handler(CommandHandler("stats", stats_command))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()