import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.callbacks.base import BaseCallbackHandler
import os
from dotenv import load_dotenv
import streamlit as st
import time

from prompt import prompt_infos, MULTI_PROMPT_ROUTER_TEMPLATE
from handlers import StreamHandler

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ///////////OpenAI Model Init///////////
router_llm = ChatOpenAI(
    temperature=0,
    model="gpt-4",
    streaming=False,
    openai_api_key=api_key,
)


streaming_llm = ChatOpenAI(
    temperature=0,
    model="gpt-4",
    streaming=True,
    callbacks=[],
    openai_api_key=api_key,
)

# ///////////Destination Chains///////////
destination_chains = {}
for p in prompt_infos:
    prompt = ChatPromptTemplate.from_template(p["prompt_template"])
    chain = LLMChain(llm=streaming_llm, prompt=prompt)
    destination_chains[p["name"]] = chain

destination = [f"{p['name']} : {p['description']}" for p in prompt_infos]
destination_str = "\n".join(destination)

# ///////////Default Chain///////////
default_prompt = ChatPromptTemplate.from_template("{input}")
default_chain = LLMChain(llm=streaming_llm, prompt=default_prompt)

# ///////////Router Chain///////////
router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destination_str)

router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"],
    output_parser=RouterOutputParser(),
)

router_chain = LLMRouterChain.from_llm(llm=router_llm, prompt=router_prompt)

# ///////////Final MultiPromptChain///////////
multi_chain = MultiPromptChain(
    router_chain=router_chain,
    destination_chains=destination_chains,
    default_chain=default_chain,
    verbose=True,
)