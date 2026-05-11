# AI Career Assistant

An AI-powered career preparation platform built using:

- Streamlit (Frontend)
- FastAPI (Backend)
- Ollama / Gemma Models
- SQLite
- Python

This application helps users:
- Track job applications
- Generate interview questions
- Chat with a study mentor
- Build learning roadmaps
- Analyze resumes using AI

---

# Features

## 1. Applications Dashboard

Users can:
- Save job applications
- View saved jobs
- View Job Descriptions (JD)
- Delete one or multiple job applications

Stored data includes:
- Company
- Role
- Skills
- Status
- JD

---

## 2. Interview Question Chatbot

AI-powered interview simulator that:
- Uses saved job skills
- Generates role-specific interview questions
- Supports conversational interview prep
- Maintains chat history

---

## 3. Study Mentor

Interactive AI study mentor that:
- Answers roadmap questions
- Explains concepts
- Suggests learning strategies
- Helps with revision planning

---

## 4. Roadmap Generator

Generates:
- 7-day learning roadmaps
- Daily study plans
- Revision schedules
- Interview preparation plans

Based on:
- Job role
- Extracted skills

---

## 5. Resume Suggestions

AI-powered resume analysis including:

- Skills to Add
- ATS Keyword Analysis
- Project Suggestions
- Resume Bullet Improvements
- Resume Scoring
- Experience Gap Suggestions
- Hiring Readiness Analysis

Supports:
- PDF resumes
- TXT resumes
- Markdown resumes

---

# Tech Stack

## Frontend
- Streamlit

## Backend
- FastAPI
- Uvicorn

## Database
- SQLite
- SQLAlchemy

## AI
- Ollama
- Gemma Models

---

# Project Structure

```bash
ai-career-assistant/
│
├── backend/
│   ├── main.py
│   ├── services/
│   ├── database/
│   └── models/
│
├── frontend/
│   └── app.py
│
└── README.md
```

---

# Installation

## 1. Clone the Repository

```bash
git clone <repo-url>
cd ai-career-assistant
```

---

## 2. Backend Setup

```bash
cd backend

python -m venv venv

source venv/bin/activate
```

Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy requests
```

Run backend:

```bash
uvicorn main:app --reload
```

Backend runs on:

```bash
http://127.0.0.1:8000
```

---

## 3. Frontend Setup

```bash
cd frontend
```

Install dependencies:

```bash
pip install streamlit pandas requests PyPDF2
```

Run frontend:

```bash
streamlit run app.py
```

Frontend runs on:

```bash
http://localhost:8501
```

---

# API Endpoints

## Extract Skills

```http
POST /extract-skills
```

---

## Generate Interview Questions

```http
POST /generate-questions
```

---

## Study Plan

```http
POST /study-plan
```

---

## Save Job

```http
POST /save-job
```

---

## Get Jobs

```http
GET /jobs
```

---

## Delete Job

```http
DELETE /delete-job/{job_id}
```

---

# Future Improvements

Planned features:

- Dedicated `/analyze-resume` endpoint
- Authentication
- Cloud deployment
- DOCX resume parsing
- Vector database integration
- AI memory
- Personalized learning plans
- Voice interview mode
- Resume-job match percentage
- Export roadmap to PDF

---

# Example Workflow

1. Save a job application
2. Extract skills from JD
3. Generate interview questions
4. Chat with study mentor
5. Generate roadmap
6. Upload resume
7. Analyze resume with AI
8. Improve ATS score

---

# Screens Included

The app includes:
- Applications Dashboard
- Interview Chatbot
- Study Mentor
- Roadmap Generator
- Resume Analyzer

---

# Author

Built as an AI Career Preparation Assistant project using FastAPI + Streamlit + Ollama.
# AI-Career-Assistant
