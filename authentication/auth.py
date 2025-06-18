import pyrebase
import streamlit as st

# Инициализация Firebase
cred_dict = dict(st.secrets["firebaseConfig"])
firebase = pyrebase.initialize_app(cred_dict)
auth = firebase.auth()


def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        id_token = user['idToken']
        account_info = auth.get_account_info(id_token)
        uid = account_info['users'][0]['localId']
        return {"user": user, "uid": uid}  # возвращаем user-объект с токеном
    except Exception as e:
        print("Login failed:", e)
        return None

def signup(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        return user
    except Exception as e:
        print("Signup failed:", e)
        return None