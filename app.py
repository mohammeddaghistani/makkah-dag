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

def main():
    # 1. تهيئة قاعدة البيانات والإعدادات
    init_db()
    ensure_settings()
    
    # 2. التحقق من تسجيل الدخول (سيعرض واجهة الدخول إذا لم يسجل)
    user = login_required()
    
    # 3. عرض لوحة التحكم وتمرير بيانات المستخدم
    if user:
        render_dashboard(user)

if __name__ == "__main__":
    main()
