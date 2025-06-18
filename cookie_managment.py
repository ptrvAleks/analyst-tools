import extra_streamlit_components as stx
import datetime

cookie_manager = stx.CookieManager()

def set_uid_cookie(uid: str):
    cookie_manager.set("uid", uid, key="set_uid", expires_at=datetime.datetime.now() + datetime.timedelta(days=7))

def get_uid_cookie():
    result = cookie_manager.get("uid")
    if result and result["uid"]:
        return result["uid"]
    return None