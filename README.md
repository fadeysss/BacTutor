# Bac Tutor (Flask + Local AI)

Bac Tutor is an offline-first study platform for Romanian Baccalaureate preparation.  
It is designed for real local usage (classmates/friends) and as a portfolio project that demonstrates full-stack product thinking, not just UI mockups.

## Why this project

- Romanian students need structured repetition for Bac topics, not only long notes.
- Many students prefer local/private tools over cloud-only AI products.
- A practical learning flow should combine lesson context, quick assessment, and progress feedback.

Core flow:

```text
subject -> section -> chapter -> lesson -> final quiz -> progress feedback
```

## Key features

- Structured curriculum for:
  - Romanian (mate-info)
  - Mathematics M1 (mate-info)
  - Informatics (mate-info)
- Chapter-based lessons with:
  - short recap
  - worked example
  - chapter formula sheet (M1 Subiectul I, II, III)
  - quick formula drills before final quiz
  - common mistakes
  - quick checks
  - end-of-lesson quiz
- Adaptive quiz selection from an exam bank (`data/exam_bank.json`)
- Progress tracking (XP, level, weak spots)
- Personal lesson upload (text or PDF)
- Knowledge ingestion with semantic search (optional Ollama embeddings)
- Local-first AI tutor with safe fallback when Ollama is unavailable

## Technical highlights

- **Backend:** Flask (single app, service-layer modules)
- **Data storage:** JSON files for catalog, progress, examples, quiz bank, knowledge feed
- **AI integration:** Ollama `/api/chat` and `/api/embed`
- **Frontend:** server-rendered Jinja + custom CSS/JS
- **Content ingestion:** PDF parsing via `pypdf`

Project structure:

```text
bactutor_app_v2/
├── app.py
├── services/
├── templates/
├── static/
├── data/
├── scripts/
└── uploads/
```

## Engineering decisions and tradeoffs

- **JSON over database:** chosen for local simplicity and easy portability.  
  Tradeoff: limited concurrency and weaker multi-user guarantees.
- **Server-rendered pages over SPA:** faster iteration and lower operational complexity.  
  Tradeoff: less dynamic client-side state handling.
- **Local AI optionality:** app remains usable without Ollama.  
  Tradeoff: response quality depends on local model/runtime availability.

## Recent improvements

- Hardened runtime defaults:
  - no static fallback secret key
  - debug mode controlled by `FLASK_DEBUG=1`
- Safer PDF uploads:
  - extension + MIME checks
  - PDF signature validation (`%PDF-`)
  - unique filenames (collision-safe)
  - explicit 20MB user-facing limit handling
- Ollama health status moved to TTL-based cache refresh (runtime recovers without restart)
- Improved site feel:
  - staggered reveal animations
  - better hover/interaction feedback
  - reduced-motion support for accessibility
- Better math readability:
  - unicode escape cleanup (`\uXXXX` no longer visible in lesson cards)
  - superscript/subscript rendering for powers and indices in formulas and quiz
- M1 expansion:
  - formula coverage added for Subiectul II and Subiectul III chapters
  - lesson quick-nav + live quiz completion progress bar
- Maintenance script portability fix:
  - removed hardcoded absolute path in `scripts/upgrade_math_m1_content.py`

## Quick start

### 1. Install

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Run app

```bash
python app.py
```

Open: `http://127.0.0.1:5000`

### 3. Optional: enable Ollama

```bash
ollama serve
ollama pull gemma3
ollama pull embeddinggemma
```

Set environment:

```bash
OLLAMA_ENABLED=1
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_CHAT_MODEL=gemma3
OLLAMA_EMBED_MODEL=embeddinggemma
```

Check:

```bash
python scripts/check_ollama.py
```

## Data files

- `data/catalog.json` - subject/section/chapter curriculum
- `data/chapter_examples.json` - worked examples and quick checks
- `data/exam_bank.json` - quiz items
- `data/progress.json` - student progress
- `data/knowledge_feed.jsonl` - imported notes/PDF chunks
- `data/knowledge_vectors.json` - semantic vectors
- `data/custom_lessons.json` - personal lessons

## Useful scripts

- `python scripts/add_knowledge.py ...`
- `python scripts/import_pdf.py ...`
- `python scripts/rebuild_embeddings.py`
- `python scripts/add_exam_item.py ...`

## Portfolio positioning (for CV / university applications)

This project demonstrates:

- end-to-end feature ownership (data model, backend services, UI, AI integration)
- educational product design (guided learning + assessment loop)
- pragmatic engineering tradeoffs (local-first, fallback strategies, maintainability)
- applied software quality improvements (input validation, runtime safety, UX polish)

## Next milestones

- Add lightweight automated tests (`pytest`) for route health and quiz grading
- Add a focused onboarding wizard (`recommended first chapter`)
- Add exportable progress snapshot for students
- Move persistence to SQLite if multi-user local concurrency becomes important
