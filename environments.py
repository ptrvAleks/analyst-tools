def get_environment():
    try:
        import streamlit as st
        if "prod" in st.secrets:
            return "prod"
    except (ImportError, AttributeError, KeyError):
        return "dev"
