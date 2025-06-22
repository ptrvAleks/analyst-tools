FROM python:3.12-slim

WORKDIR /app

# Копируем зависимости и устанавливаем
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код (на всякий случай)
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]