import extra_streamlit_components as stx
import datetime
import streamlit as st

cookie_manager = stx.CookieManager()

def set_uid_cookie(uid: str):
    cookie_manager.set("uid", uid, key="set_uid", expires_at=datetime.datetime.now() + datetime.timedelta(days=7))

def get_uid_cookie():
    if "uid" not in st.session_state:
        uid = cookie_manager.get("uid")
        if uid:
            st.session_state.uid = uid
            return uid
        else:
            return None
    return st.session_state.uid