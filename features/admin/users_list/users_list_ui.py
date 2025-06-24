# ui/users_page.py
import streamlit as st
from logic.user import User
from database.user_service import UserService

service = UserService()


def run_user_list():
    current_user: User | None = st.session_state.get("user")
    if current_user.role != "admin":
        st.error("Нет доступа")
        st.stop()

    def load_users():
        return service.get_all_users()

    if "edit_user" not in st.session_state:
        st.session_state["edit_user"] = None

    def user_card(user: User, idx: int):
        with st.container():
            edit_key = f"edit_{idx}_{user.uid}"
            html = f"""
            <div style="
                border: 2px solid #ddd;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
            ">
                <h4>{user.first_name or "—"}</h4>
                <p><strong>Email:</strong> {user.email}</p>
                <p><strong>Role:</strong> {user.role or "—"}</p>
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)

            if st.button("✏️ Редактировать", key=edit_key):
                st.session_state["edit_user"] = user
                st.rerun()

    def edit_user_form(user: User):
        st.markdown("## ✏️ Редактирование пользователя")

        if st.button("← Назад"):
            st.session_state["edit_user"] = None
            st.rerun()

        new_name = st.text_input("Имя", value=user.first_name or "")
        new_role = st.selectbox("Роль", ["admin", "user"], index=["admin", "user"].index(user.role or "user"))
        new_email = st.text_input("Почта", value=user.email or "")

        if st.button("💾 Сохранить изменения"):
            service.set_user_first_name(user, new_name)
            service.set_user_role(user, new_role)
            if new_email and new_email != user.email:
                service.update_user_email(user, new_email)
            st.success("Данные обновлены.")
            st.cache_data.clear()
            st.session_state["edit_user"] = None
            st.rerun()

        if st.button("🗑 Удалить пользователя"):
            # Удаляем пользователя из Firebase Auth
            deleted_auth = service.delete_user(user)
            # Удаляем Firestore данные (только если текущий пользователь — админ)
            deleted_data = service.delete_user_data(current_user, user.uid)

            if deleted_auth and deleted_data:
                st.success("Пользователь и его данные успешно удалены.")
                st.cache_data.clear()
                st.session_state["edit_user"] = None
                st.rerun()
            else:
                st.error("Не удалось удалить пользователя. Возможно, у вас недостаточно прав.")

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
        chunk = users[i:i + cols_per_row]
        for j, (col, u) in enumerate(zip(cols, chunk)):
            index = i + j
            with col:
                user_card(u, index)