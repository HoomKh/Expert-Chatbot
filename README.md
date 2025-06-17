# 🧠 Expert Chatbot

A smart, memory-enabled multi-domain chatbot powered by **LangChain**, **OpenAI GPT-4**, and **Streamlit**. It dynamically routes your query to the most suitable expert, keeps track of the conversation with short- and long-term memory, and now supports **document-based Q\&A** using **PDF/DOCX uploads** — making it ideal for intelligent document analysis and contextual question answering.

![LangChain](https://img.shields.io/badge/langchain-v0.1.17-blue)
![Streamlit](https://img.shields.io/badge/streamlit-%F0%9F%A7%A1-red)
![OpenAI](https://img.shields.io/badge/openai-GPT4-green)

---

## 🌟 Features

* ✅ **Multi-Expert Routing** with LangChain `MultiPromptChain`
* ✅ **10+ Expert Domains** (biology, CS, medicine, etc.)
* ✅ **File-aware Q\&A** with document upload (PDF & DOCX)
* ✅ **Per-Chat File Context** (each chat only sees its own file)
* ✅ **Real-time Token Streaming** via custom `StreamHandler`
* ✅ **Short-term Memory** per session (`ConversationBufferWindowMemory`)
* ✅ **Long-term Memory** for personal facts (`ConversationSummaryMemory`)
* ✅ **LTM Classifier** to selectively store only meaningful information
* ✅ **Context Preview**: displays exact file text used to answer each query
* ✅ **Persistent Multi-Chat History** per user session
* ✅ **Modular Refactored Codebase** with clean separation of UI, logic, memory, and chains
* ✅ **Secure OpenAI API Handling** via `.env`

---

## 🧠 Architecture Overview

```text
expert_chatbot/
├── app.py                # Streamlit App Entry Point
├── chains.py             # LangChain router and expert chains
├── chat_handler.py       # Handles message flow, context prep, memory ops
├── chat_display.py       # Chat message rendering logic
├── handlers.py           # Streaming token handler
├── memory.py             # Memory setup + meaningful memory filter
├── prompt.py             # Prompt templates for each expert domain
├── sidebar.py            # Dynamic chat list and controls
├── session.py            # Streamlit session state management
├── file_uploader.py      # File upload logic (PDF/DOCX)
├── vectorstore/
│   └── file_indexing.py  # Milvus-based document embedding and retrieval
├── requirements.txt
└── .env                  # API keys (excluded via .gitignore)
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/HoomKH/expert_chatbot.git
cd expert_chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

```env
OPENAI_API_KEY=your_openai_key_here
```

### 4. Run the App

```bash
streamlit run app.py
```

Then open: [http://localhost:8501](http://localhost:8501)

---

## 📎 Document Q\&A

You can upload a PDF or DOCX file inside each chat. That file becomes the **contextual knowledge** for that specific conversation — all answers will only consider **that file**, not others.

> 🔒 Each chat sees only its own document. Embeddings are chat-scoped, not global.

---

## 💬 Supported Expert Domains

* 🧬 Biology
* 🪐 Astronomy
* 💰 Economics
* 🧠 Psychology
* 📜 Philosophy
* 💾 Computer Science
* 🩺 Medicine
* 🎨 Art
* 📚 Literature
* 📖 History

---

## 🧪 Tech Stack

| Layer               | Technology                      |
| ------------------- | ------------------------------- |
| Frontend UI         | Streamlit                       |
| LLM Backbone        | OpenAI GPT-4                    |
| Chain Orchestration | LangChain (MultiPromptChain)    |
| Memory System       | LangChain Memory (short & long) |
| Vector Storage      | Milvus                          |
| Doc Parsing         | PyMuPDF / docx2txt              |
| API Handling        | python-dotenv                   |

---

## 🔐 Security Notes

* Your `.env` file stores API keys securely
* Make sure to **never push `.env`** to GitHub — it's already in `.gitignore`

```gitignore
.env
__pycache__/
```

---

## 🙌 Contributions

Have a new expert domain or feature idea? PRs and issues are welcome.

---

## 📄 License

MIT © [HoomKH](https://github.com/HoomKH)

---

> Built with ❤️ using LangChain, GPT-4, Streamlit, and lots of contextual intelligence.
