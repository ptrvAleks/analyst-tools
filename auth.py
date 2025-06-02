import streamlit as st
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader

def load_authenticator():
    credentials = st.secrets["credentials"]
    cookie = st.secrets["auth"]

    authenticator = stauth.Authenticate(
        credentials=credentials,
        cookie_name=cookie["cookie_name"],
        key=cookie["cookie_key"],
        cookie_expiry_days=cookie["cookie_expiry_days"]
    )
    return authenticator