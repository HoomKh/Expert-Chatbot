#expert prompt
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


# main router prompt
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