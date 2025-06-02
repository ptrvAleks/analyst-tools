import streamlit_authenticator as stauth
import streamlit as st

def get_authenticator():
    credentials = {
        "usernames": dict(st.secrets['credentials']['usernames'])
    }
    cookie_name = st.secrets["cookie"]["name"]
    cookie_key = st.secrets["cookie"]["key"]
    expiry_days = st.secrets["cookie"]["expiry_days"]

    authenticator = stauth.Authenticate(
        credentials,  # <- обычный словарь
        cookie_name,
        cookie_key,
        expiry_days
    )

    return authenticator