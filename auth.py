import streamlit_authenticator as stauth
import streamlit as st

def get_authenticator():
    credentials = {
        "usernames": dict(st.secrets['credentials']['usernames'])
    }

    authenticator = stauth.Authenticate(
        credentials,
        st.secrets['cookie']['name'],
        st.secrets['cookie']['key'],
        st.secrets['cookie']['expiry_days']
    )

    return authenticator