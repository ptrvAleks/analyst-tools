import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader

def load_authenticator():
    """
    Загружает конфиг из users.yaml и создаёт объект Authenticate.
    Возвращает: stauth.Authenticate
    """
    with open("users.yaml", "r", encoding="utf-8") as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        credentials=config["credentials"],
        cookie_name=config["cookie"]["name"],
        key=config["cookie"]["key"],
        cookie_expiry_days=config["cookie"]["expiry_days"],
        preauthorized=config.get("preauthorized", {})
    )
    return authenticator