# ui/users_page.py
import streamlit as st
from logic.user import User
from database.db_methods import delete_user_data


def run_user_list():
    @st.cache_data(show_spinner=False)
    def load_users():
        return User.get_all_users()

    if "edit_user" not in st.session_state:
        st.session_state["edit_user"] = None

    def user_card(u: User, index: int):
        with st.container():
            edit_key = f"edit_{index}_{u.uid}"
            html = f"""
            <div style="
                border: 2px solid #ddd;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
            ">
                <h4>{u.first_name or "—"}</h4>
                <p><strong>Email:</strong> {u.email}</p>
                <p><strong>Role:</strong> {u.role or "—"}</p>
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)

            if st.button("✏️ Редактировать", key=edit_key):
                st.session_state["edit_user"] = u
                st.rerun()

    def edit_user_form(u: User):
        st.markdown("## ✏️ Редактирование пользователя")

        if st.button("← Назад"):
            st.session_state["edit_user"] = None
            st.rerun()

        new_name = st.text_input("Имя", value=u.first_name or "")
        new_role = st.selectbox("Роль", ["admin", "user"], index=["admin", "user"].index(u.role or "user"))
        new_email = st.text_input("Почта", value=u.email or "")

        if st.button("💾 Сохранить изменения"):
            User.set_user_first_name(u.uid, new_name)
            User.set_user_role(u.uid, new_role)
            if new_email and new_email != u.email:
                User.update_user_email(u.uid, new_email)
            st.success("Данные обновлены.")
            st.cache_data.clear()
            st.session_state["edit_user"] = None
            st.rerun()

        if st.button("🗑 Удалить пользователя"):
            User.delete_user(u.uid)
            delete_user_data(u.uid)
            st.success("Пользователь удалён")
            st.cache_data.clear()
            st.session_state["edit_user"] = None
            st.rerun()

    # ---------- UI ----------
    st.title("Пользователи")
    users = load_users()
    if not users:
        st.info("Пользователи не найдены.")
        return

    # Форма редактирования
    if st.session_state["edit_user"]:
        edit_user_form(st.session_state["edit_user"])
        return  # не показываем список

    # Список пользователей
    st.subheader("Все пользователи")
    cols_per_row = 3
    for i in range(0, len(users), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, (col, u) in enumerate(zip(cols, users[i:i + cols_per_row])):
            index = i + j
            with col:
                user_card(u, index)