# ExamPrep (GCSE & HKDSE) - Minimal API

An initial scaffold for a math exam-prep application targeting GCSE and HKDSE students. This minimal version exposes a small FastAPI service with a few endpoints and sample logic for topics like probability, coordinate geometry, calculus, and matrices.

## Quickstart

Requirements:
- Python 3.10+ recommended

Setup and run:
```bash
cd /workspace
python -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Verify the API is up:
```bash
curl -s http://127.0.0.1:8000/health
```

## API Overview

- `GET /health`: Health check.
- `GET /topics`: List supported topics.
- `GET /samples/{topic}`: View minimal sample questions per topic.
- `POST /solve`: Demonstration solver that handles one simple case per topic.

Example: probability sample
```bash
curl -s -X POST http://127.0.0.1:8000/solve \
  -H 'Content-Type: application/json' \
  -d '{"topic":"probability","data":{"red":3,"blue":2}}'
```

Example: coordinate geometry distance
```bash
curl -s -X POST http://127.0.0.1:8000/solve \
  -H 'Content-Type: application/json' \
  -d '{"topic":"coordinate-geometry","data":{"x1":1,"y1":2,"x2":4,"y2":6}}'
```

## Project Scope (Initial)

This is a minimal foundation. Next steps will include:
- Expanding topic coverage and question banks (GCSE/HKDSE past-paper style)
- Step-by-step worked solutions and hints
- Conversational tutoring (chat) with reasoning traces
- Progress tracking and spaced repetition
- Monetization hooks (subscriptions, premium content)

## Notes

- This is not production-ready. It is a starting point to iterate quickly.
- The sample logic is intentionally simple for clarity.