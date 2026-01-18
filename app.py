import streamlit as st

# يجب أن يكون إعداد الصفحة أول أمر في ملف app.py
st.set_page_config(
    page_title="تقدير القيمة الإيجارية للعقارات الاستثمارية",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from modules.db import init_db, ensure_settings
from modules.auth import login_required
from modules.dashboard import render_dashboard

# ✅ تهيئة قاعدة البيانات مرة واحدة فقط
@st.cache_resource
def init_database_once():
    init_db()
    ensure_settings()

def main():
    init_database_once()

    # منع إعادة الرندر غير الضروري
    if "user" not in st.session_state:
        st.session_state.user = None

    if not st.session_state.user:
        st.session_state.user = login_required()

    if st.session_state.user:
        render_dashboard(st.session_state.user)

if __name__ == "__main__":
    main()
