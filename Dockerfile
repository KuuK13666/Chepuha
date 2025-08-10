# №1: База — официальный образ Python
FROM python:3.11-slim

# №2: Рабочая директория в контейнере
WORKDIR /app

# №3: (опционально) системные пакеты по минимуму
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# №4: Ставим зависимости Python (отдельным слоем — быстрее кэш)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# №5: Копируем исходники
COPY . .

# №6: Создаём каталоги под данные/файлы (на всякий)
RUN mkdir -p /app/data /app/tracks

# №7: Команда запуска
CMD ["python", "main.py"]
