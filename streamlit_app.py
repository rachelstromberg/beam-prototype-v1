"""Serve the reviewed interface as a separate Streamlit app."""
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title='Magic Notes · Customer leadership review',
    layout='wide',
    initial_sidebar_state='collapsed',
)
st.markdown('''
<style>
.stApp { background: #f8f9f5; }
.stMain { align-items: flex-start; }
.block-container { max-width: none; padding: 0; }
[data-testid="stHeader"], [data-testid="stToolbar"] { display: none; }
iframe { display: block; }
</style>
''', unsafe_allow_html=True)
review = components.declare_component(
    'magic_notes_customer_review',
    path=str(Path(__file__).resolve().parent / 'dist'),
)
review(key='magic-notes-customer-review')
