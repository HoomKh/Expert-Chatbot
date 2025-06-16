import streamlit as st
import time
from chains import multi_chain
from handlers import StreamHandler
from memory import (
    should_update_summary,
    get_short_term_memory,
    get_long_term_memory,
)

st.set_page_config(page_title="Expert Chatbot", page_icon="🧠")

# -------------------- Session State Init --------------------
def initialize_session():
    if "chats" not in st.session_state:
        st.session_state.chats = {"Chat 1": []}
    if "active_chat" not in st.session_state:
        st.session_state.active_chat = "Chat 1"
    if "chat_memories" not in st.session_state:
        st.session_state.chat_memories = {"Chat 1": get_short_term_memory()}
    if "long_term_memory" not in st.session_state:
        st.session_state.long_term_memory = get_long_term_memory()

# -------------------- Sidebar Layout --------------------
def render_sidebar():
    st.sidebar.markdown("""
        <style>
        .sidebar-title { font-size: 1.3rem; font-weight: 700; margin-bottom: 1.5rem; }
        .sidebar-btn { background-color: transparent; color: #e1e1e1; border: none; width: 100%; text-align: left; padding: 0.6rem 1rem; border-radius: 8px; margin-bottom: 0.25rem; font-size: 0.95rem; transition: background 0.2s; }
        .sidebar-btn:hover { background-color: #333; }
        .sidebar-btn.active { background-color: #4c4cff; font-weight: bold; color: white; }
        .sidebar-controls { display: flex; gap: 0.5rem; margin-top: 1rem; }
        .sidebar-controls button { width: 100%; padding: 0.4rem; border-radius: 6px; font-size: 0.85rem; border: none; background-color: #2b2b2f; color: white; }
        .sidebar-controls button:hover { background-color: #444; }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("<div class='sidebar-title'>💬 Your Chats</div>", unsafe_allow_html=True)

    for name in st.session_state.chats:
        btn_class = "sidebar-btn active" if name == st.session_state.active_chat else "sidebar-btn"
        if st.sidebar.button(name, key=f"chat-{name}"):
            st.session_state.active_chat = name
            st.rerun()

    col1, col2 = st.sidebar.columns(2)
    if col1.button("➕", help="New Chat"):
        new_name = f"Chat {len(st.session_state.chats) + 1}"
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
                new_name = "Chat 1"
                st.session_state.chats[new_name] = []
                st.session_state.chat_memories[new_name] = get_short_term_memory()
                st.session_state.active_chat = new_name
            st.rerun()

# -------------------- Chat Logic --------------------
def handle_user_input(user_input):
    container = st.empty()
    handler = StreamHandler(container)
    current_memory = st.session_state.chat_memories[st.session_state.active_chat]

    multi_chain.memory = current_memory
    multi_chain.default_chain.memory = current_memory
    for chain in multi_chain.destination_chains.values():
        chain.memory = current_memory
        chain.llm.callbacks = [handler]
    multi_chain.default_chain.llm.callbacks = [handler]

    try:
        ltm_summary = st.session_state.long_term_memory.load_memory_variables({})["history"]
    except Exception:
        ltm_summary = ""

    with st.spinner("Thinking..."):
        route_result = multi_chain.router_chain.invoke({"input": user_input})
        final_inputs = route_result["next_inputs"]
        final_inputs["ltm"] = ltm_summary
        final_inputs["history"] = current_memory.buffer_as_messages

        destination = route_result["destination"]
        if destination in multi_chain.destination_chains:
            output = multi_chain.destination_chains[destination].invoke(final_inputs)
        else:
            output = multi_chain.default_chain.invoke(final_inputs)

        handler.text = output["text"]

    container.empty()

    history = st.session_state.chats[st.session_state.active_chat]
    history.append(("user", user_input))
    history.append(("assistant", handler.text.strip()))
    st.session_state.chats[st.session_state.active_chat] = history

    if should_update_summary(user_input):
        try:
            st.session_state.long_term_memory.save_context(
                {"input": user_input}, {"output": handler.text.strip()}
            )
        except Exception:
            pass

    st.empty().markdown(
        "<div style='text-align:center; padding:1rem; font-size:1rem; color:gray;'>✨ Preparing expert response...</div>",
        unsafe_allow_html=True,
    )
    time.sleep(1)

# -------------------- Main UI --------------------
def render_chat():
    history = st.session_state.chats.get(st.session_state.active_chat, [])
    user_input = st.chat_input("Type your message here...")
    if user_input:
        handle_user_input(user_input)

    if not history:
        st.markdown("""
        <div style='text-align: center; padding: 5rem 1rem; opacity: 0.6;'>
            <h1 style='font-weight: 400;'>👋 Welcome to Expert Chatbot</h1>
            <p style='font-size: 1.1rem;'>Start a conversation using the input box below.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for sender, msg in history:
            with st.chat_message(sender):
                st.markdown(msg, unsafe_allow_html=False)

# -------------------- CSS --------------------
def inject_css():
    st.markdown("""
    <style>
    .chat-message { background-color: #2b2b2f; padding: 1rem; border-radius: 12px; margin-bottom: 0.5rem; font-size: 0.95rem; }
    .chat-message.user { background-color: #4c4cff; color: white; text-align: right; }
    .chat-message.assistant { background-color: #3a3a3a; color: white; }
    .fade-in { animation: fadeIn 0.6s ease-in-out; }
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    input[type="text"] {
        background-color: #1f1f22 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# -------------------- Run App --------------------
def main():
    initialize_session()
    inject_css()
    render_sidebar()
    render_chat()

if __name__ == "__main__":
    main()
