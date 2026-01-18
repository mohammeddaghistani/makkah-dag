import os
import hmac
import streamlit as st
from modules.style import apply_branding, render_footer

# ==========================================
# 1. إعدادات الدخول والـ Session
# ==========================================
def _get_admin_creds():
    """جلب بيانات المدير من الإعدادات السرية أو متغيرات البيئة"""
    u = st.secrets.get("ADMIN_USERNAME", os.getenv("ADMIN_USERNAME", "admin"))
    p = st.secrets.get("ADMIN_PASSWORD", os.getenv("ADMIN_PASSWORD", "admin"))
    return str(u), str(p)

def _ensure_session():
    """التأكد من تهيئة متغيرات الجلسة"""
    if "auth" not in st.session_state:
        st.session_state.auth = {"ok": False, "user": None}
    if "user" not in st.session_state:
        st.session_state.user = None

def current_user():
    _ensure_session()
    return st.session_state.user

def logout():
    _ensure_session()
    st.session_state.auth = {"ok": False, "user": None}
    st.session_state.user = None
    st.success("تم تسجيل الخروج بنجاح")
    st.rerun()

# ==========================================
# 2. نظام الصلاحيات (منح الأدمن كافة الصلاحيات)
# ==========================================
def require_role(user, allowed_roles=("admin",)):
    """
    تتحقق من صلاحية المستخدم. 
    ملاحظة: المدير (admin) يملك صلاحية الوصول الكاملة دائماً.
    """
    # معالجة الخطأ الشائع: إذا تم تمرير الصلاحيات كأول متغير بدلاً من user
    if isinstance(user, (list, tuple)) and not st.session_state.get("user"):
        st.error("خطأ تقني: لم يتم التعرف على بيانات المستخدم.")
        st.stop()
    
    # محاولة جلب المستخدم من الجلسة إذا كان المتغير الممرر غير صحيح
    actual_user = user
    if not isinstance(user, dict):
        if isinstance(user, list) and len(user) > 0 and isinstance(user[0], dict):
            actual_user = user[0]
        else:
            actual_user = st.session_state.get("user")

    if not actual_user:
        st.error("يلزم تسجيل الدخول للوصول لهذه الصفحة.")
        st.stop()

    # استخراج الدور (role) بأمان
    role = str(actual_user.get("role", "")).strip().lower()

    # --- القاعدة الذهبية: الأدمن يدخل كل مكان ---
    if role == "admin":
        return True 
    
    # التحقق لبقية الأدوار
    allowed = [str(r).strip().lower() for r in (allowed_roles or ())]
    if role not in allowed:
        st.warning(f"عذراً، لا تملك الصلاحية الكافية. الأدوار المسموحة: {', '.join(allowed)}")
        st.stop()

# ==========================================
# 3. واجهة تسجيل الدخول
# ==========================================
def login_required():
    """تفرض تسجيل الدخول وتعيد بيانات المستخدم كقاموس"""
    _ensure_session()
    
    # إذا كان مسجلاً بالفعل، نعود ببياناته
    if st.session_state.auth.get("ok") and st.session_state.user:
        return st.session_state.user

    # عرض واجهة الدخول
    apply_branding("تقدير القيمة الإيجارية للعقارات الاستثمارية")
    st.markdown("---")
    st.markdown("### 🔐 تسجيل الدخول للنظام")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        username = st.text_input("اسم المستخدم", placeholder="ادخل اسم المستخدم...")
        password = st.text_input("كلمة المرور", type="password", placeholder="ادخل كلمة المرور...")
    
    st.markdown(" ")
    if st.button("تسجيل الدخول", use_container_width=True, type="primary"):
        admin_u, admin_p = _get_admin_creds()
        
        # استخدام hmac للمقارنة الآمنة
        if hmac.compare_digest(username, admin_u) and hmac.compare_digest(password, admin_p):
            # إنشاء كائن المستخدم مع دور الأدمن
            user_info = {"username": username, "role": "admin"}
            st.session_state.auth = {"ok": True, "user": username}
            st.session_state.user = user_info
            st.success("مرحباً بك! جاري تحويلك للوحة التحكم...")
            st.rerun()
        else:
            st.error("عذراً، اسم المستخدم أو كلمة المرور غير صحيحة.")
    
    render_footer()
    st.stop()
