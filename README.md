# Инструменты системного аналитика

Проект на Streamlit с набором полезных инструментов для работы с JSON, XML и авторизацией пользователей.

---

## Описание

Это веб-приложение предоставляет системным аналитикам и разработчикам удобный интерфейс для работы с JSON-данными и их конвертацией, а также управление пользователями с помощью авторизации и регистрации.

---

## Основные функции

- **Авторизация и регистрация**  
  Безопасный вход в приложение с сохранением данных пользователя.

- **Валидация JSON**  
  Проверка корректности JSON с подсветкой ошибок и указанием точного места ошибки.  
  Подсчет количества объектов в массиве.

- **Конвертация JSON ↔ XML**  
  Двусторонняя конвертация между форматами JSON и XML.

- **Сохранение результатов конвертации**  
  Все результаты конвертации сохраняются в базе данных для каждого пользователя.

- **Генерация JSON Schema**  
  Автоматическое создание JSON Schema на основании примера JSON.

- **Генерация фейковых данных**  
  Генерация тестовых JSON данных на основе JSON Schema для удобства тестирования и разработки.

---

## Технологии

- Python  
- Streamlit  
- Firebase (для авторизации и хранения данных)  
- JSON, XML обработка библиотеками Python

---

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/ptrvAleks/analyst-tools.git
   cd analyst-tools


2.	Установите зависимости:

pip install -r requirements.txt

3. В Streamlit Cloud Secrets добавьте данные Firebase (для авторизации и базы данных) и пароль для шифрования cookies
   
Пример:
```yaml
[firebase]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = """
-----BEGIN PRIVATE KEY-----\n
YOUR_PRIVATE_KEY_CONTENT_HERE\n
-----END PRIVATE KEY-----\n
"""
client_email = "firebase-adminsdk-abcde@your-project-id.iam.gserviceaccount.com"
client_id = "123456789012345678901"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-abcde%40your-project-id.iam.gserviceaccount.com"
universe_domain = "googleapis.com"

[cookies]
# Пример пароля для шифрования cookies (замените на свой)
password = "your-cookie-secret"

[firebaseConfig]
apiKey = "your-api-key"
authDomain = "your-project-id.firebaseapp.com"
databaseURL = "https://your-project-id-default-rtdb.region.firebasedatabase.app"
projectId = "your-project-id"
storageBucket = "your-project-id.appspot.com"
messagingSenderId = "123456789012"
appId = "1:123456789012:web:abcdef1234567890" ```


3. Запустите приложение:

streamlit run app.py



⸻

Использование

	1.	Зарегистрируйтесь или войдите в систему.
	2.	Выберите нужный инструмент в боковом меню.
	3.	Загружайте JSON данные или вводите вручную.
	4.	Валидируйте, конвертируйте или генерируйте данные в удобном формате.
	5.	Все ваши результаты сохраняются автоматически и доступны в вашем личном кабинете.


⸻

Планы на будущее

	•	Добавить поддержку других форматов (YAML, CSV)
	•	Расширить права доступа для разных ролей пользователей
	•	Добавить API для интеграции с внешними системами

⸻

Контакты

Если у вас есть вопросы или предложения — пишите на почту: alex.322175@gmail.com
