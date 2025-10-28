import subprocess
from pathlib import Path
import argparse
import tomli

def flatten_secrets(prefix, d):
    """
    Рекурсивно превращает вложенные словари в плоский dict с ключами через _
    """
    flat = {}
    for k, v in d.items():
        new_key = f"{prefix}_{k}" if prefix else k
        if isinstance(v, dict):
            flat.update(flatten_secrets(new_key, v))
        else:
            flat[new_key] = v
    return flat

# Парсим аргумент среды
parser = argparse.ArgumentParser(description="Создать Docker Secrets из st.secrets.toml")
parser.add_argument("--env", required=True, help="Среда: dev, prod, staging")
args = parser.parse_args()
env = args.env

# Путь к st.secrets.toml
secrets_file = Path(".streamlit/secretsProd.toml")
if not secrets_file.exists():
    raise FileNotFoundError(f"{secrets_file} не найден")

# Загружаем весь toml
with open(secrets_file, "rb") as f:
    all_secrets = tomli.load(f)

# Плоский словарь с ключами вида env_section_key
flat_secrets = {}
for section_name, section_values in all_secrets.items():
    if isinstance(section_values, dict):
        flat_secrets.update(flatten_secrets(f"{env}_{section_name}", section_values))
    else:
        flat_secrets[f"{env}_{section_name}"] = section_values

# Папка для временных файлов
tmp_dir = Path("./tmp_secrets")
tmp_dir.mkdir(exist_ok=True)

# Создаём Docker Secrets
existing = subprocess.run(
    ["docker", "secret", "ls", "--format", "{{.Name}}"],
    capture_output=True, text=True
).stdout.splitlines()

for key, value in flat_secrets.items():
    secret_name = key
    secret_path = tmp_dir / f"{secret_name}.txt"

    # Записываем значение в файл
    with open(secret_path, "w") as f:
        f.write(str(value))

    if secret_name in existing:
        print(f"Secret '{secret_name}' уже существует, пропускаем.")
    else:
        subprocess.run(["docker", "secret", "create", secret_name, str(secret_path)], check=True)
        print(f"Secret '{secret_name}' создан.")
