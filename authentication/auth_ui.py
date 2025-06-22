# auth_ui.py
from authentication.auth_manager import AuthManager
import streamlit as st

def show_login(auth: AuthManager):
    st.title("Авторизация")
    if "login_submitted" not in st.session_state:
        st.session_state["login_submitted"] = False
    if st.session_state.get("authenticated"):
        st.stop()

    with st.form(key="login_form"):
        email = st.text_input("Почта", key="login_user_email", autocomplete="username")
        pwd = st.text_input("Пароль", type="password", key="login_password", autocomplete="current-password")
        submit = st.form_submit_button("Войти", disabled=st.session_state["login_submitted"])
        if submit:
            st.session_state["login_submitted"] = True
            if not email:
                st.error("Введите почту")
                st.session_state["login_submitted"] = False
            elif not pwd:
                st.error("Введите пароль")
                st.session_state["login_submitted"] = False
            elif not auth.login(email, pwd):
                st.error("Неверные данные")
                st.session_state["login_submitted"] = False
            else:
                st.success("Авторизация прошла успешно")
                st.session_state["login_submitted"] = True
                st.stop()

    st.subheader("Регистрация")

    reg_email = st.text_input("Почта*", key="register_user_email", autocomplete="username")
    reg_pwd   = st.text_input("Пароль*", type="password", key="register_password", autocomplete="new-password")
    reg_first_name = st.text_input("Имя", key="register_name", autocomplete="new-name")

    if "register_submitted" not in st.session_state:
        st.session_state["register_submitted"] = False

    if st.button("Регистрация", disabled=st.session_state["register_submitted"]):
        st.session_state["register_submitted"] = True
        if not auth.register(reg_email, reg_pwd, reg_first_name):
            st.error("Ошибка регистрации")
            st.session_state["register_submitted"] = False
        else:
            st.success("Пользователь зарегистрирован")
            st.session_state["register_submitted"] = True