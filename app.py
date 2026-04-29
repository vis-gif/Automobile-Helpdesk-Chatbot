import streamlit as st
from chat_engine import generate_response

st.set_page_config(page_title="AutoBot — Car Help Desk", page_icon="🚗", layout="wide")

import base64
import os

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    # Look for local background image
    if os.path.exists('background.png'):
        bg_ext = 'png'
        bg_base64 = get_base64_of_bin_file('background.png')
    else:
        bg_ext = 'jpeg'
        bg_base64 = get_base64_of_bin_file('background.jpg')
    bg_url = f"data:image/{bg_ext};base64,{bg_base64}"
except Exception:
    # Fallback to unsplash
    bg_url = "https://images.unsplash.com/photo-1558486012-817176f84c6d?q=80&w=2500&auto=format&fit=crop"

# Inject Custom CSS for HUD/Glassmorphism styling
st.markdown(f"""
<style>
    /* Full Page Background */
    .stApp {{
        background-image: url('{bg_url}'); /* Futuristic dark abstract/cyberpunk bg */
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* Hide top header and main padding */
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}
    
    /* Typography & Neon Text */
    h1, h2, h3, p, span, div, li {{
        font-family: 'Exo 2', 'Inter', sans-serif !important;
        color: #e0ffff !important;
    }}
    
    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {{
        background-color: rgba(5, 10, 20, 0.6) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border-right: 1px solid rgba(0, 255, 255, 0.3) !important;
    }}
    
    /* Sidebar Brand */
    [data-testid="stSidebar"] h1 {{
        font-size: 2.2rem !important;
        color: #00f3ff !important;
        text-shadow: 0 0 15px rgba(0,243,255,0.8);
        letter-spacing: 2px;
        margin-top: 10px;
        margin-bottom: 0px;
    }}
    
    /* Sidebar Items */
    .sidebar-category {{
        background: rgba(0, 243, 255, 0.03);
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 8px;
        border-left: 3px solid rgba(0, 243, 255, 0.5);
        border-top: 1px solid rgba(0, 243, 255, 0.1);
        border-bottom: 1px solid rgba(0, 243, 255, 0.1);
        transition: all 0.3s ease;
        cursor: default;
        font-size: 0.95rem;
    }}
    .sidebar-category:hover {{
        background: rgba(0, 243, 255, 0.15);
        border-left: 5px solid #00f3ff;
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.2);
        transform: translateX(4px);
    }}
    
    /* Main Area Container - THE HUD PANEL */
    .block-container {{
        background: rgba(10, 15, 25, 0.6);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 243, 255, 0.3);
        border-radius: 25px;
        padding: 40px !important;
        margin-top: 60px;
        margin-bottom: 60px;
        box-shadow: 0 0 40px rgba(0, 243, 255, 0.1) inset, 0 20px 50px rgba(0,0,0,0.8);
        max-width: 900px !important;
    }}
    
    /* Chip Buttons */
    .stButton>button {{
        background: rgba(0, 243, 255, 0.05) !important;
        border: 1px solid rgba(0, 243, 255, 0.5) !important;
        color: #00f3ff !important;
        border-radius: 20px !important;
        padding: 8px 15px !important;
        font-weight: 500;
        transition: all 0.3s ease;
        width: 100%;
        font-size: 0.85rem !important;
        margin-bottom: 10px;
        box-shadow: inset 0 0 10px rgba(0, 243, 255, 0.1);
    }}
    .stButton>button:hover {{
        background: rgba(0, 243, 255, 0.25) !important;
        border-color: #00f3ff !important;
        box-shadow: 0 0 20px rgba(0, 243, 255, 0.4), inset 0 0 15px rgba(0, 243, 255, 0.2);
        text-shadow: 0 0 8px rgba(0, 243, 255, 0.8);
    }}
    
    /* Chat Input */
    .stChatInputContainer {{
        background: rgba(0, 0, 0, 0.5) !important;
        border: 1px solid rgba(0, 243, 255, 0.5) !important;
        border-radius: 30px !important;
        padding-left: 10px !important;
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.1);
    }}
    
    /* Chat Bubbles */
    .stChatMessage {{
        background: rgba(0, 243, 255, 0.03) !important;
        border: 1px solid rgba(0, 243, 255, 0.15) !important;
        border-radius: 15px !important;
        padding: 15px !important;
        margin-bottom: 15px;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
    }}
    [data-testid="chatAvatarIcon-user"] {{
        background-color: rgba(0, 243, 255, 0.2) !important;
        color: #fff !important;
    }}
    [data-testid="chatAvatarIcon-assistant"] {{
        background-color: #00f3ff !important;
        color: #000 !important;
    }}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("<h1>AUTOBOT</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#a0e8ff; margin-top:-5px; margin-bottom:30px; font-size:1.05rem;'>Car Help Desk</p>", unsafe_allow_html=True)

categories = [
    ("🔦", "Warning Lights"),
    ("🔋", "Battery Problems"),
    ("🌡️", "Overheating"),
    ("🛞", "Tyre Issues"),
    ("🔊", "Strange Noises"),
    ("🛑", "Brake Problems"),
    ("❄️", "Air Conditioning"),
    ("💧", "Fluid Leaks"),
    ("🔧", "Maintenance"),
    ("💨", "Vibration & Handling")
]
for icon, title in categories:
    st.sidebar.markdown(f"<div class='sidebar-category'>{icon} &nbsp;&nbsp;{title}</div>", unsafe_allow_html=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []

# Main area Hero Text
st.markdown("<h2 style='color:#00f3ff !important; text-shadow: 0 0 15px rgba(0,243,255,0.6); margin-bottom:0px;'>Your Intelligent Car Diagnostics AI.</h2>", unsafe_allow_html=True)
st.markdown("<p style='color:#a0e8ff !important; margin-bottom: 30px;'>Select an issue below or type your problem directly into the console.</p>", unsafe_allow_html=True)

# Chips (Starter questions)
col1, col2, col3 = st.columns(3)
col4, col5, _ = st.columns(3)

starter_questions = [
    ("🔦", "Check engine light is on", col1),
    ("🔋", "Car won't start", col2),
    ("🛑", "Brakes making noise", col3),
    ("💧", "Liquid leaking under my car", col4),
    ("🌡️", "Car is overheating", col5)
]

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Handle chip clicks by setting a session state var to trigger the chat input
if "chip_query" not in st.session_state:
    st.session_state.chip_query = None

for icon, text, col in starter_questions:
    with col:
        if st.button(f"{icon} {text}"):
            st.session_state.chip_query = text

st.markdown("<hr style='border-color: rgba(0,243,255,0.2);'>", unsafe_allow_html=True)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input or chip click
prompt = st.chat_input("Ask about your car problem...")
if st.session_state.chip_query:
    prompt = st.session_state.chip_query
    st.session_state.chip_query = None

if prompt:
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Diagnosing..."):
            response = generate_response(prompt, st.session_state.messages)
            st.markdown(response)
            
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})

