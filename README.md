# LangGraph ChatBot with Multi-Thread Support

A **multi-thread chatbot** built with **LangGraph**, **LangChain**, and **Streamlit**.  
Supports multiple conversations with persistent memory stored in SQLite, streaming AI responses, and programmatic thread management.

---

## Features

- Multi-thread conversations (each thread has its own memory)
- Persistent memory using SQLite
- Streamed AI responses
- Sidebar for switching between conversations
- Fully backend-compatible for programmatic thread creation
- Powered by GPT-4 via LangChain

---

## Tech Stack

- **Python 3.10+**
- **Streamlit** → Frontend UI
- **LangGraph** → Agentic framework
- **LangChain** → LLM integration
- **SQLite** → Persistence backend
- **dotenv** → Environment variable management

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Uttam-5049/langgraph-chatbot.git
cd langgraph-chatbot
```

2. Create a virtual environment and activate it:

```bash
python -m venv myenv
venv\Scripts\activate     
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key
```

---

## Project Structure

```
.
├── frontend.py           # Streamlit frontend
├── backend.py            # LangGraph agent & thread management
├── chatbot.db            # SQLite DB (auto-generated)
├── requirements.txt      # Python dependencies
└── README.md
```

---

## Usage

### 1. Running the Streamlit App

```bash
streamlit run frontend.py
```

- Click **New Chat** in the sidebar to create a new conversation thread.
- Click existing thread IDs to load previous conversations.
- Type your messages in the chat input and see AI responses streamed live.

---

### 2. Backend Thread Management

You can create a new thread entirely in the backend:

```pythond
from langchain_core.messages import HumanMessage


# Configure LangGraph to use this thread
CONFIG = {'configurable': {'thread_id': 'thread_1'}}

# Send initial message
initial_message = HumanMessage(content="Hello, new thread!")
response = agent.invoke({"messages": [initial_message]}, config=CONFIG)

# Access AI response
print(response['messages'][0].content)
```
- Each thread is independent and persists in SQLite

---

## Key Functions

- `random_id()` → Generates a unique thread ID
- `reset_chat()` → Starts a new chat from the Streamlit UI
- `add_thread(thread_id)` → Adds a thread to sidebar
- `load_thread()` → Loads all saved thread IDs from the database
- `load_conversation(thread_id)` → Loads messages for a given thread

---

## Database

- **SQLite** used for persistence (`chatbot.db`)
- **SqliteSaver** in LangGraph handles checkpointing
- Each `thread_id` corresponds to one conversation state

---

## Configuration

All configuration is passed via **CONFIG**:

```python
CONFIG = {'configurable': {'thread_id': 'thread-1'}}
```

- `thread_id` identifies which conversation to load/save
- Ensures multi-thread persistence

---

- [Streamlit Docs](https://docs.streamlit.io/)

