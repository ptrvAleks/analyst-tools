def get_firebase_config(env: str = "dev"):
    try:
        import streamlit as st
    except ImportError:
        st = None

    if env == "prod":
        if st and "firebase" in st.secrets:
            # st.secrets уже словарь → можно напрямую
            firebase_dict = dict(st.secrets["firebase"])
            return firebase_dict
        else: print("Prod credentials not found")
    elif env == "dev":
        # dev
        firebase_dict = dict(st.secrets["firebaseDev"])
        if not firebase_dict:
            raise RuntimeError("firebaseDev")

        return firebase_dict


def get_environment():
    try:
        import streamlit as st
        if "firebase" in st.secrets:
            return "prod"
    except:
        pass
    return "dev"