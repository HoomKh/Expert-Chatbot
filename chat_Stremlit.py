import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.callbacks.base import BaseCallbackHandler
import os
import streamlit as st
import time



# ========= Stream Handler ==========
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text + "▌")


# ========== Expert Prompts ==========
prompt_infos = prompt_infos = [
    {
        "name": "biology",
        "description": "Good for biology questions",
        "prompt_template": """You are a biology expert. Answer biology questions clearly and concisely.
    Here is a question:
{input}""",
    },
    {
        "name": "astronomy",
        "description": "Good for astronomy questions",
        "prompt_template": """You are an astronomy professor. Explain astronomy topics clearly.
Here is a question:
{input}""",
    },
    {
        "name": "economics",
        "description": "Good for economics questions",
        "prompt_template": """You are a skilled economist. Explain economic concepts with examples.
Here is a question:
{input}""",
    },
    {
        "name": "philosophy",
        "description": "Good for philosophy questions",
        "prompt_template": """You are a philosopher. Provide thoughtful answers to philosophical questions.
Here is a question:
{input}""",
    },
    {
        "name": "computer science",
        "description": "Good for computer science and programming questions",
        "prompt_template": """You are a computer scientist. You answer coding and algorithmic questions step-by-step, using clear logic and code when needed.
Here is a question:
{input}""",
    },
    {
        "name": "psychology",
        "description": "Good for psychology questions and mental behavior topics",
        "prompt_template": """You are a psychologist. Explain human behavior, cognitive processes, and mental health concepts with clarity and empathy.
Here is a question:
{input}""",
    },
    {
        "name": "history",
        "description": "Good for historical facts, events, and analysis",
        "prompt_template": """You are a historian. Provide fact-based historical context and insights into events, timelines, and civilizations.
Here is a question:
{input}""",
    },
    {
        "name": "literature",
        "description": "Good for literary analysis, authors, and genres",
        "prompt_template": """You are a literature expert. Analyze poems, novels, literary devices, and author intent with insight and elegance.
Here is a question:
{input}""",
    },
    {
        "name": "medicine",
        "description": "Good for medical questions and healthcare topics",
        "prompt_template": """You are a medical doctor. Explain diseases, treatments, and healthcare concepts with accuracy and clarity.
Here is a question:
{input}""",
    },
    {
        "name": "art",
        "description": "Good for art history, theory, and criticism",
        "prompt_template": """You are an art expert. Discuss artworks, styles, techniques, and famous artists thoughtfully and descriptively.
Here is a question:
{input}""",
    },
]


# ========== OpenAI Model ==========

router_llm = ChatOpenAI(
    temperature=0,
    model="gpt-4",
    streaming=False,
    openai_api_key="",
)

# Answering LLMs (streaming-enabled)
streaming_llm = ChatOpenAI(
    temperature=0,
    model="gpt-4",
    streaming=True,
    callbacks=[],
    openai_api_key="",
)

# ========== Destination Chains ==========
destination_chains = {}
for p in prompt_infos:
    prompt = ChatPromptTemplate.from_template(p["prompt_template"])
    chain = LLMChain(llm=streaming_llm, prompt=prompt)
    destination_chains[p["name"]] = chain

destination = [f"{p['name']} : {p['description']}" for p in prompt_infos]
destination_str = "\n".join(destination)

# ========== Default Chain ==========
default_prompt = ChatPromptTemplate.from_template("{input}")
default_chain = LLMChain(llm=streaming_llm, prompt=default_prompt)

# ========== Router Prompt ==========
# main prompt
MULTI_PROMPT_ROUTER_TEMPLATE = """Given a raw text input to a \
language model select the model prompt best suited for the input. \
You will be given the names of the available prompts and a \
description of what the prompt is best suited for. \
You may also revise the original input if you think that revising\
it will ultimately lead to a better response from the language model.

<< FORMATTING >>
Return a markdown code snippet with a JSON object formatted to look like:
```json
{{{{
    "destination": string \ "DEFAULT" or name of the prompt to use in {destinations}
    "next_inputs": string \ a potentially modified version of the original input
}}}}
```

REMEMBER: The value of “destination” MUST match one of \
the candidate prompts listed below.\
If “destination” does not fit any of the specified prompts, set it to “DEFAULT.”
REMEMBER: "next_inputs" can just be the original input \
if you don't think any modifications are needed.

<< CANDIDATE PROMPTS >>
{destinations}

<< INPUT >>
{{input}}

<< OUTPUT (remember to include the ```json)>>"""

router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destination_str)

router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"],
    output_parser=RouterOutputParser(),
)

router_chain = LLMRouterChain.from_llm(llm=router_llm, prompt=router_prompt)

# ========== Final MultiPromptChain ==========
multi_chain = MultiPromptChain(
    router_chain=router_chain,
    destination_chains=destination_chains,
    default_chain=default_chain,
    verbose=True,
)

# ========== Streamlit UI ==========
st.set_page_config(page_title="Expert Chatbot", page_icon="🧠")
st.title("🧠 Expert Chatbot")
st.caption("Ask anything — the bot will route your question to the most suitable expert domain.")

st.markdown(
    """
    <style>
    .fade-in {
        animation: fadeIn 1.5s ease-in;
    }
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .expert-label {
        color:
        font-size: 0.85rem;
        margin-bottom: 0.2rem;
    }
    .user-question {
        text-align: center;
        font-weight: bold;
        font-size: 1.05rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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


    for chain in list(destination_chains.values()) + [default_chain]:
        chain.llm.callbacks = [handler]

    with st.spinner("Thinking..."):
        _ = multi_chain.run(user_input)

    container.empty() 


    blur_msg = st.empty()
    blur_msg.markdown(
        "<div style='text-align:center; padding:1rem; font-size:1rem; color:gray;'>✨ Preparing expert response...</div>",
        unsafe_allow_html=True
    )
    time.sleep(2)
    blur_msg.empty()


    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("assistant", f"\n{handler.text.strip()}"))

for sender, msg in st.session_state.chat_history:
    with st.chat_message(sender):
        if sender == "user":
            st.markdown(f"<div class='fade-in user-question'>{msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='fade-in'>{msg}</div>", unsafe_allow_html=True)

