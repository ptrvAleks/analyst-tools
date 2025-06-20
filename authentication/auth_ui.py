import streamlit as st
from authentication.auth import login, signup
from cookie_firebase_uid import set_uid_cookie

def show_login(cookies):
    st.title("Авторизация")
    if "login_user_email" not in st.session_state:
        st.session_state["login_user_email"] = ""

    if "password" not in st.session_state:
        st.session_state["password"] = ""

    # ---------- Форма логина ----------
    with st.form(key="login_form"):
        login_email = st.text_input("Почта", key="login_user_email",
                                    autocomplete="username")
        login_pwd = st.text_input("Пароль", type="password", key="password",
                                  autocomplete="current-password")
        login_submit = st.form_submit_button("Войти")

        if login_submit:
            user = login(login_email, login_pwd)
            if user:
                uid = user["localId"]
                st.session_state.update({
                    "authenticated": True,
                    "username": login_email,
                    "uid": uid,
                })
                set_uid_cookie(uid)
                cookies["username"] = login_email
                cookies["auth"] = "true"
                cookies["uid"] = uid
                cookies.save()
                st.rerun()
            else:
                st.error("Неверные данные")

    # ---------- Форма регистрации ----------
    st.title("Регистрация")
    with st.form(key="register_form"):
        reg_email = st.text_input("Почта", key="register_user_email",
                                  autocomplete="username")
        reg_pwd = st.text_input("Пароль", type="password",
                                key="register_password",
                                autocomplete="new-password")
        reg_submit = st.form_submit_button("Регистрация")

        if reg_submit:
            new_user = signup(reg_email, reg_pwd)
            if new_user:
                uid = new_user["localId"]
                st.session_state.update({
                    "authenticated": True,
                    "username": reg_email,
                    "uid": uid,
                })
                set_uid_cookie(uid)
                cookies["username"] = reg_email
                cookies["auth"] = "true"
                cookies["uid"] = uid
                cookies.save()
                st.rerun()
            else:
                st.error("Ошибка регистрации")