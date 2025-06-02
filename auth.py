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
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"]
    )
    return authenticator