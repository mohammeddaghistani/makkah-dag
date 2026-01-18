import os
import hmac
import streamlit as st
from modules.style import apply_branding, render_footer

# =========================
# إعدادات الدخول الافتراضية
# =========================
def _get_admin_creds():
    u = None
    p = None
    try:
        u = st.secrets.get("ADMIN_USERNAME", None)
        p = st.secrets.get("ADMIN_PASSWORD", None)
    except Exception:
        pass

    u = u or os.getenv("ADMIN_USERNAME", "admin")
    p = p or os.getenv("ADMIN_PASSWORD", "admin")
    return u, p

def _constant_time_eq(a: str, b: str) -> bool:
    try:
        return hmac.compare_digest(a or "", b or "")
    except Exception:
        return (a or "") == (b or "")

# =========================
# Session helpers
# =========================
def _ensure_session():
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
    st.success("تم تسجيل الخروج")
    st.rerun()

# =========================
# Role guard (تم التعديل هنا لحل المشكلة)
# =========================
def require_role(user, allowed_roles=("admin",)):
    """
    تتأكد من أن المستخدم يملك الصلاحية المطلوبة.
    تتعامل مع البيانات سواء كانت قاموساً أو قائمة.
    """
    if not user:
        st.error("يلزم تسجيل الدخول للوصول لهذه الصفحة.")
        st.stop()

    # حل مشكلة AttributeError: تحويل القائمة إلى قاموس إذا لزم الأمر
    current_user_data = user
    if isinstance(user, list):
        current_user_data = user[0] if len(user) > 0 else {}

    # التأكد من استخراج الدور (role) بأمان
    role = (current_user_data.get("role") or "").strip().lower()
    allowed = tuple(r.strip().lower() for r in (allowed_roles or ()))

    if role not in allowed:
        st.warning(f"ليس لديك صلاحية الوصول لهذه الصفحة. (دورك الحالي: {role})")
        st.stop()

# =========================
# Login Required
# =========================
def login_required():
    _ensure_session()

    # إذا كان المستخدم مسجلاً مسبقاً
    if st.session_state.auth.get("ok") and st.session_state.user:
        return st.session_state.user

    # واجهة دخول
    apply_branding("تقدير القيمة الإيجارية للعقارات الاستثمارية")

    st.markdown("### 🔐 تسجيل الدخول")
    col1, col2 = st.columns([2, 1])

    with col1:
        username = st.text_input("اسم المستخدم", key="login_username")
        password = st.text_input("كلمة المرور", type="password", key="login_password")

    with col2:
        st.write("")
        st.write("")
        do_login = st.button("دخول", use_container_width=True)

    if do_login:
        admin_u, admin_p = _get_admin_creds()

        if _constant_time_eq(username, admin_u) and _constant_time_eq(password, admin_p):
            # تخزين البيانات كقاموس واضح
            user_info = {"username": username, "role": "admin"}
            st.session_state.auth = {"ok": True, "user": username}
            st.session_state.user = user_info
            st.success("تم تسجيل الدخول بنجاح")
            st.rerun()
        else:
            st.error("بيانات الدخول غير صحيحة")

    render_footer()
    st.stop()
