# 🧠 Expert Chatbot

A smart, memory-enabled multi-domain chatbot built with **LangChain**, **OpenAI GPT-4**, and **Streamlit**. 
It routes your question to the most relevant expert (e.g., biology, CS, medicine), keeps track of your conversation context with short-term memory, and remembers personal details using long-term memory — like your name, goals, or preferences.

![LangChain](https://img.shields.io/badge/langchain-v0.1.17-blue)
![Streamlit](https://img.shields.io/badge/streamlit-%F0%9F%A7%A1-red)
![OpenAI](https://img.shields.io/badge/openai-GPT4-green)

---

## 🌟 Features

- ✅ Multi-Expert Routing using LangChain
- ✅ Support for 10+ specialized knowledge domains
- ✅ Real-time token streaming via StreamHandler
- ✅ Short-term memory per chat (ConversationBufferMemory)
- ✅ Long-term memory across chats (ConversationSummaryMemory)
- ✅ Memory filter to store only meaningful info (e.g. name, job)
- ✅ Interactive Streamlit UI with chat history per session
- ✅ Secure API key loading via `.env`
- ✅ Modular, readable, and maintainable architecture

---

## 🏗️ Architecture

```text
expert_chatbot/
├── app.py              # Main Streamlit UI (refactored)
├── chains.py           # LangChain Router & Expert Chains
├── handlers.py         # Token streaming handler
├── memory.py           # Memory setup & LTM classifier
├── prompt.py           # Expert and default prompt templates
├── .env                # Your OpenAI API key (excluded)
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/HoomKH/expert_chatbot.git
cd expert_chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your `.env` file

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Run the app

```bash
streamlit run app.py
```

Then visit: [http://localhost:8501](http://localhost:8501)

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

| Layer            | Technology                     |
|------------------|---------------------------------|
| Frontend         | Streamlit                      |
| LLM Backbone     | OpenAI GPT-4                   |
| Routing Engine   | LangChain (MultiPromptChain)   |
| Memory System    | LangChain Memory (short + long)|
| Env Handling     | python-dotenv                  |

---

## 🔐 Security Note

* Use `.env` to load your API key securely
* Never commit `.env` to GitHub (it's in `.gitignore`)

```gitignore
.env
__pycache__/
```

---

## 🙌 Contributions

Pull requests are welcome. For major changes, open an issue first to discuss your idea.

---

## 📄 License

MIT © [HoomKH](https://github.com/HoomKH)

---

> Built with ❤️ using LangChain, GPT-4, and Streamlit
