## 🚀 Live Demo

👉 [Open HelpDesk AI](https://cheerful-lollipop-1e7867.netlify.app/)

# HelpDesk AI

AI-powered IT Helpdesk Agent that analyzes technical problems, runs diagnostic checks, retrieves relevant troubleshooting knowledge, generates evidence-aware responses, and creates support tickets when escalation is required.

## Features

- AI-powered IT troubleshooting
- Local Qwen 2.5 7B through Ollama
- Semantic knowledge retrieval
- Local troubleshooting knowledge base
- Automated internet, network, and system diagnostics
- Evidence-aware AI responses
- Automatic issue categorization
- Automatic escalation
- SQLite support tickets
- React dashboard
- REST API
- Fully local AI inference

## Architecture

```text
User
  |
  v
React + Vite Frontend
  |
  v
FastAPI REST API
  |
  v
HelpDesk AI Agent
  |
  +-- Issue Classification
  |
  +-- Diagnostic Tools
  |     +-- Internet Check
  |     +-- Network Check
  |     +-- System Check
  |
  +-- Knowledge Retrieval
  |     +-- Local Knowledge Base
  |     +-- Embeddings
  |     +-- Similarity Search
  |
  +-- Qwen 2.5 7B
  |
  +-- Escalation Engine
          |
          v
      SQLite Tickets
