import firebase_admin
from firebase_admin import firestore, credentials
import streamlit as st

bd_cred = credentials.Certificate(dict(st.secrets["firebase"]))
firebase_admin.initialize_app(bd_cred)

db = firestore.client()