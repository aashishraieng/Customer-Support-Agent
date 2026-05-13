# AI WhatsApp Banking Support Agent

## Overview
An AI-powered banking support chatbot built using FastAPI, Gemini AI, n8n, WhatsApp Cloud API, and SQLite.

The system supports:
- balance inquiry
- transaction history
- card blocking
- human support escalation
- OTP authentication
- session timeout handling

Users interact through WhatsApp while n8n orchestrates webhook automation and FastAPI handles AI/business logic.

---

## Features

- WhatsApp chatbot integration
- Gemini AI intent classification
- Stateful conversation management
- OTP-based authentication
- Session timeout security
- Card block workflow
- Human handoff support
- SQLite session persistence
- n8n workflow automation

---

## Tech Stack

### Backend
- FastAPI
- Python
- SQLite

### AI
- Gemini 2.5 Flash

### Automation
- n8n
- WhatsApp Cloud API
- ngrok

---

## Project Architecture

WhatsApp User
↓
Meta WhatsApp Cloud API
↓
n8n Webhook
↓
FastAPI Backend
↓
Gemini Intent Classifier
↓
Business Logic / Session Handling
↓
n8n Response Workflow
↓
WhatsApp Reply

---

## Project Structure

```text
bank-support-agent/
│
├── main.py                # Main FastAPI application, defines endpoints and orchestrates the chatbot logic
├── intent_classifier.py   # Uses Gemini API to classify user intents (e.g., balance inquiry, card block)
├── session_store.py       # Manages user sessions, authentication state, and timeouts
├── database.py            # SQLite database initialization and session table creation
├── tools.py               # Mock banking functions (e.g., fetching balance, transaction history)
├── requirements.txt       # Python project dependencies
├── .env                   # Environment variables (e.g., GEMINI_API_KEY)
├── .gitignore             # Specifies intentionally untracked files that Git should ignore
└── bank.db                # SQLite database file storing active sessions
```

---

## Setup Instructions

### 1. Clone repository

```bash
git clone <repo_url>
cd bank-support-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create .env

```env
GEMINI_API_KEY=your_api_key
```

### 4. Run FastAPI

```bash
uvicorn main:app --reload
```

### 5. Run ngrok

```bash
ngrok http 5678
```

### 6. Start n8n workflow

Activate webhook workflows in n8n.

---

## Example Queries

- "How much money do I have?"
- "Show my transactions"
- "Block my card"
- "Talk to human"

---

## Current Limitations

- Demo OTP only
- No real banking integration
- Static user mapping
- Basic FAQ support

---

## Future Improvements

- Real OTP service
- PostgreSQL database
- Docker deployment
- RAG-based FAQ system
- Money transfer workflow
- Admin dashboard
- JWT authentication