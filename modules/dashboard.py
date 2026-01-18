import streamlit as st

# استيراد الدوال من الموديلات المختلفة
from modules.admin import admin_ui
from modules.deals import deals_ui
from modules.reports_ui import reports_ui
from modules.strategy import strategy_ui
from modules.style import apply_branding, render_footer
from modules.valuation_ui import valuation_ui

def render_dashboard(user):
    # 1. عرض الهوية (Branding)
    logo = apply_branding("تقدير القيمة الإيجارية للعقارات الاستثمارية")

    # 2. الشريط العلوي (Header)
    top = st.columns([1, 6, 2])
    with top[0]:
        if logo:
            st.image(str(logo), width=86)
    with top[1]:
        st.markdown(f"## 🏢 نظام تقدير القيمة الإيجارية")
        # تحسين عرض بيانات المستخدم
        st.info(f"👤 **المستخدم:** {user.get('username')} | 🔑 **الصلاحية:** {user.get('role').upper()}")
    
    with top[2]:
        st.write("") # موازنة رأسية
        if st.button("🚪 تسجيل الخروج", key="logout_btn", use_container_width=True):
            # مسح كافة بيانات الجلسة للتأكد من الخروج الآمن
            st.session_state.clear() 
            st.rerun()

    # 3. نظام التبويبات (Tabs)
    # ملاحظة: الترتيب هنا يحدد ما يراه المستخدم أولاً
    tabs = st.tabs(["📋 التقييم", "🤝 الصفقات", "📊 التقارير", "🎯 الاستراتيجية", "⚙️ الإدارة"])

    with tabs[0]:
        # نمرر user دائماً لضمان عمل require_role داخل الموديول
        valuation_ui(user)
        
    with tabs[1]:
        # تأكد أن دالة deals_ui في ملفها تستقبل user إذا أردت حمايتها
        deals_ui() 
        
    with tabs[2]:
        reports_ui(user)
        
    with tabs[3]:
        strategy_ui()
        
    with tabs[4]:
        # التحقق من أن المستخدم أدمن قبل عرض محتوى الإدارة
        if user.get("role") == "admin":
            admin_ui(user) # تم إضافة التمرير هنا لإصلاح الخطأ
        else:
            st.warning("⚠️ عذراً، هذه اللوحة مخصصة للمدير العام فقط.")
            st.image("https://cdn-icons-png.flaticon.com/512/4072/4072217.png", width=100)

    # 4. التذييل (Footer)
    render_footer()
    
    # وضع حقوق النشر داخل الدالة لضمان ظهورها في المكان الصحيح فقط
    st.markdown("---")
    st.caption("✨ جميع الحقوق محفوظة © 2026 - نظام مكة DAG الذكي")

# ملاحظة: تم حذف الأسطر التي كانت خارج الدالة لضمان نظافة واجهة الدخول
