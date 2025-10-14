import os, random, asyncio
from telegram.ext import Application, CommandHandler, ContextTypes
from app.handlers import start_command, help_command, fortune_command, info_command, stats_command
from app.database import init_db
from dotenv import load_dotenv 
from telegram import BotCommand, Update
from app.database import *
from telegram import ReplyKeyboardMarkup, KeyboardButton
#if user.id == 883502267 or user.first_name == 'Субхон' and user.last_name == 'Эмомов' and user.username == '@SEmomov':

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    
    # Улучшенная проверка админа
    load_dotenv()
    admin_user_info = os.getenv('admin_user_info') #  список данных админов 

    if str(user.id) in admin_user_info or user.first_name in admin_user_info and user.last_name in admin_user_info and user.username in admin_user_info:
        try:
            user_data = add_all_info()
            
            if not user_data or (not user_data.get('users') and not user_data.get('fortunes')):
                await update.message.reply_text("📊 Нет данных для отображения")
                return
            
            # Форматируем пользователей
            users_text = "👥 Пользователи:\n"
            if user_data.get('users'):
                for i, user_row in enumerate(user_data['users'], 1): 
                    users_text += f"{i}. {str(user_row)}\n"
            else:
                users_text += "Нет пользователей\n"
            
            # Форматируем предсказания
            #fortunes_text = "🔮 Предсказания:\n"
            #if user_data.get('fortunes'):
            #    for i, fortune in enumerate(user_data['fortunes'], 1):
            #        fortunes_text += f"{i}. {str(fortune)}\n"
            #else:
            #    fortunes_text += "Нет предсказаний\n"
            
            # Отправляем
            await update.message.reply_text(users_text)
            #await update.message.reply_text(fortunes_text)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка: {e}")
    else: 
        await update.message.reply_text('🚫 В ДОСТУПЕ ОТКАЗАНО!')