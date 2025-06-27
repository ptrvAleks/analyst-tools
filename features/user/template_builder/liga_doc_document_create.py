import streamlit as st
import json
import uuid
from pathlib import Path
from io import BytesIO
from features.user.template_builder.document_routes import document_routes

TEMPLATES_DIR = Path(__file__).parent / "templates"

def load_template(key: str) -> str:
    template_path = TEMPLATES_DIR / f"{key}.json"
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


def render_template(template: str, values: dict):
    for key, val in values.items():
        if val == "null":  # строка "null" — как маркер для подстановки None
            template = template.replace(f'"${{{key}}}"', "null")  # если переменная в кавычках
            template = template.replace(f"${{{key}}}", "null")    # если переменная без кавычек
        elif isinstance(val, (dict, list)):
            json_val = json.dumps(val, ensure_ascii=False)
            template = template.replace(f"${{{key}}}", json_val)
        else:
            template = template.replace(f"${{{key}}}", str(val))
    return json.loads(template)

def run_liga_doc_create():

    # Выбор документа
    doc_types = list(document_routes.keys())
    selected_doc_type = st.selectbox("Тип документа", doc_types)

    # Выбор маршрута
    routes = document_routes.get(selected_doc_type, {})
    if not routes:
        st.warning("Для этого документа нет маршрутов")
        return

    route_names = list(routes.keys())
    selected_route = st.selectbox("Маршрут подписания", route_names)
    selected_users = routes[selected_route]

    try:
        with st.expander("Шаблон"):
            template = load_template("universal")
            # Получаем users из словаря маршрутов (то есть шаблонные данные)
            default_users = routes[selected_route]
            users_json = json.dumps(default_users, ensure_ascii=False)

            # Подставляем в шаблон (только users)
            template_with_users = template.replace("${users}", users_json)

            template_with_users = template_with_users.replace("${type}", selected_doc_type)

            st.subheader("📄 Шаблон запроса с предзаполненным users из маршрута")
            st.code(template_with_users, language="json")
    except FileNotFoundError:
        st.error("Не найден universal.json шаблон.")
        return

    # Подготовка переменных
    user_inputs = {
        # Автоматические значения
    "requestUuid": str(uuid.uuid4()),
    "number": "1",
    "externalId": str(uuid.uuid4()),
    "type": selected_doc_type,
    }


    # 🔧 Ручной ввод legalEntityId для каждого участника маршрута
    st.subheader("👤 Введите ext_1c_id для каждого участника")
    user_inputs_list = []
    for user in selected_users:
        user_type = user["type"]
        input_id = st.text_input(f"{user_type}", key=f"{selected_route}_{user_type}")
        user_inputs_list.append({
            "type": user_type,
            "legalEntityId": input_id
        })
    user_inputs["users"] = json.dumps(user_inputs_list, ensure_ascii=False)
    # Пользовательский ввод
    st.subheader("📝 Введите значения")
    user_inputs["name"] = st.text_input("Название документа")
    user_inputs["legalEntityExternalId"] = st.text_input("Юр лицо")
    user_inputs["fileId"] = st.text_input("fileId", "")
    user_inputs["date"] = st.date_input("date").strftime("%Y-%m-%d")
    # Хранение количества ссылок в сессии
    if "link_count" not in st.session_state:
        st.session_state.link_count = 1

    # Кнопки добавить/удалить ссылку
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Добавить ссылку"):
            st.session_state.link_count += 1
    with col2:
        if st.button("➖ Удалить последнюю") and st.session_state.link_count > 0:
            st.session_state.link_count -= 1

    # Ввод ссылок
    links = []
    for i in range(st.session_state.link_count):
        st.markdown(f"**Ссылка #{i + 1}**")
        title = st.text_input(f"Название ссылки #{i + 1}", key=f"link_title_{i}")
        link = st.text_input(f"URL ссылки #{i + 1}", key=f"link_url_{i}")
        if title and link:
            links.append({"title": title, "link": link})


    if st.button("🚀 Сгенерировать JSON"):
        try:
            if links:
                user_inputs["links"] = json.dumps(links, ensure_ascii=False)
            else:
                user_inputs["links"] = "null"  # шаблон примет null
            result = render_template(template, user_inputs)
            st.success("✅ Сгенерированный JSON:")
            st.json(result)

            buffer = BytesIO()
            buffer.write(json.dumps(result, indent=2, ensure_ascii=False).encode("utf-8"))
            buffer.seek(0)

            st.download_button(
                label="💾 Скачать результат",
                data=buffer,
                file_name=f"{selected_doc_type}_request.json",
                mime="application/json"
            )
        except Exception as e:
            st.error(f"Ошибка генерации: {e}")