import io
import re
import wave
import hashlib
from datetime import datetime

import pandas as pd
import streamlit as st

# Optional speech-to-text dependency. The app remains usable without it.
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except Exception:
    sr = None
    SPEECH_RECOGNITION_AVAILABLE = False


# ============================================================
# INTERVIEWREADY — FREE-FIRST AI INTERVIEW COACH MVP
# Speech recognition uses Google's public web recognizer:
# no API key is required, but internet/service availability applies.
# Scores and written feedback are transparent heuristics, not an LLM.
# ============================================================

st.set_page_config(
    page_title="InterviewReady | AI Interview Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------- DESIGN ----------------------------

st.markdown(
    """
    <style>
    :root {
        --navy: #101d36;
        --navy-2: #1b3157;
        --blue: #3568c8;
        --blue-soft: #eaf1ff;
        --gold: #f2bd55;
        --ink: #18263d;
        --muted: #52627a;
        --line: #d9e2ef;
        --surface: #ffffff;
        --page: #f3f6fb;
        --green: #16845b;
        --red: #b83d4b;
    }
    .stApp { background: var(--page); color: var(--ink); }
    [data-testid="stHeader"] { background: rgba(243,246,251,.92); }
    [data-testid="stSidebar"] { background: var(--navy); }
    [data-testid="stSidebar"] * { color: #f7f9ff !important; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        border-radius: 9px; padding: 7px 10px;
    }
    h1,h2,h3,h4 { color: var(--navy) !important; font-weight: 780 !important; }
    p, li, label, .stMarkdown { color: var(--ink); }
    [data-testid="stWidgetLabel"] p { color: #263954 !important; font-weight: 650; }
    [data-testid="stCaptionContainer"] p { color: var(--muted) !important; }
    input, textarea {
        color: #17243b !important; background: #fff !important;
        -webkit-text-fill-color: #17243b !important;
    }
    textarea::placeholder, input::placeholder {
        color: #738198 !important; -webkit-text-fill-color: #738198 !important;
    }
    div[data-baseweb="select"] > div {
        background: #fff !important; color: #17243b !important;
        border-color: #b9c7da !important;
    }
    div[data-baseweb="select"] * { color: #17243b !important; }
    [role="listbox"] * { color: #17243b !important; background: #fff !important; }
    [data-testid="stNumberInput"] input { color: #17243b !important; }
    [data-testid="stMetric"] {
        background: #fff; border: 1px solid var(--line);
        padding: 14px 16px; border-radius: 13px;
        box-shadow: 0 3px 12px rgba(16,29,54,.04);
    }
    [data-testid="stMetricLabel"] { color: #52627a !important; }
    [data-testid="stMetricValue"] { color: var(--navy) !important; }
    .hero {
        background: linear-gradient(118deg, #101d36 0%, #24477e 72%, #3568c8 100%);
        padding: 30px 32px; border-radius: 19px; margin: 2px 0 25px 0;
        border: 1px solid rgba(255,255,255,.12);
        box-shadow: 0 10px 26px rgba(16,29,54,.13);
    }
    .hero h1 { color: #fff !important; margin: 0 0 7px 0; font-size: 2.25rem; }
    .hero p { color: #eaf1ff !important; margin: 0; font-size: 1.02rem; }
    .eyebrow { color: #f2bd55 !important; font-weight: 800; letter-spacing: .12em;
               text-transform: uppercase; font-size: .75rem; margin-bottom: 8px; }
    .panel {
        background: #fff; border: 1px solid var(--line); border-radius: 15px;
        padding: 19px 21px; margin: 10px 0;
