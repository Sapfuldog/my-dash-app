# Используем базовый образ Miniconda
FROM continuumio/miniconda3

# Установка зависимостей
COPY environment.yml /tmp/environment.yml

# Создаем новое окружение conda с зависимостями из environment.yaml
RUN conda env create -f environment.yaml

# Активируем созданное окружение
RUN echo "conda activate $(head -1 environment.yaml | cut -d' ' -f2)" >> ~/.bashrc


# Устанавливаем пакеты pip внутри активированного окружения
RUN /bin/bash -c "source activate $(head -1 environment.yaml | cut -d' ' -f2) && \
                  pip install dash-vega-components"

# Устанавливаем рабочую директорию
WORKDIR /app

# Открываем порт 8050
EXPOSE 8050

# Команда для запуска приложения
CMD ["conda", "run", "-n", "myenv", "python", "app.py"]
