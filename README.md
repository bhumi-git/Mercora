# Mercora

> **Turning raw business data into decisions, not just dashboards.**

Mercora is an AI-assisted business intelligence platform designed to transform raw, structured data into meaningful analytics, interactive insights, and decision-ready information.

The project combines backend engineering, data processing, cloud-based data storage, and generative AI to explore how traditional business analytics can become more accessible and actionable.

**Status:** 🚧 Active Development

---

## The Problem

Businesses often have access to large amounts of operational data, but raw data alone does not make decision-making easier.

Data may be:

* scattered across different files and sources
* difficult to interpret without technical expertise
* time-consuming to analyze manually
* presented through dashboards without enough context
* disconnected from the actual business questions users need answered

Mercora explores a different approach:

> **What if a business could provide its data and get both the analytics and the reasoning behind them?**

---

## The Solution

Mercora is being developed as an AI-assisted analytics platform that can:

1. Ingest structured business data
2. Store and process the data through a backend system
3. Analyze important patterns and metrics
4. Present insights through an interactive interface
5. Use generative AI to help interpret data and surface meaningful observations

The goal is not simply to create another dashboard, but to build a system that connects:

**Data → Analysis → Insight → Decision**

---

## Current Development

The current version focuses on establishing the core backend and data infrastructure.

### Implemented

* [x] FastAPI backend
* [x] Backend project structure
* [x] Neon PostgreSQL database integration
* [x] Gemini API integration
* [x] Database setup and table creation
* [x] Environment-based configuration
* [ ] Data ingestion pipeline
* [ ] Analytics engine
* [ ] Dashboard interface
* [ ] AI-generated business insights
* [ ] End-to-end workflow
* [ ] Deployment

> Features marked as incomplete are actively being developed.

---

## Architecture

The planned architecture follows a modular flow:

```text
                ┌──────────────────┐
                │   Business Data  │
                │ CSV / Structured │
                │      Data        │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │   FastAPI        │
                │    Backend       │
                └────────┬─────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
     ┌─────────────────┐   ┌─────────────────┐
     │ Neon PostgreSQL │   │ Data Processing │
     │    Database     │   │   & Analytics   │
     └─────────────────┘   └────────┬────────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │   Gemini API    │
                           │ AI Interpretation│
                           └────────┬────────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │   Dashboard /   │
                           │   User Insights │
                           └─────────────────┘
```

*Architecture will evolve as development progresses.*

---

## Tech Stack

### Backend

* Python
* FastAPI
* REST APIs

### Database

* PostgreSQL
* Neon

### AI

* Google Gemini API

### Development

* Git
* GitHub
* VS Code
* Python Virtual Environment

### Planned / In Progress

* Data processing and analytics
* Interactive dashboard
* Visualization layer
* Cloud deployment

---

## How Mercora Works

The intended workflow is:

```text
Upload / Connect Data
        ↓
Data Validation
        ↓
Data Processing
        ↓
Database Storage
        ↓
Analytics & Metric Generation
        ↓
AI-assisted Interpretation
        ↓
Interactive Business Insights
```

The system is being designed so that the user does not need to manually inspect every data point to understand what is happening.

---

## AI Layer

Mercora integrates Google's Gemini API as an AI-assisted interpretation layer.

Rather than replacing the underlying analytics, the AI component is intended to work alongside structured analysis to help translate quantitative findings into understandable business insights.

Potential use cases include:

* identifying notable patterns
* summarizing trends
* explaining unusual changes
* generating natural-language observations
* helping users explore business questions

The exact AI capabilities are still under development.

---

## Project Goals

Mercora is being built to explore several areas of modern software engineering:

* Backend API development
* Database architecture
* Data processing
* Business intelligence
* Generative AI integration
* Cloud-ready application design
* Product-oriented problem solving

The larger objective is to bridge the gap between **technical data processing and human decision-making**.

---

## Project Structure

```text
Mercora/
│
├── app/
│   ├── ...
│
├── create_tables.py
├── .env.example
├── .gitignore
├── README.md
└── ...
```

The structure will evolve as additional modules are implemented.

---

## Local Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd Mercora
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file based on `.env.example`.

```env
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=your_neon_database_url
```

**Never commit your `.env` file or API credentials to GitHub.**

### 6. Run the backend

```bash
uvicorn app.main:app --reload
```

The exact command may change as the project architecture evolves.

---

## Development Roadmap

### Phase 1 — Foundation

* [x] Project setup
* [x] FastAPI backend
* [x] PostgreSQL/Neon integration
* [x] Gemini API integration

### Phase 2 — Data Intelligence

* [ ] Data ingestion
* [ ] Data validation
* [ ] Data cleaning
* [ ] Automated metric generation
* [ ] Analytics engine

### Phase 3 — Product Experience

* [ ] Interactive dashboard
* [ ] Data
