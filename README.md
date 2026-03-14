# pdf-text-extractor

A lightweight FastAPI microservice that extracts text from PDF files. Designed to feed downstream LLM pipelines with clean, structured text.

## Features

- Extracts text from any text-based PDF
- Two output modes: **page-by-page** or **full document**
- Optional text cleaning: collapses whitespace and line breaks
- Ready to run in Docker

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv)
- Docker (optional)

## Running locally

```bash
uv sync
uv run uvicorn main:app --reload --reload-dir .
```

API available at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

## Running with Docker

```bash
docker build -t pdf-text-extractor .
docker run -p 8000:8000 pdf-text-extractor
```

## API

### `GET /health`

Returns service status.

```json
{ "status": "ok" }
```

---

### `POST /extract`

Extracts text from an uploaded PDF.

**Parameters**

| Name    | Type    | Default | Description |
|---------|---------|---------|-------------|
| `mode`  | string  | `pages` | `pages` returns one entry per page; `full` returns the entire document as a single string |
| `clean` | boolean | `false` | `true` collapses multiple spaces and line breaks into single spaces |

**Request**

```bash
curl -X POST "http://localhost:8000/extract?mode=pages&clean=false" \
  -F "file=@document.pdf"
```

**Response — `mode=pages`**

```json
{
  "total_pages": 3,
  "pages": [
    { "page": 1, "text": "..." },
    { "page": 2, "text": "..." },
    { "page": 3, "text": "..." }
  ]
}
```

**Response — `mode=full`**

```json
{
  "total_pages": 3,
  "text": "..."
}
```

## Tech stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [uv](https://github.com/astral-sh/uv)
- Python 3.13
