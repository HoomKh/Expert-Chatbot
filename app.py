import streamlit as st
from logic.session import initialize_session_state
from logic.chat_handler import handle_user_input
from ui.sidebar import render_sidebar
from ui.chat_display import render_chat_ui

def main():
    initialize_session_state(st)
    render_sidebar()
    render_chat_ui(handle_user_input)

if __name__ == "__main__":
    main()
