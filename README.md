# Yakuza 0 RAG Backend API

A high-performance, asynchronous FastAPI backend powering a Retrieval-Augmented Generation (RAG) pipeline to query Yakuza 0 GameFAQs guides. Built using ChromaDB, SentenceTransformers, and local Ollama (`llama3`).

## Tech Stack

* **Framework:** FastAPI (Python 3.10+)
* **Settings & Schemas:** Pydantic v2 & `pydantic-settings`
* **Vector Store:** ChromaDB (`PersistentClient`)
* **Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2`)
* **LLM Engine:** Ollama (`llama3`)
* **Testing:** Pytest & `httpx`

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

4. Configure environment variables by creating a `.env` file in the `backend/` directory (optional, defaults are pre-configured):
   ```ini
   CHROMA_DB_DIR=app/data/vector_store
   COLLECTION_NAME=yakuza_guide
   EMBEDDING_MODEL=all-MiniLM-L6-v2
   OLLAMA_MODEL=llama3
   OLLAMA_BASE_URL=http://localhost:11434
   CORS_ORIGINS=["*"]
   ```

---

## Running Automated Tests

Run the test suite using Python's module runner to ensure path resolution works across all platforms:

```bash
python -m pytest tests/test_query.py
```

---

## Running the Application

1. Verify Ollama is active:
   ```bash
   curl http://localhost:11434
   ```

2. Start the Uvicorn development server from inside the `backend/` directory:
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

3. Access the interactive API documentation (Swagger UI) at:
   `http://127.0.0.1:8000/docs`

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