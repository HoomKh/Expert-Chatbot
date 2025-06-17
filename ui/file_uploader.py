import streamlit as st
from vectorstore.file_indexing import load_and_index_uploaded_file

def render_file_upload_popup():
    chat_id = st.session_state.active_chat

    with st.popover("📎", use_container_width=True):
        st.markdown("#### Upload PDF")
        uploaded_file = st.file_uploader(label="#", type=["pdf"], key=f"upload-btn-{chat_id}")
        if uploaded_file:
            safe_collection_name = f"user_doc_{chat_id}".replace(" ", "_")
            with st.spinner("📄 Indexing..."):
                retriever = load_and_index_uploaded_file(uploaded_file, collection_name=safe_collection_name)
                st.session_state[f"file_context_{chat_id}"] = retriever
                st.success("✅ File ready!")