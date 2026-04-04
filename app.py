import streamlit as st
from src.agent import get_agent

st.title("🤖 AI Finance Assistant (Clean Version)")

agent = get_agent()

query = st.text_input("Ask your question:")

if query:
    with st.spinner("Thinking..."):
        response = agent.run(query)
        st.write(response)