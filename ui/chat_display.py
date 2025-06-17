import streamlit as st
from ui.file_uploader import render_file_upload_popup

def render_chat_ui(on_user_input):
    chat_id = st.session_state.active_chat
    history = st.session_state.chats.get(chat_id, [])

    st.markdown("""
    <style>
    .welcome-box {
        text-align: center;
        padding: 4rem 1rem 2rem 1rem;
        color: #ccc;
        opacity: 0.85;
    }
    .welcome-box h1 {
        font-size: 2.2rem;
        font-weight: 600;
    }
    .welcome-box p {
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

    if not history:
        st.markdown("""
        <div class="welcome-box">
            <h1>👋 Welcome to Expert Chatbot</h1>
            <p>Start chatting or upload a document to begin.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for sender, msg in history:
            with st.chat_message(sender):
                st.markdown(msg, unsafe_allow_html=False)

    st.markdown("<div style='height: 3rem'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([10, 1])
    with col1:
        user_input = st.chat_input("Type your message here...")
    with col2:
        render_file_upload_popup()

    if user_input:
        on_user_input(user_input, st)  
