from memory import get_long_term_memory, get_short_term_memory

#intialize session
def initialize_session_state(st):
    if "chats" not in st.session_state:
        st.session_state.chats = {"Chat_1": []}
    if "active_chat" not in st.session_state:
        st.session_state.active_chat = "Chat_1"
    if "chat_memories" not in st.session_state:
        st.session_state.chat_memories = {"Chat_1": get_short_term_memory()}
    if "long_term_memory" not in st.session_state:
        st.session_state.long_term_memory = get_long_term_memory()