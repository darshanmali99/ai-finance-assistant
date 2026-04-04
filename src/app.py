import streamlit as st
import os
from dotenv import load_dotenv

from src.agent import get_response

# Load environment variables
load_dotenv()

# =========================
# UI SETUP
# =========================
st.set_page_config(page_title="AI Finance Assistant", page_icon="🤖")

st.title("🤖 AI Finance Assistant (RAG + Search)")
st.write("Ask anything about RBI, SEBI, Finance, or Latest News")

# =========================
# INPUT
# =========================
query = st.text_input("Ask your question:")

# =========================
# RESPONSE
# =========================
if query:
    with st.spinner("Thinking..."):
        try:
            response = get_response(query)
            st.success(response)
        except Exception as e:
            st.error(f"Error: {str(e)}")