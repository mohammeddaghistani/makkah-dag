import streamlit as st
from modules.style import apply_branding

# =========================
# Footer (كان مفقودًا)
# =========================
def render_footer():
    st.markdown("""
    <style>
    .footer {
        margin-top: 50px;
        padding: 15px;
        text-align: center;
        color: #777;
        font-size: 13px;
        direction: rtl;
        border-top: 1px solid #e5e5e5;
    }
    </style>
    <div class="footer">
        © محمد داغستاني 2026 — مبادرة تطوير الأعمال بإشراف ودعم أ. عبدالرحمن خجا
    </div>
    """, unsafe_allow_html=True)


# =========================
# Login Required
# =========================
def login_required():
    apply_branding("تقدير القيمة الإيجارية للعقارات الاستثمارية")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return {
            "username": st.session_state.get("username", "admin"),
            "role": "admin"
        }

    st.markdown("### 🔐 تسجيل الدخول")

    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")

    if st.button("دخول"):
        # تسجيل دخول تجريبي (يمكن ربطه بقاعدة بيانات لاحقًا)
        if username and password:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("الرجاء إدخال اسم المستخدم وكلمة المرور")

    # ⬅️ هذا هو السطر الذي كان يسبب الانهيار
    render_footer()

    st.stop()
