# 🤖 HelpDesk AI

### AI-Powered IT Helpdesk Agent

**HelpDesk AI** is an intelligent IT support agent that understands technical problems, performs system diagnostics, retrieves relevant troubleshooting knowledge, generates evidence-aware responses, and automatically escalates unresolved issues by creating support tickets.

## 🚀 Live Demo

### 👉 [Open HelpDesk AI](https://helpdesk-ai-pearl.vercel.app/)

> **Demo note:** The frontend is publicly hosted on Vercel. The AI inference backend runs locally using FastAPI and Ollama and is exposed securely for demonstration through an HTTPS tunnel.

---

## 🎯 Problem Statement

Traditional IT helpdesks often depend on manual ticket creation and repetitive troubleshooting.

HelpDesk AI automates the first level of IT support by:

* Understanding the user's technical problem
* Categorizing the issue automatically
* Running relevant diagnostic checks
* Searching a troubleshooting knowledge base
* Generating an AI-assisted solution
* Detecting unresolved or critical issues
* Automatically creating an IT support ticket

This reduces repetitive support work and provides users with faster initial assistance.

---

## ✨ Key Features

### 🧠 AI IT Troubleshooting

Uses **Qwen 2.5 7B** through Ollama to understand user problems and generate troubleshooting guidance.

### 🔍 Intelligent Diagnostics

Automatically runs relevant diagnostic tools, including:

* Internet connectivity check
* Network availability check
* Local system information check

### 📚 Knowledge Retrieval

Retrieves relevant troubleshooting information from a local knowledge base using semantic similarity search.

Current knowledge areas include:

* Wi-Fi
* Internet connectivity
* Printers
* Bluetooth
* Windows
* Software issues

### 🏷️ Automatic Issue Classification

Problems are automatically categorized into areas such as:

* Network
* Printer
* Bluetooth
* Software
* System
* General

### 🚨 Automatic Escalation

When an issue cannot be resolved or the user indicates that they have already attempted troubleshooting, HelpDesk AI can automatically escalate the issue.

Example:

> "My Wi-Fi is still not working. I already tried everything and I cannot work."

The system can recognize the escalation condition and create a support ticket.

### 🎫 IT Support Tickets

Escalated issues are stored as support tickets using SQLite.

Each ticket contains information such as:

* Ticket ID
* Problem description
* Category
* Priority
* Status
* Creation time

### 📊 Web Dashboard

The React dashboard provides dedicated views for:

* Dashboard
* AI Assistant
* Tickets
* Diagnostics
* Knowledge Base

---

## 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │       User          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ React + Vite        │
                         │ Web Frontend        │
                         └──────────┬──────────┘
                                    │ HTTPS
                                    ▼
                         ┌─────────────────────┐
                         │ FastAPI REST API    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │      HelpDesk AI Agent       │
                    └──────────────┬───────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
      ┌──────────────┐     ┌───────────────┐    ┌──────────────┐
      │ Issue        │     │ Diagnostics   │    │ Knowledge    │
      │ Classification│    │ Engine        │    │ Retrieval    │
      └──────────────┘     └───────────────┘    └──────┬───────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │ Semantic Search │
                                              │ + Embeddings    │
                                              └────────┬────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │ Qwen 2.5 7B     │
                                              │ via Ollama      │
                                              └────────┬────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │ AI Response     │
                                              └────────┬────────┘
                                                       │
                                      ┌────────────────┴──────────────┐
                                      │                               │
                                      ▼                               ▼
                              ┌──────────────┐                ┌──────────────┐
                              │ Resolution   │                │ Escalation   │
                              │ Guidance     │                │ Engine       │
                              └──────────────┘                └──────┬───────┘
                                                                      │
                                                                      ▼
                                                              ┌──────────────┐
                                                              │ SQLite       │
                                                              │ Tickets      │
                                                              └──────────────┘
```

---

## 🛠️ Technology Stack

| Layer           | Technology              |
| --------------- | ----------------------- |
| Frontend        | React                   |
| Build Tool      | Vite                    |
| Styling         | CSS                     |
| Backend         | Python                  |
| API Framework   | FastAPI                 |
| AI Model        | Qwen 2.5 7B             |
| AI Runtime      | Ollama                  |
| Embeddings      | nomic-embed-text        |
| Retrieval       | NumPy cosine similarity |
| Knowledge Base  | Markdown                |
| Database        | SQLite                  |
| API Style       | REST                    |
| Deployment      | Vercel + HTTPS tunnel   |
| Version Control | Git + GitHub            |

---

## 📁 Project Structure

```text
helpdesk-ai/
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── ...
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   ├── ai/
│   │   ├── db/
│   │   ├── rag/
│   │   ├── tickets/
│   │   └── tools/
│   │
│   ├── knowledge_base/
│   │   ├── wifi.md
│   │   ├── internet.md
│   │   ├── printer.md
│   │   ├── bluetooth.md
│   │   ├── windows.md
│   │   └── software.md
│   │
│   ├── requirements.txt
│   └── .python-version
│
├── .gitignore
└── README.md
```

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/john20-bit/helpdesk-ai.git
cd helpdesk-ai
```

### 2. Start the backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Start FastAPI:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3. Start Ollama

Make sure Ollama is installed and running.

Pull the required models:

```bash
ollama pull qwen2.5:7b
ollama pull nomic-embed-text
```

### 4. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

---

## 🌐 Demo Deployment

The public frontend is deployed using **Vercel**.

### Frontend

```text
https://helpdesk-ai-pearl.vercel.app/
```

### Backend

For the current demonstration architecture, the FastAPI backend runs locally and is exposed through an HTTPS tunnel.

```text
Vercel
   ↓
HTTPS
   ↓
Tunnel
   ↓
FastAPI
   ↓
Ollama
   ↓
Qwen 2.5 7B
```

This allows the public frontend to communicate with the locally running AI inference system during the demonstration.

---

## 🧪 Example Use Cases

### Network Troubleshooting

**User:**

```text
My Wi-Fi is connected but I cannot access the internet.
```

**HelpDesk AI:**

1. Identifies the issue as a Network problem
2. Runs connectivity diagnostics
3. Retrieves relevant Wi-Fi and internet troubleshooting knowledge
4. Sends the evidence and context to the AI model
5. Generates troubleshooting guidance

---

### Automatic Escalation

**User:**

```text
My Wi-Fi is still not working. I already tried everything and I cannot work.
```

HelpDesk AI can:

```text
Detect unresolved issue
        ↓
Trigger escalation
        ↓
Assign priority
        ↓
Create support ticket
        ↓
Return ticket information
```

Example ticket:

```text
Ticket ID: HD-XXXX
Category: Network
Priority: High
Status: Open
```

---

## 🔐 Design Principles

HelpDesk AI follows an evidence-oriented approach:

* Diagnostic tools provide real system information
* Knowledge retrieval provides relevant troubleshooting context
* The AI model uses the retrieved information when generating responses
* Escalation is triggered when automated troubleshooting is insufficient
* Support tickets preserve unresolved issues for further action

---

## 📌 Project Highlights

* 🤖 AI-powered IT support
* 🔍 Automated diagnostics
* 📚 Semantic knowledge retrieval
* 🧠 Local LLM inference
* 🎫 Automatic ticket creation
* 🚨 Intelligent escalation
* 🌐 Public web interface
* 🔌 REST API architecture
* 💾 Persistent SQLite ticket storage
* 🖥️ Responsive React dashboard

---

## 👨‍💻 Project

**HelpDesk AI**

AI-powered IT Helpdesk Agent for intelligent first-level technical support.

### Repository

[GitHub Repository](https://github.com/john20-bit/helpdesk-ai)

### Live Demo

https://helpdesk-ai-pearl.vercel.app/

---

## 📄 License

This project is developed for educational and demonstration purposes.
