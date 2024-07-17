# Используем базовый образ Miniconda
FROM continuumio/miniconda3

# Установка зависимостей
COPY environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml

# Активируем окружение
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Устанавливаем рабочую директорию
WORKDIR /app

# Открываем порт 8050
EXPOSE 8050

# Команда для запуска приложения
CMD ["conda", "run", "-n", "myenv", "python", "app.py"]
