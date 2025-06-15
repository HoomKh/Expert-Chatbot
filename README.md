# 🧠 Expert Chatbot

A smart, multi-domain chatbot built with **LangChain**, **OpenAI GPT-4**, and **Streamlit**.  
It intelligently routes your question to the right expert — whether it's philosophy, biology, programming, or economics.

![LangChain](https://img.shields.io/badge/langchain-v0.1.17-blue)
![Streamlit](https://img.shields.io/badge/streamlit-%F0%9F%A7%A1-red)
![OpenAI](https://img.shields.io/badge/openai-GPT4-green)

---

## 🌟 Features

- ✅ AI Expert Routing using LangChain
- ✅ Support for 10+ knowledge domains
- ✅ Fast response with OpenAI GPT-4
- ✅ Real-time token streaming (via StreamHandler)
- ✅ Interactive Streamlit UI with chat history
- ✅ Secure API Key via `.env` file
- ✅ Fully modular and maintainable codebase

---

## 🏗️ Architecture

```text
expert_chatbot/
├── app.py              # Streamlit UI
├── chains.py           # LangChain Router & Expert Chains
├── handlers.py         # Streaming Token Handler
├── prompt.py           # Expert prompt templates
├── .env                # API key (do not commit!)
├── .gitignore
├── requirements.txt
└── README.md
````

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/Hoom-KH/expert_chatbot.git
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

Then open your browser to: [http://localhost:8501](http://localhost:8501)

---

## 💬 Supported Domains

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

| Layer          | Tech Used                  |
| -------------- | -------------------------- |
| Frontend       | Streamlit                  |
| LLM Backbone   | OpenAI GPT-4               |
| Routing Engine | LangChain (RouterRunnable) |
| Env Handling   | python-dotenv              |

---

## 🔐 Security Note

To protect your API key:

* Store it in a `.env` file (never hardcode it).
* Add `.env` to your `.gitignore` to avoid exposing it publicly.

```gitignore
.env
__pycache__/
```

---

## 🙌 Contributions

Pull requests are welcome. For major changes, please open an issue first to discuss your ideas.

---

## 📄 License

MIT © [Hoom\_KH](https://github.com/Hoom-KH)

---

> Made with ❤️ using GPT-4, LangChain, and Streamlit

