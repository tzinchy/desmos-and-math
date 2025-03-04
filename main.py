# app.py
import streamlit as st
import sqlite3
import plotly.express as px
import pandas as pd
import random
from datetime import datetime

# Настройка страницы (должна быть первой командой!)
st.set_page_config(
    page_title="Око за око",
    page_icon="👁️",
    layout="centered"
)

# Инициализация БД
conn = sqlite3.connect('game_stats.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    opponent_strategy TEXT,
    user_score INTEGER,
    opponent_score INTEGER,
    result TEXT,
    played_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)''')
conn.commit()

# Стратегии бота
strategies = {
    'Всегда сотрудничать': lambda _, oh: 'cooperate',
    'Всегда предавать': lambda _, oh: 'betray',
    'Случайный выбор': lambda _, oh: random.choice(['cooperate', 'betray']),
    'Око за око': lambda _, oh: 'cooperate' if not oh else oh[-1],
    'Подозрительное око': lambda mh, oh: 'betray' if not mh else oh[-1]
}

def get_or_create_user(username):
    cursor.execute('SELECT id FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    if user: return user[0]
    cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
    conn.commit()
    return cursor.lastrowid

def init_game_state():
    if 'game' not in st.session_state:
        st.session_state.game = {
            'round': 0,
            'user_score': 0,
            'bot_score': 0,
            'user_choices': [],
            'bot_choices': [],
            'strategy': None,
            'user_id': None
        }

def show_stats():
    st.header("📊 Статистика игроков")
    
    # Лучшие игроки
    cursor.execute('''
        SELECT u.username, SUM(g.user_score), COUNT(g.id)
        FROM games g
        JOIN users u ON g.user_id = u.id
        GROUP BY u.username
        ORDER BY SUM(g.user_score) DESC
        LIMIT 10''')
    players = cursor.fetchall()
    
    df_players = pd.DataFrame(players, columns=['Игрок', 'Очки', 'Игр'])
    fig1 = px.bar(df_players, x='Игрок', y='Очки', title="Топ игроков по очкам")
    st.plotly_chart(fig1)
    
    # Эффективность стратегий
    cursor.execute('''
        SELECT opponent_strategy, 
               AVG(user_score),
               COUNT(*),
               SUM(CASE WHEN result='loss' THEN 1 ELSE 0 END) AS bot_wins
        FROM games
        GROUP BY opponent_strategy''')
    strats = cursor.fetchall()
    
    df_strats = pd.DataFrame(strats, columns=['Стратегия', 'Средние очки', 'Игр', 'Победы бота'])
    fig2 = px.pie(df_strats, names='Стратегия', values='Игр', title="Распределение стратегий")
    st.plotly_chart(fig2)
    
    # Линейный график побед бота
    cursor.execute('''
        SELECT played_at, SUM(CASE WHEN result='loss' THEN 1 ELSE 0 END) AS bot_wins
        FROM games
        GROUP BY played_at
        ORDER BY played_at''')
    bot_wins = cursor.fetchall()
    
    df_bot_wins = pd.DataFrame(bot_wins, columns=['Дата', 'Победы бота'])
    fig3 = px.line(df_bot_wins, x='Дата', y='Победы бота', title="Победы бота по датам")
    st.plotly_chart(fig3)

def play_round(user_choice):
    bot_choice = strategies[st.session_state.game['strategy']](
        st.session_state.game['user_choices'],
        st.session_state.game['bot_choices']
    )
    
    # Расчет очков
    if user_choice == 'cooperate' and bot_choice == 'cooperate':
        us, bs = 3, 3
    elif user_choice == 'cooperate' and bot_choice == 'betray':
        us, bs = 0, 5
    elif user_choice == 'betray' and bot_choice == 'cooperate':
        us, bs = 5, 0
    else:
        us, bs = 1, 1
    
    # Обновление состояния
    st.session_state.game['user_score'] += us
    st.session_state.game['bot_score'] += bs
    st.session_state.game['user_choices'].append(user_choice)
    st.session_state.game['bot_choices'].append(bot_choice)
    st.session_state.game['round'] += 1

def show_game():
    st.header("🎮 Игра: Око за око")
    
    if st.session_state.game['round'] >= 10:
        # Сохранение результатов
        result = 'win' if st.session_state.game['user_score'] > st.session_state.game['bot_score'] else 'loss'
        cursor.execute('''
            INSERT INTO games 
            (user_id, opponent_strategy, user_score, opponent_score, result)
            VALUES (?,?,?,?,?)''',
            (st.session_state.game['user_id'],
             st.session_state.game['strategy'],
             st.session_state.game['user_score'],
             st.session_state.game['bot_score'],
             result))
        conn.commit()
        
        # Показ результатов
        st.success(f"Игра завершена! Результат: {result.upper()}")
        st.metric(label="Ваши очки", value=st.session_state.game['user_score'])
        st.metric(label="Очки бота", value=st.session_state.game['bot_score'])
        
        # Сброс состояния
        del st.session_state.game
        return

    st.subheader(f"Раунд {st.session_state.game['round'] + 1}/10")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🤝 Сотрудничать", use_container_width=True):
            play_round('cooperate')
    with col2:
        if st.button("🔪 Предать", use_container_width=True):
            play_round('betray')
    
    # Прогресс игры
    st.progress(st.session_state.game['round'] / 10)
    st.write(f"Текущий счёт: {st.session_state.game['user_score']} : {st.session_state.game['bot_score']}")

# Отдельная страница для статистики
def stats_page():
    st.title("📊 Статистика")
    show_stats()

# Новая страница с предисловием и ссылкой
def shapes_page():
    st.title("🖼️ Фигуры")
    st.write("""
        Добро пожаловать на страницу с фигурами! Здесь вы можете перейти на другой сайт, 
        где можно передвигать фигуры. Это отличный способ расслабиться и потренировать 
        свои навыки пространственного мышления.
    """)
    st.markdown("[Перейти к фигурам](https://www.desmos.com/3d/pswxnacwyy)")

# Навигация
page = st.sidebar.selectbox("Выберите страницу", ["Игра", "Статистика", "Фигуры"])

if page == "Игра":
    st.title("👁️ Око за око: Эволюция сотрудничества")
    init_game_state()
    
    # Ввод имени пользователя
    username = st.text_input("Введите ваш никнейм:")
    if not username:
        st.stop()
    
    user_id = get_or_create_user(username)
    st.session_state.game['user_id'] = user_id
    
    # Выбор стратегии
    if not st.session_state.game['strategy']:
        strategy = st.selectbox(
            "Выберите стратегию бота:",
            list(strategies.keys())
        )
        if st.button("Начать игру"):
            st.session_state.game['strategy'] = strategy
            st.rerun()
        st.stop()
    
    show_game()

elif page == "Статистика":
    stats_page()

elif page == "Фигуры":
    shapes_page()