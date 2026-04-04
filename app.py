import streamlit as st
from dotenv import load_dotenv
from src.agent import get_response

load_dotenv()

st.set_page_config(page_title="AI Finance Assistant", page_icon="🤖")

# =========================
# TITLE
# =========================
st.title("🤖 AI Finance Assistant")
st.caption("RAG + Search + LLM powered system")

# =========================
# CHAT MEMORY
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# DISPLAY CHAT
# =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# INPUT
# =========================
query = st.chat_input("Ask about RBI, SEBI, Finance, or Latest News...")

if query:
    # user message
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    # assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_response(query)
            st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )