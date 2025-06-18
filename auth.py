import pyrebase
import streamlit as st


cred_dict = dict(st.secrets["firebaseConfig"])

firebase = pyrebase.initialize_app(cred_dict)
auth=firebase.auth()

def login(email, password):
    try:
        login = auth.sign_in_with_email_and_password(email, password)
        return login
    except:
        print("Login failed")
        return None

def signup(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        return user
    except:
        print("Email or password is incorrect")
        return None

