# Переменные
IMAGE_NAME = streamlit-app
CONTAINER_NAME = streamlit-container
PORT = 8501

# Сборка Docker-образа
build:
	docker build -t $(IMAGE_NAME) .

# Запуск контейнера
run:
	docker run -d -p $(PORT):$(PORT) --name $(CONTAINER_NAME) $(IMAGE_NAME)

# Остановка контейнера
stop:
	docker stop $(CONTAINER_NAME)

# Удаление контейнера
remove:
	docker rm -f $(CONTAINER_NAME)

# Перезапуск контейнера (остановка, удаление, запуск)
restart: stop remove run

# Очистка (удаление контейнера и образа)
clean:
	docker rm -f $(CONTAINER_NAME) || true
	docker rmi $(IMAGE_NAME) || true

# Просмотр логов контейнера
logs:
	docker logs -f $(CONTAINER_NAME)

# Проверка состояния контейнера
status:
	docker ps -a | grep $(CONTAINER_NAME)

# Помощь (список доступных команд)
help:
	@echo "Использование: make [команда]"
	@echo ""
	@echo "Команды:"
	@echo "  build     - Собрать Docker-образ"
	@echo "  run       - Запустить контейнер"
	@echo "  stop      - Остановить контейнер"
	@echo "  remove    - Удалить контейнер"
	@echo "  restart   - Перезапустить контейнер (остановить, удалить, запустить)"
	@echo "  clean     - Очистить (удалить контейнер и образ)"
	@echo "  logs      - Просмотр логов контейнера"
	@echo "  status    - Проверить состояние контейнера"
	@echo "  help      - Показать это сообщение"