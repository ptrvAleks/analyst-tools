import streamlit as st
from auth import login, signup

def show_login(cookies):
    st.title("Авторизация")


    with st.form(key="login_form"):
        user_email = st.text_input("Почта", key="login_user_email", autocomplete="username")
        password = st.text_input("Пароль", type="password", key="password", autocomplete="current-password")
        submit = st.form_submit_button("Войти")

        user = login(user_email, password)
        if submit and user:
            st.session_state.authenticated = True
            st.session_state.username = user_email

            cookies["username"] = user_email
            cookies["auth"] = "true"
            cookies.save()
            st.rerun()
        elif submit:
            st.error("Неверные данные")

    # with st.form(key="register_form"):
    #     user_email = st.text_input("Почта", key="register_user_email", autocomplete="username")
    #     password = st.text_input("Пароль", type="password", key="register_password", autocomplete="current-password")
    #     submit = st.form_submit_button("Регистрация")
    #
    #     user = signup(user_email, password)
    #     if submit and user:
    #         st.session_state.authenticated = True
    #         st.session_state.username = user_email
    #
    #         cookies["username"] = user_email
    #         cookies["auth"] = "true"
    #         cookies.save()
    #         st.rerun()
    #     elif submit:
    #         st.error("Ошибка регистрации")