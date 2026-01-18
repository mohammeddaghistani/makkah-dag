import hashlib
import pandas as pd
import streamlit as st
from sqlalchemy.orm import Session

# استيراد الأدوات اللازمة
from modules.auth import require_role
from modules.db import AppSettings, SessionLocal, User, get_settings
from modules.utils import now_iso

def _hash(pw):
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

def _settings_ui():
    st.subheader("⚙️ إعدادات التقييم الأساسية")
    s = get_settings()

    with st.expander("📊 المعايير الحسابية للتقييم", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            yield_rate_pct = st.number_input("نسبة العائد المستهدف (%)", min_value=0.1, max_value=50.0, value=float(s.yield_rate_pct), step=0.1, key="set_yield")
        with c2:
            grace_period_years = st.number_input("فترة السماح (بالسنوات)", min_value=0.0, max_value=10.0, value=float(s.grace_period_years), step=0.5, key="set_grace")
        with c3:
            rent_to_sale_pct = st.number_input("نسبة الإيجار من قيمة البيع (%)", min_value=0.0, max_value=100.0, value=float(s.rent_to_sale_pct), step=0.1, key="set_rent_to_sale")

        if st.button("💾 حفظ الإعدادات العامة", type="primary", key="settings_save", use_container_width=True):
            db: Session = SessionLocal()
            try:
                row = db.query(AppSettings).filter(AppSettings.id == 1).first()
                row.yield_rate_pct = float(yield_rate_pct)
                row.grace_period_years = float(grace_period_years)
                row.rent_to_sale_pct = float(rent_to_sale_pct)
                row.updated_at = now_iso()
                db.commit()
                st.success("✅ تم تحديث إعدادات النظام بنجاح")
                st.rerun()
            finally:
                db.close()

# تم إضافة متغير user هنا ليتوافق مع استدعاء render_dashboard
def admin_ui(user):
    # الإصلاح المهم: تمرير متغير user أولاً ثم القائمة لتجنب AttributeError
    require_role(user, allowed_roles=["admin"])

    st.title("🛡️ لوحة تحكم المدير العام")
    
    tabs = st.tabs(["👥 إدارة المستخدمين", "⚙️ إعدادات التقييم"])

    with tabs[0]:
        st.subheader("إدارة صلاحيات الوصول")

        with st.expander("➕ إضافة مستخدم جديد للنظام", expanded=False):
            u = st.text_input("اسم المستخدم", key="admin_add_user")
            pw = st.text_input("كلمة المرور", type="password", key="admin_add_pw")
            role = st.selectbox("الدور الوظيفي / الصلاحية", ["admin", "committee", "valuer", "data_entry"], key="admin_add_role")
            if st.button("إنشاء الحساب", type="primary", key="admin_create_user"):
                if not u or not pw:
                    st.warning("⚠️ الرجاء إدخال كافة البيانات المطلوبة")
                else:
                    db: Session = SessionLocal()
                    try:
                        exists = db.query(User).filter(User.username == u).first()
                        if exists:
                            st.error("❌ اسم المستخدم هذا مسجل مسبقاً")
                        else:
                            db.add(User(username=u, password_hash=_hash(pw), role=role, is_active=True))
                            db.commit()
                            st.success(f"✅ تم إنشاء حساب ({u}) بنجاح")
                            st.rerun()
                    finally:
                        db.close()

        # عرض جدول المستخدمين الحاليين
        db: Session = SessionLocal()
        try:
            users = db.query(User).order_by(User.id.desc()).all()
            data = [{"المعرف": x.id, "اسم المستخدم": x.username, "الصلاحية": x.role, "نشط": "نعم" if x.is_active else "لا"} for x in users]
        finally:
            db.close()

        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.divider()
            st.subheader("🔄 إدارة حالة الحسابات")
            
            # جلب قائمة الأسماء من قاعدة البيانات مباشرة للتأكد من المزامنة
            usernames = [x.username for x in users]
            sel = st.selectbox("اختر مستخدم لتغيير حالته", usernames, key="admin_select_user")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔴 تعطيل الحساب", key="admin_disable", use_container_width=True):
                    db: Session = SessionLocal()
                    try:
                        x = db.query(User).filter(User.username == sel).first()
                        # منع الأدمن من تعطيل نفسه
                        if x and x.username != st.secrets.get("ADMIN_USERNAME", "admin"):
                            x.is_active = False
                            db.commit()
                            st.success(f"🚫 تم تعطيل حساب {sel}")
                            st.rerun()
                        else:
                            st.error("⚠️ لا يمكن تعطيل حساب المدير العام من هنا")
                    finally:
                        db.close()
            with col2:
                if st.button("🟢 تفعيل الحساب", key="admin_enable", use_container_width=True):
                    db: Session = SessionLocal()
                    try:
                        x = db.query(User).filter(User.username == sel).first()
                        if x:
                            x.is_active = True
                            db.commit()
                            st.success(f"✅ تم تفعيل حساب {sel}")
                            st.rerun()
                    finally:
                        db.close()
        else:
            st.info("ℹ️ لا يوجد مستخدمون مسجلون في النظام حالياً.")

    with tabs[1]:
        _settings_ui()
