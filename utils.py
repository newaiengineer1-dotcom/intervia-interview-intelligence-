import os, re
import streamlit as st
from groq import Groq
try:
    from pypdf import PdfReader
except Exception:
    PdfReader = None
CATEGORIES=["Behavioral & Situational 🎭","Technical & Role-Specific 💻","HR & Screening Basics 🤝","Leadership & Management 👔","Case & Analytical Interviews 📊","Competency & Skill-Based 🧠","Reverse Interviewing 🔍"]
DURATION_TARGETS={30:8,60:15,120:28,180:40}
def get_groq_client():
    key=None
    try: key=st.secrets.get("GROQ_API_KEY")
    except Exception: pass
    key=key or os.getenv("GROQ_API_KEY")
    return Groq(api_key=key) if key else None
def extract_uploaded_text(f):
    if not f:return ""
    if f.name.lower().endswith('.txt'): return f.getvalue().decode('utf-8',errors='ignore')
    if f.name.lower().endswith('.pdf') and PdfReader:
        try:return '\n'.join((p.extract_text() or '') for p in PdfReader(f).pages)
        except Exception:return ""
    return ""
def clean_text(x,n=12000): return re.sub(r'\s+',' ',x or '').strip()[:n]
