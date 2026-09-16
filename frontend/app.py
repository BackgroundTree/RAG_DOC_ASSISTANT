"""
Streamlit frontend for the Yakuza 0 RAG Assistant.

A simple chat interface that lets users ask questions about Yakuza 0
mechanics, substories, and minigames, backed by a RAG API.
"""

import streamlit as st

from api_client import send_query

# --------------------------------------------------------------------------
# Page configuration
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Yakuza 0 RAG Assistant",
    layout="centered",
)

st.title("🐉 Yakuza 0 RAG Assistant")
st.caption(
    "Ask me anything about Yakuza 0's mechanics, substories, or minigames. "
    "Answers are grounded in retrieved source material from the Kamurocho archives."
)

# --------------------------------------------------------------------------
# Session state initialization
# --------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []  # list[dict]: {"role", "content", "sources"}

# --------------------------------------------------------------------------
# Render past chat history
# --------------------------------------------------------------------------
for msg in st.session_state.messages:
    role = msg.get("role", "assistant")
    content = msg.get("content", "")

    with st.chat_message(role):
        st.markdown(content)

        if role == "assistant":
            sources = msg.get("sources")
            if sources:
                with st.expander("📚 Cited Sources"):
                    for source in sources:
                        st.markdown(f"- {source}")

# --------------------------------------------------------------------------
# Chat input and response handling
# --------------------------------------------------------------------------
prompt = st.chat_input("Ask about Yakuza 0 mechanics, substories, or minigames...")

if prompt:
    # 1. Append and render the user's message.
    st.session_state.messages.append({"role": "user", "content": prompt, "sources": []})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Query the backend and render the assistant's response.
    with st.chat_message("assistant"):
        with st.spinner("Searching Kamurocho archives..."):
            result = send_query(prompt)

        error = result.get("error")
        answer = result.get("answer", "")
        sources = result.get("sources", []) or []

        if error:
            st.error(error)
        else:
            st.markdown(answer)

            if sources:
                with st.expander("📚 Cited Sources"):
                    for source in sources:
                        st.markdown(f"- {source}")

            # 3. Persist the assistant's message in session state.
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                }
            )