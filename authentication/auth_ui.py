# auth_ui.py
from authentication.auth_manager import AuthManager
import streamlit as st


def show_login(auth: AuthManager):
    # Инициализируем режим, если нет
    if "auth_mode" not in st.session_state:
        st.session_state["auth_mode"] = "login"
    if "login_submitted" not in st.session_state:
        st.session_state["login_submitted"] = False
    if "register_submitted" not in st.session_state:
        st.session_state["register_submitted"] = False

    if st.session_state.get("authenticated"):
        st.stop()

    if st.session_state["auth_mode"] == "login":
        st.title("Авторизация")
        with st.form(key="login_form"):
            email = st.text_input("Почта", key="login_user_email", autocomplete="username")
            pwd = st.text_input("Пароль", type="password", key="login_password", autocomplete="current-password")
            col1, col2 = st.columns(2)
            with col1:
                login_btn = st.form_submit_button("Войти", disabled=st.session_state["login_submitted"])
            with col2:
                go_register_btn = st.form_submit_button("Зарегистрироваться")

            if login_btn:
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

            if go_register_btn:
                # Переключаемся на режим регистрации
                st.session_state["auth_mode"] = "register"
                # Чтобы обновить интерфейс сразу
                st.rerun()

    elif st.session_state["auth_mode"] == "register":
        st.title("Регистрация")
        with st.form(key="register_form"):
            reg_email = st.text_input("Почта*", key="register_user_email", autocomplete="username")
            reg_pwd = st.text_input("Пароль*", type="password", key="register_password", autocomplete="new-password")
            reg_first_name = st.text_input("Имя", key="register_name", autocomplete="new-name")
            col1, col2 = st.columns(2)
            with col1:
                register_btn = st.form_submit_button("Регистрация", disabled=st.session_state["register_submitted"])
            with col2:
                back_btn = st.form_submit_button("Назад")

            if register_btn:
                st.session_state["register_submitted"] = True
                if not auth.register(reg_email, reg_pwd, reg_first_name):
                    st.error("Ошибка регистрации")
                    st.session_state["register_submitted"] = False
                else:
                    st.success("Пользователь зарегистрирован")
                    st.session_state["register_submitted"] = True
                    # После успешной регистрации возвращаемся к логину
                    st.session_state["auth_mode"] = "login"
                    st.rerun()

            if back_btn:
                # Возврат к форме логина
                st.session_state["auth_mode"] = "login"
                st.rerun()