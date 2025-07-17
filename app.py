import streamlit as st
import pandas as pd
import numpy as np
from model import train_model
import base64
from pathlib import Path
import os

# --- Image Handling ---
def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    return base64.b64encode(img_bytes).decode()

def img_to_html(img_path, width=None):
    img_format = img_path.split('.')[-1]
    img_b64 = img_to_bytes(img_path)
    style = f"width:{width}px;" if width else ""
    return f'<img src="data:image/{img_format};base64,{img_b64}" style="{style}">'

# --- CSS Injection ---
def inject_css():
    css_path = os.path.join(Path(__file__).parent, "assets/css/style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- JS Injection ---
def inject_js():
    js_path = os.path.join(Path(__file__).parent, "assets/js/script.js")
    if os.path.exists(js_path):
        with open(js_path) as f:
            st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)

# --- App Config ---
st.set_page_config(
    page_title="AI Health Monitor",
    page_icon="🏥",
    layout="wide"
)

# Inject assets
inject_css()
inject_js()

# --- HTML Templates ---
def page_header():
    st.markdown(f"""
    <div class="header">
        {img_to_html("assets/images/logo.png", 80)}
        <h1>AI Health Monitor</h1>
        {img_to_html("assets/images/banner.jpg")}
    </div>
    """, unsafe_allow_html=True)

# --- Pages ---
def introduction_page():
    page_header()
    st.markdown("""
    <div class="card">
        <h2><i class="fas fa-user"></i> Patient Profile</h2>
        <div class="form-container">
    """, unsafe_allow_html=True)
    
    with st.form("profile_form"):
        cols = st.columns(2)
        with cols[0]:
            name = st.text_input("Full Name")
            age = st.number_input("Age", 1, 120)
        with cols[1]:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            weight = st.number_input("Weight (kg)", 30, 200)
        
        if st.form_submit_button("Save Profile"):
            st.session_state.profile = {
                "name": name, "age": age,
                "gender": gender, "weight": weight
            }
            st.success("Profile saved!")

    st.markdown("</div></div>", unsafe_allow_html=True)

def health_monitor_page():
    page_header()
    st.markdown("""
    <div class="card">
        <h2><i class="fas fa-heartbeat"></i> Health Monitoring</h2>
        <div class="metrics-container">
    """, unsafe_allow_html=True)
    
    # Your monitoring content here
    st.markdown("</div></div>", unsafe_allow_html=True)

# --- Navigation ---
PAGES = {
    "Profile": introduction_page,
    "Monitor": health_monitor_page
}

page = st.sidebar.radio("Navigation", list(PAGES.keys()))
PAGES[page]()
