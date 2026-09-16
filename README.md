# Yakuza 0 RAG Application (Full-Stack)

A full-stack Retrieval-Augmented Generation (RAG) application for querying Yakuza 0 GameFAQs guides. The project combines a high-performance, asynchronous **FastAPI backend** — handling retrieval and generation over ChromaDB, SentenceTransformers, and local Ollama (`llama3`) — with an interactive **Streamlit chat frontend** that lets users converse naturally with the RAG pipeline and inspect cited sources for every answer.

## Tech Stack

### Backend

* **Framework:** FastAPI (Python 3.10+)
* **Settings & Schemas:** Pydantic v2 & `pydantic-settings`
* **Vector Store:** ChromaDB (`PersistentClient`)
* **Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2`)
* **LLM Engine:** Ollama (`llama3`)
* **Testing:** Pytest & `httpx`

### Frontend

* **Framework:** Streamlit
* **HTTP Client:** `requests`
* **Environment Config:** `python-dotenv`

---

## Prerequisites

1. **Python 3.10+** installed.
2. **Ollama** installed and running locally.
3. **Llama 3 Model** pulled in Ollama:
```bash
ollama pull llama3
```

---

## Setup & Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv

# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# Linux/macOS:
source .venv/bin/activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables by copying `.env.example` to `.env` in the `backend/` directory (optional, defaults are pre-configured):
```ini
CHROMA_DB_DIR=app/data/vector_store
COLLECTION_NAME=yakuza_guide
EMBEDDING_MODEL=all-MiniLM-L6-v2
OLLAMA_MODEL=llama3
OLLAMA_BASE_URL=http://localhost:11434
CORS_ORIGINS=["*"]
```

### Frontend Setup

1. Ensure your virtual environment is active, then install frontend dependencies:
```bash
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# Linux/macOS:
source .venv/bin/activate

# Install requirements:
pip install -r frontend/requirements.txt
```

2. Configure environment variables by copying `.env.example` to `.env` in the `frontend/` directory (optional — this value is also defaulted in code):
```ini
API_BASE_URL=http://localhost:8000
```

---

## Running Automated Tests

Run the backend test suite using Python's module runner to ensure path resolution works across all platforms:

```bash
# Run from the project root:
python -m pytest backend/tests/test_query.py

# OR run from inside backend/:
cd backend && python -m pytest tests/test_query.py
```

---

## How to Run

Follow these steps in order to bring up the full stack locally.

### Step 1: Verify Ollama is Active

Confirm the local Ollama daemon is running and that the `llama3` model is available:

```bash
curl http://localhost:11434
ollama pull llama3
```

### Step 2: Start the Backend API

From inside the `backend/` directory, start the Uvicorn development server:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The interactive API documentation (Swagger UI) will be available at:
`http://127.0.0.1:8000/docs`

### Step 3: Start the Streamlit Frontend

From the **project root**, in a separate terminal, launch the Streamlit app:

```bash
streamlit run frontend/app.py --server.port 8501
```

The chat interface will be accessible at:
`http://localhost:8501`

> **Note:** The backend (Step 2) must be running before the frontend can successfully send queries, since the Streamlit app communicates with the FastAPI service via `API_BASE_URL`.

---

## API Endpoints

### 1. Health Check
* **Endpoint:** `GET /health`
* **Description:** Verifies service availability.
* **Response (200 OK):**
```json
{
  "status": "ok"
}
```

### 2. Query RAG Pipeline
* **Endpoint:** `POST /query`
* **Description:** Generates an answer strictly using retrieved context from the Yakuza 0 GameFAQs database.
* **Request Body:**
```json
{
  "question": "How do I unlock Kiryu Legend style?"
}
```
* **Response (200 OK):**
```json
{
  "answer": "To unlock Kiryu's Legend style (Dragon of Dojima), you must complete the Real Estate Royale storyline...",
  "sources": [
    "02_Real_Estate_Royale.txt"
  ]
}
```

#### Example Usage

**cURL (Terminal / Bash / PowerShell):**
```bash
curl.exe -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "How do I unlock Kiryu Legend style?"}'
```

**PowerShell (`Invoke-RestMethod`):**
```powershell
$body = @{ question = "How do I unlock Kiryu Legend style?" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/query" -Method Post -ContentType "application/json" -Body $body
```

---

## Project Structure Overview

```
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── query.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── data/
│   │   │   └── vector_store/
│   │   │       ├── 3682f241-fcfc-4b45-.../
│   │   │       ├── chroma.sqlite3
│   │   │       └── config.json
│   │   ├── schemas/
│   │   │   └── query.py
│   │   ├── services/
│   │   │   ├── generation.py
│   │   │   └── retrieval.py
│   │   ├── utils/
│   │   └── main.py
│   ├── tests/
│   │   └── test_query.py
│   ├── data/
│   │   ├── 01_Combat_And_Abilities.txt
│   │   ├── 02_Real_Estate_Royale.txt
│   │   ├── 03_Cabaret_Club_Czar.txt
│   │   ├── 04_Substories.txt
│   │   └── 05_Minigames.txt
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── notebooks/
│   │   └── rag_pipeline.ipynb
│   ├── .env.example
│   ├── api_client.py
│   ├── app.py
│   └── requirements.txt
├── .gitattributes
├── .gitignore
├── LICENSE
└── README.md
```