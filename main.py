import streamlit as st
import numpy as np
import plotly.graph_objects as go
import webbrowser

# Заголовок
st.title("Методические указания: Вычисление производной")
st.markdown("**Специальность 09.02.07 Информационные системы и программирование**")
st.markdown("**Подготовил : Андреев Александр 44ИС-21**")
st.markdown("---")

# Введение
st.header("Введение")
st.write("""
Производные — это один из ключевых инструментов математического анализа, который позволяет изучать скорость изменения функций. 
В данных методических указаниях мы рассмотрим основные правила дифференцирования, примеры вычисления производных и их практическую значимость.
""")

# Основные правила дифференцирования
st.header("Основные правила дифференцирования")

st.subheader("Правило 1: Производная константы")
st.latex(r"f(x) = C \quad \Rightarrow \quad f'(x) = 0")
st.write("**Объяснение:** Константа не меняется, поэтому её скорость изменения равна нулю.")

# График для константы
x = np.linspace(-10, 10, 400)
f = 5 * np.ones_like(x)  # Пример константы f(x) = 5
f_prime = np.zeros_like(x)  # Производная константы

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=f, mode='lines', name="f(x) = 5"))
fig.add_trace(go.Scatter(x=x, y=f_prime, mode='lines', name="f'(x) = 0", line=dict(dash='dash')))
fig.update_layout(title="График константы и её производной", xaxis_title="x", yaxis_title="y")
st.plotly_chart(fig)

st.subheader("Правило 2: Производная линейной функции")
st.latex(r"f(x) = kx + b \quad \Rightarrow \quad f'(x) = k")
st.write("**Объяснение:** Константа \( b \) 'исчезает', а производная \( kx \) равна \( k \).")

# График для линейной функции
k, b = 2, 3  # Пример: f(x) = 2x + 3
f = k * x + b
f_prime = k * np.ones_like(x)  # Производная

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=f, mode='lines', name=f"f(x) = {k}x + {b}"))
fig.add_trace(go.Scatter(x=x, y=f_prime, mode='lines', name=f"f'(x) = {k}", line=dict(dash='dash')))
fig.update_layout(title="График линейной функции и её производной", xaxis_title="x", yaxis_title="y")
st.plotly_chart(fig)

st.subheader("Правило 3: Производная степенной функции")
st.latex(r"f(x) = x^n \quad \Rightarrow \quad f'(x) = n \cdot x^{n-1}")
st.write("**Примеры:**")
st.code("f(x) = x^2 → f'(x) = 2x")
st.code("f(x) = x^3 → f'(x) = 3x^2")

# График для степенной функции
n = 2  # Пример: f(x) = x^2
f = x**n
f_prime = n * x**(n-1)  # Производная

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=f, mode='lines', name=f"f(x) = x^{n}"))
fig.add_trace(go.Scatter(x=x, y=f_prime, mode='lines', name=f"f'(x) = {n}x^{n-1}", line=dict(dash='dash')))
fig.update_layout(title="График степенной функции и её производной", xaxis_title="x", yaxis_title="y")
st.plotly_chart(fig)

st.subheader("Правило 4: Производная суммы функций")
st.latex(r"f(x) = g(x) + h(x) \quad \Rightarrow \quad f'(x) = g'(x) + h'(x)")
st.write("**Пример:**")
st.code("f(x) = x^2 + 3x → f'(x) = 2x + 3")

# График для суммы функций
f = x**2 + 3*x  # Пример: f(x) = x^2 + 3x
f_prime = 2*x + 3  # Производная

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=f, mode='lines', name="f(x) = x^2 + 3x"))
fig.add_trace(go.Scatter(x=x, y=f_prime, mode='lines', name="f'(x) = 2x + 3", line=dict(dash='dash')))
fig.update_layout(title="График суммы функций и её производной", xaxis_title="x", yaxis_title="y")
st.plotly_chart(fig)

st.subheader("Правило 5: Производная экспоненциальной функции")
st.latex(r"f(x) = e^x \quad \Rightarrow \quad f'(x) = e^x")
st.write("**Объяснение:** Экспоненциальная функция \( e^x \) уникальна тем, что её производная равна самой функции.")

# График для экспоненциальной функции
f = np.exp(x)  # Пример: f(x) = e^x
f_prime = np.exp(x)  # Производная

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=f, mode='lines', name="f(x) = e^x"))
fig.add_trace(go.Scatter(x=x, y=f_prime, mode='lines', name="f'(x) = e^x", line=dict(dash='dash')))
fig.update_layout(title="График экспоненциальной функции и её производной", xaxis_title="x", yaxis_title="y")
st.plotly_chart(fig)

# Пример 1: Квадратичная функция
st.header("Пример 1: Квадратичная функция")
st.write("Исходные функции:")
st.code("f(x) = x^2 + 3x - 2")
st.code("g(x) = 3 + 2x")

st.write("Производные:")
st.code("f'(x) = 2x + 3")
st.code("g'(x) = 2")

st.write("Что происходит:")
st.write("- \( f(x) \) — парабола, её производная \( f'(x) \) — прямая линия.")
st.write("- \( g(x) \) — прямая линия, её производная \( g'(x) \) — константа.")

# График для квадратичной функции
f = x**2 + 3*x - 2  # Пример: f(x) = x^2 + 3x - 2
f_prime = 2*x + 3  # Производная

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=f, mode='lines', name="f(x) = x^2 + 3x - 2"))
fig.add_trace(go.Scatter(x=x, y=f_prime, mode='lines', name="f'(x) = 2x + 3", line=dict(dash='dash')))
fig.update_layout(title="График квадратичной функции и её производной", xaxis_title="x", yaxis_title="y")
st.plotly_chart(fig)

# Кнопка для перехода в Desmos
if st.button("Открыть Desmos для примера 1"):
    webbrowser.open("https://www.desmos.com/calculator")  # Замените на реальную ссылку

# Пример 2: Тригонометрические функции
st.header("Пример 2: Тригонометрические функции")
st.write("Исходные функции:")
st.code("f(x) = sin(x)")
st.code("g(x) = cos(x)")

st.write("Производные:")
st.code("f'(x) = cos(x)")
st.code("g'(x) = -sin(x)")

st.write("Что происходит:")
st.write("- Производные синуса и косинуса циклически повторяются каждые 4 шага.")

# График для тригонометрической функции
f = np.sin(x)  # Пример: f(x) = sin(x)
f_prime = np.cos(x)  # Производная

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=f, mode='lines', name="f(x) = sin(x)"))
fig.add_trace(go.Scatter(x=x, y=f_prime, mode='lines', name="f'(x) = cos(x)", line=dict(dash='dash')))
fig.update_layout(title="График синуса и его производной", xaxis_title="x", yaxis_title="y")
st.plotly_chart(fig)

# Кнопка для перехода в Desmos
if st.button("Открыть Desmos для примера 2"):
    webbrowser.open("https://www.desmos.com/calculator")  # Замените на реальную ссылку

# Пример 3: Экспоненциальные функции
st.header("Пример 3: Экспоненциальные функции")
st.write("Исходные функции:")
st.code("f(x) = a^x")
st.code("g(x) = a^x * ln(a)")

st.write("Производные:")
st.code("f'(x) = a^x * ln(a)")
st.code("g'(x) = a^x * (ln(a))^2")

st.write("Что происходит:")
st.write("- Экспоненциальная функция \( e^x \) уникальна тем, что её производная равна самой функции.")

# График для экспоненциальной функции
a = 2  # Пример: f(x) = 2^x
f = a**x
f_prime = a**x * np.log(a)  # Производная

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=f, mode='lines', name=f"f(x) = {a}^x"))
fig.add_trace(go.Scatter(x=x, y=f_prime, mode='lines', name=f"f'(x) = {a}^x * ln({a})", line=dict(dash='dash')))
fig.update_layout(title="График экспоненциальной функции и её производной", xaxis_title="x", yaxis_title="y")
st.plotly_chart(fig)

# Кнопка для перехода в Desmos
if st.button("Открыть Desmos для примера 3"):
    webbrowser.open("https://www.desmos.com/calculator")  # Замените на реальную ссылку

# Практическая значимость
st.header("Практическая значимость производных")
st.write("""
1. **Физика:** Производная пути по времени — это скорость.
2. **Экономика:** Производная функции прибыли показывает, как быстро меняется прибыль.
3. **Биология:** Производная используется для моделирования роста популяций.
4. **Инженерия:** Производные используются для расчёта прочности материалов.
5. **Медицина:** Производные помогают анализировать изменение концентрации лекарств в крови.
""")

# Теория про Эйлера
st.header("Теория про Эйлера")
st.write("""
Леонард Эйлер ввёл число \( e \) (основание натурального логарифма) и открыл формулу:
""")
st.latex(r"e^{ix} = \cos(x) + i \cdot \sin(x)")
st.write("Эта формула связывает экспоненциальные и тригонометрические функции.")

# Заключение
st.header("Заключение")
st.write("""
Производные — это мощный инструмент для анализа изменений. Они используются в физике, экономике, биологии, инженерии и медицине. 
Экспоненциальные и тригонометрические функции играют ключевую роль в моделировании реальных процессов.
""")