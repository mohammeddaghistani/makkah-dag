import base64
from pathlib import Path
from typing import Optional

import streamlit as st

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def _b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def apply_branding(page_title: str = "تقدير القيمة الإيجارية للعقارات الاستثمارية") -> Optional[Path]:
    """RTL + modern brand UI (NO set_page_config here). Returns logo path if present."""

    primary = "#A88040"  # gold
    accent = "#4F9A4C"   # green
    bg = "#F7F5F0"       # warm off-white
    card = "#FFFFFF"
    text = "#111827"
    muted = "#6B7280"

    logo = ASSETS_DIR / "logo.png"
    font = ASSETS_DIR / "Tajawal-Regular.ttf"

    font_css = ""
    if font.exists():
        font_b64 = _b64(font)
        font_css = f"""
        @font-face {{
            font-family: 'Tajawal';
            src: url(data:font/ttf;base64,{font_b64}) format('truetype');
            font-weight: 400;
            font-style: normal;
        }}
        """

    css = f"""
    <style>

      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

      :root {{
        --primary: {primary};
        --accent: {accent};
        --bg: {bg};
        --card: {card};
        --text: {text};
        --muted: {muted};
        --radius: 18px;
      }}

      {font_css}

      /* RTL + digits in English: put a Latin font first so digits render Western */
      html, body, [class*="css"], [data-testid="stAppViewContainer"] {{
        direction: rtl;
        font-family: Inter, 'Tajawal', system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        font-variant-numeric: lining-nums tabular-nums;
        background: var(--bg);
        color: var(--text);
      }}

      /* Keep inputs digits Western as well */
      input, textarea, [data-baseweb="select"] * {{
        font-family: Inter, 'Tajawal', system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif !important;
        font-variant-numeric: lining-nums tabular-nums;
      }}

      .block-container {{
        max-width: 1180px;
        padding-top: 1.2rem;
        padding-bottom: 2.6rem;
      }}

      header[data-testid="stHeader"] {{ display: none; }}
      footer {{ visibility: hidden; }}

      .md-card {{
        background: var(--card);
        border-radius: var(--radius);
        border: 1px solid rgba(17,24,39,0.08);
        box-shadow: 0 6px 28px rgba(15,23,42,0.06);
        padding: 1.05rem 1.15rem;
      }}

      .stButton > button {{
        border-radius: 14px !important;
        padding: 0.55rem 1.0rem !important;
        border: 1px solid rgba(17,24,39,0.12) !important;
      }}
      .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, var(--primary), var(--accent)) !important;
        color: #fff !important;
        border: none !important;
      }}

      .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        border-radius: 14px !important;
      }}

      .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        border-bottom: 1px solid rgba(17,24,39,0.12);
        padding-bottom: 6px;
      }}
      .stTabs [data-baseweb="tab"] {{
        padding: 10px 14px;
        border-radius: 14px;
        background: rgba(255,255,255,0.75);
        border: 1px solid rgba(17,24,39,0.08);
      }}
      .stTabs [aria-selected="true"] {{
        background: rgba(168,128,64,0.12);
        border: 1px solid rgba(168,128,64,0.35);
      }}

      /* Make metric cards nicer */
      [data-testid="stMetric"] {{
        background: rgba(255,255,255,0.85);
        border: 1px solid rgba(17,24,39,0.08);
        border-radius: 16px;
        padding: 12px 14px;
      }}
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)
    return logo if logo.exists() else None


def render_footer():
    st.markdown(
        """
        <div style="margin-top:22px;padding:14px 10px;border-top:1px solid rgba(17,24,39,.10);opacity:.92">
          <div><b>© محمد داغستاني 2026</b></div>
          <div>مبادرة تطوير الأعمال بإشراف ودعم أ. عبدالرحمن خجا</div>
          <div style="color:rgba(17,24,39,.70)">للاستخدام الداخلي – غير مخصص للنشر</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
