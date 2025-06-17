import time
from handlers import StreamHandler
from chains import multi_chain
from memory import should_update_summary


def handle_user_input(user_input, st):

    container = st.empty()
    handler = StreamHandler(container)
    chat_id = st.session_state.active_chat
    current_memory = st.session_state.chat_memories[chat_id]

    # Set memory and callback for chains
    multi_chain.memory = current_memory
    multi_chain.default_chain.memory = current_memory
    for chain in multi_chain.destination_chains.values():
        chain.memory = current_memory
        chain.llm.callbacks = [handler]
    multi_chain.default_chain.llm.callbacks = [handler]

    # Long-Term Memory
    try:
        ltm_summary = st.session_state.long_term_memory.load_memory_variables({})[
            "history"
        ]
    except Exception:
        ltm_summary = ""

    # Context from Uploaded file
    file_context_key = f"file_context_{chat_id}"
    if file_context_key in st.session_state:
        retriever = st.session_state[file_context_key]
        try:
            docs = retriever.invoke(user_input)
        except:
            docs = retriever.get_relevant_documents(user_input)
        file_context = "\n\n".join([doc.page_content for doc in docs])
    else:
        file_context = ""
        
    
    # Main RAG Invocation
    with st.spinner("Thinking..."):
        route_result = multi_chain.router_chain.invoke({"input": user_input})
        final_inputs = route_result["next_inputs"]
        final_inputs["ltm"] = ltm_summary
        final_inputs["history"] = current_memory.buffer_as_messages
        final_inputs["context"] = file_context
        
        destination = route_result["destination"]
        if destination in multi_chain.destination_chains:
            output = multi_chain.destination_chains[destination].invoke(final_inputs)
        else:
            output = multi_chain.default_chain.invoke(final_inputs)
        
        handler.text = output["text"]
        
    
    # Save to history
    history = st.session_state.chats[chat_id]
    history.append(("user", user_input))
    history.append(("assistant", handler.text.strip()))
    st.session_state.chats[chat_id] = history
    
    #Save to LTM if relevant
    if should_update_summary(user_input):
        try:
            st.session_state.long_term_memory.save_context(
                {"input" : user_input}, {"output" : handler.text.strip()}
            )
        except Exception:
            pass
    
    # st.empty().markdown(
    #     "<div style='text-align:center; padding:1rem; font-size:1rem; color:gray;'>✨ Preparing expert response...</div>",
    #     unsafe_allow_html=True,
    # )
    # time.sleep(1)
    st.rerun()