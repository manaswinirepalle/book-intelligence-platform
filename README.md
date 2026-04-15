# Book Intelligence Platform

Book Intelligence Platform is a production-style full-stack web application that combines web scraping, metadata storage, and AI-powered RAG (Retrieval-Augmented Generation) to support book discovery and contextual Q&A.

## Features

- Django REST Framework backend with MySQL metadata persistence.
- Selenium scraper for bulk ingestion from `books.toscrape.com`.
- RAG pipeline using overlapping chunking, Sentence Transformers embeddings, ChromaDB retrieval, and LM Studio for generation.
- AI enrichments:
  - Summary generation
  - Genre classification
  - Sentiment analysis
  - Recommendation logic
- Query-level caching for repeated `/api/ask/` requests.
- Chat history storage for previous Q&A interactions.
- React + Tailwind frontend with loading and error states.

## Tech Stack

### Backend
- Python
- Django + Django REST Framework
- MySQL
- ChromaDB
- Sentence Transformers
- Selenium
- LM Studio (OpenAI-compatible local endpoint)

### Frontend
- React (Vite)
- Tailwind CSS
- Axios

## Project Structure

```text
backend/
  books_app/
  api/
  rag/
  scraper/
  models/
  serializers/
  views/
  urls.py
  settings.py
  requirements.txt
frontend/
  src/
  components/
  pages/
  services/
  App.jsx
  main.jsx
```

## Database Design

### `books` table
- `id`
- `title`
- `author`
- `description`
- `rating`
- `reviews_count`
- `book_url`
- `created_at`

### Additional table
- `chat_history`: `question`, `answer`, `sources_json`, `created_at`

## Backend Setup (Step-by-Step)

1. Create MySQL database:
   ```sql
   CREATE DATABASE book_intelligence CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. Setup backend environment:
   ```bash
   cd backend
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   # source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Configure environment:
   ```bash
   copy .env.example .env
   ```
   Then update MySQL + LM Studio values in `.env`.

4. Run migrations:
   ```bash
   python manage.py makemigrations api
   python manage.py migrate
   ```

5. (Optional) Seed sample books from `backend/sample_data/books_seed.json` using Django shell.

6. Run backend:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

## Frontend Setup

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

Frontend runs at `http://localhost:5173`.

## API Documentation

Base URL: `http://localhost:8000/api`

### GET Endpoints
- `GET /books/` - List all books
- `GET /books/<id>/` - Book details (+ AI summary/genre/sentiment)
- `GET /recommend/<id>/` - Recommended books
- `GET /history/` - Chat history

### POST Endpoints
- `POST /upload/` - Scrape and store books
  ```json
  {
    "pages": 2
  }
  ```

- `POST /ask/` - RAG-based Q&A
  ```json
  {
    "question": "Which books discuss future technology?",
    "top_k": 4
  }
  ```

## Sample Q&A Response

```json
{
  "question": "Which books discuss future technology?",
  "answer": "Based on retrieved context...",
  "sources": [
    {
      "title": "Orbit of Ideas",
      "book_id": 2,
      "source": "https://example.com/books/orbit-of-ideas"
    }
  ],
  "cached": false
}
```

## RAG Pipeline

1. Descriptions are split into overlapping chunks.
2. Chunks are embedded by Sentence Transformers.
3. Embeddings are stored in ChromaDB.
4. Query embedding is used for similarity search.
5. Retrieved context + question are sent to LM Studio.
6. Answer + sources are returned and cached.

## Optimization & Architecture Notes

- Caching for repeated questions via Django cache.
- Modular RAG files in `backend/rag/`.
- Reusable serializers and view modules.
- Bulk scraping supported by `pages` parameter in `/upload/`.

## Bonus Features Included

- Chat history persistence (`chat_history` table).
- Bulk scraping support.
- Async-ready modular structure (Celery can be attached later to offload scraping/RAG tasks).

## Screenshot Placeholders

- `docs/screenshots/dashboard.png`
- `docs/screenshots/book-detail.png`
- `docs/screenshots/qa-page.png`
