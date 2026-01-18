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
# Role guard (تم التعديل الجذري هنا لحل كل أنواع الأخطاء)
# =========================
def require_role(user, allowed_roles=("admin",)):
    """
    تتحقق من الصلاحية وتمنع الأخطاء حتى لو تم تمرير المدخلات بشكل خاطئ.
    """
    # 1. التحقق إذا تم تبديل المدخلات بالخطأ (إذا كان المدخل الأول قائمة والثاني نص)
    if isinstance(user, list) and isinstance(allowed_roles, str):
        # تصحيح الخطأ تلقائياً: تبديل القيم لمكانها الصحيح
        actual_allowed_roles = user
        # محاولة جلب المستخدم الحالي من الجلسة بما أن الأول ليس مستخدماً
        user = st.session_state.get("user")
        allowed_roles = actual_allowed_roles

    if not user:
        st.error("يلزم تسجيل الدخول للوصول لهذه الصفحة.")
        st.stop()

    # 2. معالجة نوع بيانات المستخدم (Dictionary vs List)
    current_user_data = user
    if isinstance(user, list):
        if len(user) > 0 and isinstance(user[0], dict):
            current_user_data = user[0]
        else:
            st.error("بيانات المستخدم غير صالحة أو بتنسيق خاطئ.")
            st.stop()

    # 3. التأكد من أننا نتعامل مع قاموس الآن
    if not isinstance(current_user_data, dict):
        st.error(f"خطأ برمج في تمرير البيانات: المتوقع قاموس، الموجود {type(current_user_data).__name__}")
        st.stop()

    # 4. التحقق من الدور (Role)
    role = (current_user_data.get("role") or "").strip().lower()
    allowed = tuple(r.strip().lower() for r in (allowed_roles or ()))

    if role not in allowed:
        st.warning(f"ليس لديك صلاحية الوصول لهذه الصفحة. دورك: {role}")
        st.stop()

# =========================
# Login Required
# =========================
def login_required():
    _ensure_session()

    if st.session_state.auth.get("ok") and st.session_state.user:
        return st.session_state.user

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
            user_info = {"username": username, "role": "admin"}
            st.session_state.auth = {"ok": True, "user": username}
            st.session_state.user = user_info
            st.success("تم تسجيل الدخول بنجاح")
            st.rerun()
        else:
            st.error("بيانات الدخول غير صحيحة")

    render_footer()
    st.stop()
