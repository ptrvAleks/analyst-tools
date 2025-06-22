FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Проброс переменной окружения (на всякий случай)
ARG ENV
ENV ENV=${ENV}

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.runOnSave=true", "--server.port=8501", "--server.address=0.0.0.0"]