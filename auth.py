import streamlit as st
import streamlit_authenticator as stauth

def get_authenticator():
    credentials = {
        "usernames": {
            "analyst": {
                "name": st.secrets["credentials"]["usernames"]["analyst"]["name"],
                "password": st.secrets["credentials"]["usernames"]["analyst"]["password"]
            }
        }
    }

    cookie_name = st.secrets["auth"]["cookie_name"]
    cookie_key = st.secrets["auth"]["cookie_key"]
    cookie_expiry_days = st.secrets["auth"]["cookie_expiry_days"]

    authenticator = stauth.Authenticate(
        credentials,
        cookie_name,
        cookie_key,
        cookie_expiry_days
    )

    return authenticator