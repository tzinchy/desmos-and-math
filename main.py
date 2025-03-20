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
    'Око за око': lambda mh, oh: 'betray' if len(mh) >= 2 and mh[-1] == 'betray' and mh[-2] == 'betray' else 'cooperate',
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

def show_moves():
    """Функция для отображения ходов"""
    # Ходы пользователя
    st.markdown("**Ваши ходы**")
    cols = st.columns(10)
    for i in range(10):
        if i < len(st.session_state.game['user_choices']):
            move = st.session_state.game['user_choices'][i]
            color = "green" if move == "cooperate" else "red"
            cols[i].markdown(f"<div style='background-color: {color}; border-radius: 50%; width: 30px; height: 30px;'></div>", 
                           unsafe_allow_html=True)
        else:
            cols[i].markdown(f"<div style='background-color: lightgray; border-radius: 50%; width: 30px; height: 30px;'></div>", 
                           unsafe_allow_html=True)
    
    # Ходы бота
    st.markdown("**Ходы бота**")
    cols = st.columns(10)
    for i in range(10):
        if i < len(st.session_state.game['bot_choices']):
            move = st.session_state.game['bot_choices'][i]
            color = "green" if move == "cooperate" else "red"
            cols[i].markdown(f"<div style='background-color: {color}; border-radius: 50%; width: 30px; height: 30px;'></div>", 
                           unsafe_allow_html=True)
        else:
            cols[i].markdown(f"<div style='background-color: lightgray; border-radius: 50%; width: 30px; height: 30px;'></div>", 
                           unsafe_allow_html=True)

def show_stats():
    st.header("📊 Статистика игроков и стратегий")
    
    # Топ игроков по общему количеству баллов
    st.subheader("Топ игроков по общему количеству баллов")
    cursor.execute('''
        SELECT u.username, SUM(g.user_score) as total_score
        FROM games g
        JOIN users u ON g.user_id = u.id
        GROUP BY u.username
        ORDER BY total_score DESC
        LIMIT 10
    ''')
    top_players = cursor.fetchall()
    
    df_top_players = pd.DataFrame(top_players, columns=['Игрок', 'Общее количество баллов'])
    fig1 = px.bar(df_top_players, x='Игрок', y='Общее количество баллов', title="Топ игроков по баллам")
    st.plotly_chart(fig1)
    
    # Средние баллы по стратегиям
    st.subheader("Средние баллы по стратегиям")
    cursor.execute('''
        SELECT opponent_strategy, AVG(user_score) as avg_score
        FROM games
        GROUP BY opponent_strategy
    ''')
    avg_scores = cursor.fetchall()
    
    df_avg_scores = pd.DataFrame(avg_scores, columns=['Стратегия', 'Средние баллы'])
    fig2 = px.bar(df_avg_scores, x='Стратегия', y='Средние баллы', title="Средние баллы по стратегиям")
    st.plotly_chart(fig2)
    
    # Общее количество баллов по стратегиям
    st.subheader("Общее количество баллов по стратегиям")
    cursor.execute('''
        SELECT opponent_strategy, SUM(user_score) as total_score
        FROM games
        GROUP BY opponent_strategy
    ''')
    total_scores = cursor.fetchall()
    
    df_total_scores = pd.DataFrame(total_scores, columns=['Стратегия', 'Общее количество баллов'])
    fig3 = px.pie(df_total_scores, names='Стратегия', values='Общее количество баллов', title="Общее количество баллов по стратегиям")
    st.plotly_chart(fig3)
    
    # Количество игр по стратегиям
    st.subheader("Количество игр по стратегиям")
    cursor.execute('''
        SELECT opponent_strategy, COUNT(*) as games_count
        FROM games
        GROUP BY opponent_strategy
    ''')
    games_count = cursor.fetchall()
    
    df_games_count = pd.DataFrame(games_count, columns=['Стратегия', 'Количество игр'])
    fig4 = px.bar(df_games_count, x='Стратегия', y='Количество игр', title="Количество игр по стратегиям")
    st.plotly_chart(fig4)
    
    # Соотношение побед, поражений и ничьих
    st.subheader("Соотношение побед, поражений и ничьих")
    cursor.execute('''
        SELECT result, COUNT(*) as result_count
        FROM games
        GROUP BY result
    ''')
    results = cursor.fetchall()
    
    df_results = pd.DataFrame(results, columns=['Результат', 'Количество'])
    fig5 = px.pie(df_results, names='Результат', values='Количество', title="Соотношение побед, поражений и ничьих")
    st.plotly_chart(fig5)
    
    # Линейный график побед бота по датам
    st.subheader("Победы бота по датам")
    cursor.execute('''
        SELECT played_at, SUM(CASE WHEN result='loss' THEN 1 ELSE 0 END) AS bot_wins
        FROM games
        GROUP BY played_at
        ORDER BY played_at
    ''')
    bot_wins = cursor.fetchall()
    
    df_bot_wins = pd.DataFrame(bot_wins, columns=['Дата', 'Победы бота'])
    fig6 = px.line(df_bot_wins, x='Дата', y='Победы бота', title="Победы бота по датам")
    st.plotly_chart(fig6)

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

    # Если раунд завершён, завершаем игру
    if st.session_state.game['round'] >= 10:
        st.session_state.game['round'] = 10  # Фиксируем на 10 раундах
        st.rerun()  # Перезагружаем страницу для отображения результатов
    else:
        st.rerun()  # Обновляем интерфейс после каждого хода

def show_game():
    st.header("🎮 Игра: Cотрудничества и предательства")
    
    if st.session_state.game['round'] >= 10:
        # Определение результата
        if st.session_state.game['user_score'] > st.session_state.game['bot_score']:
            result = 'win'
        elif st.session_state.game['user_score'] < st.session_state.game['bot_score']:
            result = 'loss'
        else:
            result = 'draw'  # Ничья
        
        # Сохранение результатов
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
        if result == 'draw':
            st.success("Игра завершена! Результат: НИЧЬЯ")
        else:
            st.success(f"Игра завершена! Результат: {result.upper()}")
        st.metric(label="Ваши очки", value=st.session_state.game['user_score'])
        st.metric(label="Очки бота", value=st.session_state.game['bot_score'])
        st.write(f"Стратегия бота: **{st.session_state.game['strategy']}**")
        
        # Показ всех ходов
        show_moves()
        
        # Кнопка "Сыграть ещё раз"
        if st.button("🔄 Сыграть ещё раз", use_container_width=True):
            del st.session_state.game
            st.rerun()
        return

    st.subheader(f"Раунд {st.session_state.game['round'] + 1}/10")
    
    # Показ текущих ходов
    show_moves()
    
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
    
    st.write('''
    # Добро пожаловать на страницу с фигурами!
Здесь вы можете перейти на другой сайт, где можно передвигать фигуры. Это отличный способ расслабиться и потренировать свои навыки пространственного мышления.

---

## Уравнение конуса в трехмерном пространстве

### Пояснение переменных:
- **(x, y, z)** — координаты точки в трехмерном пространстве.
  - **(x)** — перемещение влево-вправо.
  - **(y)** — перемещение вперед-назад.
  - **(z)** — перемещение вверх-вниз.
- **(a_cone1)** — параметр, определяющий радиус основания конуса.
  - Чем больше **(a_cone1)**, тем шире основание конуса.
- **(h_cone1)** — параметр, определяющий высоту конуса.
  - Чем больше **(h_cone1)**, тем выше конус.

### Геометрический смысл:
Уравнение описывает все точки **(x, y, z)**, которые лежат на поверхности конуса с вершиной в точке **(x_cone1, y_cone1, z_cone1)**. Параметры **(a_cone1)** и **(h_cone1)** задают форму конуса: его ширину и высоту.

---

## Уравнение куба в трехмерном пространстве

Уравнение куба задается следующим образом:

$$
\\max(|x - x_{cube1}|, |y - y_{cube1}|, |z - z_{cube1}|) = a_{cube1}
$$

### Пояснение переменных:
- **(x, y, z)** — координаты точки в трехмерном пространстве.
  - **(x)** — перемещение влево-вправо.
  - **(y)** — перемещение вперед-назад.
  - **(z)** — перемещение вверх-вниз.
- **(x_cube1, y_cube1, z_cube1)** — координаты центра куба.
  - **(x_cube1)** — смещение центра куба по оси **(x)**.
  - **(y_cube1)** — смещение центра куба по оси **(y)**.
  - **(z_cube1)** — смещение центра куба по оси **(z)**.
- **(a_cube1)** — параметр, определяющий половину длины ребра куба.
  - Чем больше **(a_cube1)**, тем больше размер куба.

### Геометрический смысл:
Уравнение описывает все точки **(x, y, z)**, которые лежат на поверхности куба с центром в точке **(x_cube1, y_cube1, z_cube1)**. Параметр **(a_cube1)** задает размер куба.

---

## Уравнение сферы в трехмерном пространстве

Уравнение сферы задается следующим образом:

$$
(x - x_{sphere3})^2 + (y - y_{sphere3})^2 + (z - z_{sphere3})^2 = r_{sphere3}^2
$$

### Пояснение переменных:
- **(x, y, z)** — координаты точки в трехмерном пространстве.
  - **(x)** — перемещение влево-вправо.
  - **(y)** — перемещение вперед-назад.
  - **(z)** — перемещение вверх-вниз.
- **(x_sphere3, y_sphere3, z_sphere3)** — координаты центра сферы.
  - **(x_sphere3)** — смещение центра сферы по оси **(x)**.
  - **(y_sphere3)** — смещение центра сферы по оси **(y)**.
  - **(z_sphere3)** — смещение центра сферы по оси **(z)**.
- **(r_sphere3)** — радиус сферы.
  - Чем больше **(r_sphere3)**, тем больше размер сферы.

### Геометрический смысл:
Уравнение описывает все точки **(x, y, z)**, которые лежат на поверхности сферы с центром в точке **(x_sphere3, y_sphere3, z_sphere3)**. Параметр **(r_sphere3)** задает размер сферы.
''')

    st.markdown("[Перейти к фигурам](https://www.desmos.com/3d/qr2xgbo4vt)")

# Навигация
page = st.sidebar.selectbox("Выберите страницу", ["Игра", "Статистика", "Фигуры"])

if page == "Игра":
    st.title("👁️ Эволюция сотрудничества")
    init_game_state()
    
    # Ввод имени пользователя
    username = st.text_input("Введите ваш никнейм:")
    if not username:
        st.stop()
    
    user_id = get_or_create_user(username)
    st.session_state.game['user_id'] = user_id
    
    # Автоматический выбор случайной стратегии
    if not st.session_state.game['strategy']:
        st.session_state.game['strategy'] = random.choice(list(strategies.keys()))
        st.rerun()
    
    show_game()

elif page == "Статистика":
    stats_page()

elif page == "Фигуры":
    shapes_page()
