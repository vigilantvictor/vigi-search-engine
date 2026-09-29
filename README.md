# 🔎 VigiSearch — Personal AI Search Engine

VigiSearch is a personal AI-powered web search engine built with **Python, FastAPI, HTML, CSS, and JavaScript**. It searches the web using **Tavily** and uses a **Groq-powered Large Language Model (LLM)** to analyze the retrieved sources and generate a clear, source-based answer.

## 🌐 Live Demo

**Try VigiSearch:**
https://vigi-search-engine.vigilant-v2006.workers.dev

## 📌 Project Overview

VigiSearch combines traditional web search with Large Language Model capabilities.

Instead of simply returning a list of search results, the application:

1. Accepts a user's search query.
2. Searches the web using Tavily.
3. Collects relevant sources.
4. Sends the sources and query to a Groq LLM.
5. Generates an AI-powered answer based on the retrieved sources.
6. Displays the answer along with the source information.
7. Stores search history locally using SQLite.

## ✨ Features

* 🔎 Web search using Tavily API
* 🤖 AI-powered answers using Groq LLM
* 📚 Source-based responses
* 🔗 Source URLs for further reading
* 🕒 Search history
* 🧹 Clear search history
* 🌐 Web-based user interface
* 💻 Command-line search interface
* ⚡ FastAPI backend
* 🔐 API keys stored using environment variables
* 🚀 Deployed and publicly accessible

## 🛠️ Technologies Used

### Backend

* Python
* FastAPI
* Uvicorn
* SQLite
* Requests

### Frontend

* HTML5
* CSS3
* JavaScript

### APIs & Services

* Tavily Search API
* Groq API
* Render
* Cloudflare

## 🏗️ Project Structure

```text
vigi-search-engine/
│
├── app/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── database.py
│   ├── llm.py
│   └── search.py
│
├── backend/
│   ├── __init__.py
│   ├── api.py
│   └── main.py
│
├── frontend/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── index.html
│
├── tests/
│   ├── __init__.py
│   └── test_database.py
│
├── data/
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ How It Works

```text
User
 │
 ▼
VigiSearch Frontend
 │
 ▼
FastAPI Backend
 │
 ├──────────────► Tavily Search API
 │                    │
 │                    ▼
 │               Web Sources
 │
 ▼
Groq LLM
 │
 ▼
AI-Generated Answer
 │
 ▼
User
```

## 🚀 Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/vigilantvictor/vigi-search-engine.git
cd vigi-search-engine
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root:

```env
TAVILY_API_KEY=your_tavily_api_key
GROQ_API_KEY=your_groq_api_key
```

Never commit your `.env` file to GitHub.

### 5. Start the backend

```bash
python -m uvicorn backend.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### 6. Start the frontend

Open another terminal:

```powershell
cd frontend
python -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500
```

## 🔑 Environment Variables

| Variable             | Description                            |
| -------------------- | -------------------------------------- |
| `TAVILY_API_KEY`     | API key used for web search            |
| `GROQ_API_KEY`       | API key used for LLM responses         |
| `LLM_MODEL`          | Groq model used for generating answers |
| `MAX_SEARCH_RESULTS` | Maximum number of search results       |
| `MAX_SOURCE_LENGTH`  | Maximum source content length          |

## 📡 API Endpoints

| Method   | Endpoint          | Description                              |
| -------- | ----------------- | ---------------------------------------- |
| `POST`   | `/api/search`     | Search the web and generate an AI answer |
| `POST`   | `/api/source/ask` | Ask a question about a specific source   |
| `GET`    | `/api/history`    | Retrieve search history                  |
| `DELETE` | `/api/history`    | Clear search history                     |
| `GET`    | `/health`         | Check backend health                     |

## 🔒 Security

API keys are loaded through environment variables and are not included in the frontend or source code.

The `.env` file is excluded from Git using `.gitignore`.

## 🚀 Deployment

The project is deployed using:

* **Render** — FastAPI backend
* **Cloudflare** — Frontend

### Live Website

https://vigi-search-engine.vigilant-v2006.workers.dev

## 🎯 Learning Objectives

This project was developed to gain practical experience with:

* Python application development
* REST API development
* FastAPI
* External API integration
* Large Language Models
* Prompt engineering
* Web search integration
* SQLite database operations
* Frontend and backend communication
* Environment variable management
* Git and GitHub
* Cloud deployment

## 👨‍💻 Author

**Vigilant**

Computer Science Student | Software Development & AI/ML Enthusiast

## ⭐ Acknowledgements

* Tavily for web search capabilities
* Groq for LLM inference
* FastAPI for backend API development
* Cloudflare for frontend hosting
* Render for backend deployment
