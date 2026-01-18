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

# 🔥 هذا يمنع إعادة تهيئة قاعدة البيانات كل مرة
@st.cache_resource
def init_database_once():
    init_db()
    ensure_settings()

def main():
    # تهيئة مرة واحدة فقط
    init_database_once()
    
    user = login_required()
    
    if user:
        render_dashboard(user)

if __name__ == "__main__":
    main()
