from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Magic Notes · Version 1",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .stApp { background: #f7f3ec; }
    .stMain { align-items: flex-start; }
    .block-container { max-width: none; padding: 0; }
    [data-testid="stHeader"], [data-testid="stToolbar"] { display: none; }
    iframe { display: block; }
    </style>
    """,
    unsafe_allow_html=True,
)

component_path = Path(__file__).resolve().parent
magic_notes = components.declare_component(
    "magic_notes_v1", path=str(component_path)
)
magic_notes(key="magic-notes-v1")
