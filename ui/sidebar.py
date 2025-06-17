import streamlit as st
from memory import get_short_term_memory


def render_sidebar():
    st.sidebar.markdown(
        """
        <style>
        .sidebar-title { font-size: 1.3rem; font-weight: 700; margin-bottom: 1.5rem; }
        .sidebar-btn { background-color: transparent; color: #e1e1e1; border: none; width: 100%; text-align: left; padding: 0.6rem 1rem; border-radius: 8px; margin-bottom: 0.25rem; font-size: 0.95rem; transition: background 0.2s; }
        .sidebar-btn:hover { background-color: #333; }
        .sidebar-btn.active { background-color: #4c4cff; font-weight: bold; color: white; }
        </style>
        """,
        unsafe_allow_html=True,
    )


    st.sidebar.markdown(
        "<div class='sidebar-title'>💬 Your Chats</div>", unsafe_allow_html=True
    )


    for name in st.session_state.chats:
        btn_class = (
            "sidebar-btn active"
            if name == st.session_state.active_chat
            else "sidebar-btn"
        )
        if st.sidebar.button(name, key=f"chat-{name}"):
            st.session_state.active_chat = name
            st.rerun()

    col1, col2 = st.sidebar.columns(2)
    if col1.button("➕", help="New Chat"):
        new_name = f"Chat_{len(st.session_state.chats) + 1}"
        st.session_state.chats[new_name] = []
        st.session_state.chat_memories[new_name] = get_short_term_memory()
        st.session_state.active_chat = new_name
        st.rerun()
    if col2.button("🗑️", help="Delete Chat"):
        if st.session_state.active_chat in st.session_state.chats:
            del st.session_state.chats[st.session_state.active_chat]
            del st.session_state.chat_memories[st.session_state.active_chat]
            remaining = list(st.session_state.chats.keys())
            if remaining:
                st.session_state.active_chat = remaining[0]
            else:
                new_name = "Chat_1"
                st.session_state.chats[new_name] = []
                st.session_state.chat_memories[new_name] = get_short_term_memory()
                st.session_state.active_chat = new_name
            st.rerun()
