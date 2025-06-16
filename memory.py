from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

import os
from dotenv import load_dotenv

# ////////////Load .env///////////
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


# ////////////Short Term Memory///////////
def get_short_term_memory():
    return ConversationBufferWindowMemory(k=5, return_messages=True, output_key="text", input_key="input")


# ////////////Long Term Memory///////////
def get_long_term_memory():
    return ConversationSummaryMemory(
        llm=ChatOpenAI(temperature=0, openai_api_key=api_key), return_messages=True
    )


# ////////////Classify Update Long Term Memory///////////
def should_update_summary(user_input: str) -> bool:
    if user_input.strip().endswith("?"):
        return False 

    keywords = ["name", "live", "from", "like", "work", "study", "age", "old", "job", "family", "i am", "i'm", "my"]
    if not any(k in user_input.lower() for k in keywords):
        return False  

    chat = ChatOpenAI(temperature=0, openai_api_key=api_key)
    message = HumanMessage(content=f"""
You are a memory filter AI. If the following input contains long-term useful personal info (name, location, goals...), reply with Yes. Otherwise, reply No.

Input: "{user_input}"

Only answer Yes or No.
""")
    result = chat.invoke([message])
    print("[LTM Check Result]", result.content)
    return "yes" in result.content.lower()





