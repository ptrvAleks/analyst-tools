from my_secrets import get_secret

def get_firebase_config(env):
    """
    Собирает все firebase ключи для текущей среды в словарь.
    """
    env_keys_map = {
        "dev": "firebase",
        "prod": "firebase"
    }

    section_prefix = env_keys_map.get(env, "firebase")

    # Список всех стандартных ключей firebase
    firebase_keys = [
    "apiKey",
    "appId",
    "auth_provider_x509_cert_url",
    "auth_uri",
    "authDomain",
    "client_email",
    "client_id",
    "client_x509_cert_url",
    "databaseURL",
    "messagingSenderId",
    "private_key",
    "private_key_id",
    "project_id",
    "projectId",
    "storageBucket",
    "token_uri",
    "type",
    "universe_domain"
]


    config = {}
    for key in firebase_keys:
        secret_value = get_secret(env, f"{section_prefix}_{key}")
        if secret_value:
            config[key] = secret_value

    if not config:
        raise RuntimeError(f"Firebase credentials not found for env: {env}")

    return config