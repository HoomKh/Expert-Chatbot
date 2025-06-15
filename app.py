import streamlit as st
import time
from chains import multi_chain
from handlers import StreamHandler

st.set_page_config(page_title="Expert Chatbot", page_icon="🧠")
st.title("🧠 Expert Chatbot")
st.caption("Ask anything — the bot will route your question to the most suitable expert domain.")

# Load CSS
st.markdown("""
    <style>
    .fade-in { animation: fadeIn 1.5s ease-in; }
    @keyframes fadeIn { 0% {opacity: 0; transform: translateY(10px);} 100% {opacity: 1; transform: translateY(0);} }
    .user-question { text-align: center; font-weight: bold; font-size: 1.05rem; }
    </style>
    """, unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.container():
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.chat_input("Type your question here...")
    with col2:
        if st.button("🧹", help="Clear Conversation"):
            st.session_state.chat_history = []
            st.rerun()

if user_input:
    container = st.empty()
    handler = StreamHandler(container)

    for chain in multi_chain.destination_chains.values():
        chain.llm.callbacks = [handler]
    multi_chain.default_chain.llm.callbacks = [handler]

    with st.spinner("Thinking..."):
        _ = multi_chain.run(user_input)

    container.empty()
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("assistant", f"\n{handler.text.strip()}"))

    blur_msg = st.empty()
    blur_msg.markdown("<div style='text-align:center; padding:1rem; font-size:1rem; color:gray;'>✨ Preparing expert response...</div>", unsafe_allow_html=True)
    time.sleep(2)
    blur_msg.empty()

for sender, msg in st.session_state.chat_history:
    with st.chat_message(sender):
        st.markdown(f"<div class='fade-in user-question'>{msg}</div>" if sender == "user" else f"<div class='fade-in'>{msg}</div>", unsafe_allow_html=True)
