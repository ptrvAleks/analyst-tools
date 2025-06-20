# auth_ui.py
from authentication.auth_manager import AuthManager
import streamlit as st

def show_login(auth: AuthManager):
    st.title("Авторизация")

    with st.form(key="login_form"):
        email = st.text_input("Почта", key="login_user_email", autocomplete="username")
        pwd = st.text_input("Пароль", type="password", key="login_password", autocomplete="current-password")
        submit = st.form_submit_button("Войти")
        if submit:
            if not email:
                st.error("Введите почту")
            elif not pwd:
                st.error("Введите пароль")
            elif not auth.login(email, pwd):
                st.error("Неверные данные")

    st.subheader("Регистрация")
    reg_email = st.text_input("Почта", key="register_user_email", autocomplete="username")
    reg_pwd   = st.text_input("Пароль", type="password", key="register_password", autocomplete="new-password")

    if st.button("Регистрация"):
        if not auth.register(reg_email, reg_pwd):
            st.error("Ошибка регистрации")
        else:
            st.success("Пользователь зарегистрирован")