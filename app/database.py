import sqlite3
import os
from datetime import datetime

# Путь к файлу базы данных. has_user_got_fortune_today
# 'data' - это папка на уровне выше, поэтому используем os.path.join для корректного пути
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'fortunes.db')

# Функция для создания соединения с БД
def get_db_connection():
    # Создаем папку 'data', если ее нет
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    # Этот параметр позволяет получать данные в виде словаря по имени столбца
    conn.row_factory = sqlite3.Row
    return conn

# Функция для инициализации структуры БД (создания таблиц)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Таблица пользователей user_id
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        telegram_id INTEGER UNIQUE NOT NULL,
        first_name TEXT,
        username TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Таблица предсказаний пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_fortunes (
        telegram_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        fortune_text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (telegram_id) REFERENCES users (id) 
    )
    ''')

    conn.commit()
    conn.close()
    print("База данных инициализирована")

# Функция для добавления или получения существующего пользователя
def get_or_create_user(telegram_id, first_name, username):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Пытаемся найти пользователя
    cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
    user = cursor.fetchone()

    # Если не нашли, создаем нового
    if user is None:
        cursor.execute(
            'INSERT INTO users (telegram_id, first_name, username) VALUES (?, ?, ?)',
            (telegram_id, first_name, username)
        )
        conn.commit()
        # Получаем ID только что вставленной записи
        new_user_id = cursor.lastrowid
        conn.close()
        return new_user_id
    else:
        # Если пользователь найден, возвращаем id
        conn.close()
        return user['telegram_id']

# Функция для сохранения выданного предсказания в историю
def save_user_fortune(telegram_id, fortune_text, username): 
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO user_fortunes (telegram_id, fortune_text, username ) VALUES (?, ?, ?)',
        (telegram_id, fortune_text, username)
    )
    conn.commit()
    conn.close()

# Функция для проверки, получал ли пользователь предсказание сегодня
def has_user_got_fortune_today(telegram_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL-запрос, который ищет предсказания для пользователя за сегодня
    query = '''
    SELECT fortune_text FROM user_fortunes 
    WHERE telegram_id = ? 
    AND DATE(created_at) = DATE('now') 
    LIMIT 1
    '''
    cursor.execute(query, (telegram_id,))
    fortune_today = cursor.fetchone()
    conn.close()

    # Если найдена хотя бы одна запись - возвращаем True
    return fortune_today is not None

# Функция для создания словаря по { дате : предсазанию } пользователя за все время. 
def get_user_fortunes_count(telegram_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = '''
    SELECT created_at, fortune_text FROM user_fortunes
    WHERE telegram_id = ?
    ORDER BY created_at DESC
    '''

    cursor.execute(query, (telegram_id,))
    fortunes = cursor.fetchall()  # ← получаем ВСЕ записи
    conn.close()

    # Форматируем каждую запись
    return [f"\n{row[0]} - {row[1]}" for row in fortunes]  # ← по индексам