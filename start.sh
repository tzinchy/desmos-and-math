#!/bin/bash
# Удаляем файл базы данных, если он существует
rm -f game_stats.db

# Запускаем основное приложение
streamlit run main.py