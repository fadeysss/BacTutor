# Bac Tutor - Architecture and Handoff

## 1. Project Purpose

Bac Tutor is a local-first study web app for Romanian Baccalaureate preparation.
It is designed around short, complete study sessions:

1. pick subject/subiect/chapter
2. read structured lesson
3. solve end-of-lesson quiz
4. get immediate feedback
5. persist progress locally

The app works without cloud dependencies. AI assistance is optional via local Ollama.

---

## 2. Tech Stack

- Backend: Flask (server-rendered)
- Templates: Jinja2
- Frontend: custom CSS + vanilla JS
- Data persistence: JSON + JSONL files in `data/`
- PDF parsing: `pypdf`
- Optional local AI:
  - Ollama `/api/chat`
  - Ollama `/api/embed`

Dependencies are declared in `requirements.txt`:

- `Flask>=3.0,<4.0`
- `pypdf>=4.2,<6.0`
- `python-dotenv>=1.0,<2.0`

---

## 3. Repository Structure

Main folders and responsibilities:

- `app.py`: Flask app entrypoint, route handlers, request orchestration
- `services/`: business logic and data-access helpers
- `templates/`: page templates
- `static/`: CSS and JS
- `data/`: all persistent app content/state
- `scripts/`: maintenance and content generation scripts
- `uploads/`: uploaded PDF files

Key files:

- `app.py`
- `services/catalog_service.py`
- `services/lesson_service.py`
- `services/quiz_service.py`
- `services/progress_service.py`
- `services/exam_bank_service.py`
- `services/content_store.py`
- `services/chapter_examples_service.py`
- `services/custom_lesson_service.py`
- `services/formula_sheet_service.py`
- `services/math_text_service.py`
- `services/llm_service.py`
- `templates/lesson.html`
- `static/app.js`
- `static/style.css`

---

## 4. Core Runtime Architecture

## 4.1 Request lifecycle

1. Flask route in `app.py` receives request.
2. Route resolves IDs (`subject_id`, `subiect_id`, `chapter_id`) via catalog service.
3. Route calls lesson/quiz/progress/content services to assemble data.
4. Route renders Jinja template with computed context.
5. POST actions update local JSON state and re-render page.

No DB, no ORM. All state is file-based.

## 4.2 Session identity model

- Anonymous local student identity is created in Flask session by `ensure_student_id(session)`.
- This `student_id` is used as key in `data/progress.json`.

---

## 5. Route Map and Behaviors

Defined in `app.py`.

## 5.1 `GET /` (home)

- Loads catalog subjects
- Loads student summary
- Computes `recommended_start` (first available chapter in preferred subject order)
- Renders `templates/home.html`

## 5.2 `GET /dashboard`

- Loads student summary across subjects
- Computes weak-spot links to chapters with low recent scores
- Renders `templates/dashboard.html`

## 5.3 `GET /subject/<subject_id>`

- Canonicalizes legacy aliases (`matematica_m2 -> matematica_m1`)
- Loads subject + chapter stats
- Renders chapter cards with score badges
- Renders `templates/subject.html`

## 5.4 `GET/POST /lesson/<subject_id>/<subiect_id>/<chapter_id>`

Main learning route:

- marks chapter view in progress
- builds lesson bundle
- builds adaptive quiz set
- handles POST actions:
  - `action=ask` (free AI question)
  - `action=smart_help` (preset helper question)
  - `action=quiz` (quiz submission + grading + XP update)
- renders `templates/lesson.html`

## 5.5 `GET/POST /custom-lesson`

- allows manual text lesson creation
- allows PDF lesson import and conversion to text
- stores personal lessons
- supports Q&A scoped to selected personal lesson
- renders `templates/custom_lesson.html`

## 5.6 `GET/POST /admin`

- add manual knowledge notes
- import PDF into chunked knowledge entries
- rebuild missing semantic embeddings
- show knowledge stats + recent entries
- renders `templates/admin.html`

---

## 6. Service Layer Responsibilities

## 6.1 `catalog_service.py`

- Loads `data/catalog.json` (cached via `lru_cache`)
- Fetches subject/subiect/chapter entities
- Provides flat catalog bindings for admin forms
- Handles legacy subject aliases

## 6.2 `progress_service.py`

- Reads/writes `data/progress.json`
- Tracks views and quiz attempts
- XP, level, averages, weak spots
- Level thresholds:
  - `< 90` XP: Incepator
  - `< 220` XP: Intermediar
  - `>= 220` XP: Avansat

XP gain on quiz:

- `xp_gain = 10 + score * 8`

## 6.3 `exam_bank_service.py`

- Reads/writes `data/exam_bank.json`
- Returns chapter item pools
- Adaptive selection based on:
  - student level
  - chapter attempts/last score
  - difficulty distribution plan
- Quiz length:
  - `matematica_m1`: 20 items
  - other subjects: 1 item

## 6.4 `quiz_service.py`

- Converts exam items to renderable quiz question objects
- Adds formatted HTML fields for math readability:
  - `prompt_html`
  - `options[].label`
  - `explanation_html`
  - `hint_html`
  - `worked_steps_html`
- Grades submitted answers and returns detailed feedback structure

## 6.5 `chapter_examples_service.py`

- Reads `data/chapter_examples.json`
- Returns chapter-specific micro recap, example, checks, sprint plan

## 6.6 `formula_sheet_service.py`

- Loads all files matching `data/math_m1_subiect*_formulas.json`
- Builds index by `(subject_id, subiect_id, chapter_id)`
- Returns formula sheet object per chapter

## 6.7 `math_text_service.py`

Central math rendering utility:

- decodes escaped unicode (`\uXXXX`, `\UXXXXXXXX`)
- normalizes operators/symbols (`<=`, `>=`, `->`, `sqrt(...)`, etc.)
- converts exponent/subscript text into HTML `sup/sub`
- used in drills, quiz prompts/options/results

## 6.8 `lesson_service.py`

Composes complete lesson context:

- chapter explanation sections
- revision cards
- chapter worked example
- formula sheet (if available)
- formula drills from recent/adaptive exam items
- quick checks and sprint plan
- knowledge snippets
- AI status

Also provides AI/fallback chapter Q&A.

## 6.9 `content_store.py`

Knowledge ingestion and retrieval:

- appends notes to `knowledge_feed.jsonl`
- extracts/chunks PDF text
- stores embeddings in `knowledge_vectors.json`
- lexical + semantic search
- snippet generation for lesson context

## 6.10 `custom_lesson_service.py`

- stores personal lessons in `custom_lessons.json`
- supports text and PDF lessons
- mirrors personal lesson content into knowledge feed

## 6.11 `llm_service.py`

- optional Ollama integration wrapper
- chat and embeddings APIs
- health/status check (`/api/tags`)
- status cache with TTL (20s)
- graceful failure when Ollama unavailable

---

## 7. Data Model Contracts

## 7.1 `data/catalog.json`

Top-level:

```json
{
  "subjects": [
    {
      "id": "...",
      "title": "...",
      "subiecte": [
        {
          "id": "...",
          "chapters": [
            { "id": "...", "title": "...", "summary": "..." }
          ]
        }
      ]
    }
  ]
}
```

Subject keys in use:

- `id`, `title`, `short_title`, `track`, `discipline_type`, `badge`, `description`, `subiecte`

Subiect keys in use:

- `id`, `title`, `summary`, `chapters`

Chapter keys in use:

- `id`, `title`, `summary`, `objective`, `common_mistake`, `practice_prompt`, `practice_type`, `estimated_minutes`, `coach_tip`, `starter_tasks`, `keywords`

## 7.2 `data/exam_bank.json`

Item keys in use:

- `id`, `subject_id`, `subiect_id`, `chapter_id`, `year`, `source_type`, `source_label`, `difficulty`, `prompt`, `options`, `correct_index`, `explanation`, `hint`, `worked_steps`, `tags`

## 7.3 `data/chapter_examples.json`

Item keys:

- `subject_id`, `subiect_id`, `chapter_id`, `micro_recap`, `attention_hook`, `concrete_example`, `quick_checks`, `memory_hook`, `sprint_plan`

## 7.4 `data/progress.json`

Per student keys:

- `xp`, `quizzes_taken`, `average_score`, `chapters_viewed`, `subjects`, `recent_activity`, `created_at`

## 7.5 `data/knowledge_feed.jsonl`

Each line is one JSON entry.
Typical keys:

- `id`, `timestamp`, `source_type`, `source_name`, `subject_id`, `subiect_id`, `chapter_id`, `title`, `text`, `keywords`

## 7.6 `data/knowledge_vectors.json`

Structure:

```json
{
  "vectors": {
    "<entry_id>": [0.1, -0.2, ...]
  }
}
```

## 7.7 `data/math_m1_subiect*_formulas.json`

Structure:

```json
{
  "subject_id": "matematica_m1",
  "subiect_id": "subiectul-2",
  "chapters": [
    {
      "chapter_id": "...",
      "title": "...",
      "formulas": ["..."],
      "tips": ["..."]
    }
  ]
}
```

---

## 8. Matematica M1 Content State

Current M1 structure:

- Subiectul 1: 14 chapters
- Subiectul 2: 3 chapters
- Subiectul 3: 7 chapters

Current exam-bank distribution includes large M1 coverage and formula sheets are available for all M1 subiecte (I/II/III).

---

## 9. Frontend Architecture

## 9.1 Base layout

- Shared layout in `templates/base.html`
- top navigation + global Ollama status pill
- flash message stack

## 9.2 Lesson page UI model

`templates/lesson.html` includes:

- lesson hero
- quick section jump navigation
- explanation blocks
- worked example
- formula sheet
- formula drills
- sprint/check blocks
- knowledge snippet cards
- final quiz zone
- sticky AI tutor panel

## 9.3 JS behavior (`static/app.js`)

- chapter filter
- quiz option selected-state sync
- quiz completion progress bar (`data-quiz-progress`)
- motion handling:
  - reveal animations
  - safe fallback if observer not available
  - reduced motion mode
- pointer-based background glow

---

## 10. Security and Reliability Controls

Implemented in `app.py`:

- `SECRET_KEY`: env value or runtime random fallback (`os.urandom(32).hex()`)
- max upload limit: `20MB` (`MAX_CONTENT_LENGTH`)
- PDF upload validation:
  - filename present
  - `.pdf` extension
  - MIME allowlist
  - signature check (`%PDF-`)
- unique upload names with UUID
- explicit 413 error handler with user-facing message

Non-fatal fallback design:

- if Ollama fails: lessons and quiz still work
- if embeddings missing: lexical search still works

---

## 11. Configuration and Environment

Runtime environment variables:

- `FLASK_DEBUG` (`1` enables debug)
- `SECRET_KEY`
- `OLLAMA_ENABLED` (`1`/`0`)
- `OLLAMA_HOST` or `OLLAMA_BASE_URL`
- `OLLAMA_MODEL` or `OLLAMA_CHAT_MODEL`
- `OLLAMA_EMBED_MODEL`

Ollama status cache:

- TTL = 20 seconds in `llm_service.py`

---

## 12. Scripts and Operational Tooling

Available scripts in `scripts/`:

- `add_exam_item.py`: append manual quiz item
- `add_knowledge.py`: append knowledge note
- `check_ollama.py`: print Ollama health/models
- `generate_exam_content.py`: generate content sets
- `import_pdf.py`: CLI PDF import pipeline
- `migrate_math_subject_m2_to_m1.py`: subject migration helper
- `rebuild_embeddings.py`: index missing embeddings
- `upgrade_math_m1_content.py`: M1 content upgrade tooling

---

## 13. How to Run Locally

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open:

- `http://127.0.0.1:5000`

Optional Ollama:

```powershell
ollama serve
ollama pull gemma3
ollama pull embeddinggemma
```

---

## 14. Extension Rules (Do Not Break These)

1. Keep ID contracts stable:
   - `subject_id`
   - `subiect_id`
   - `chapter_id`

2. Keep quiz-template data contract stable:
   - `question.prompt_html`
   - `question.options[].value/label`
   - result detail HTML fields (`selected_html`, `correct_html`, etc.)

3. If changing JSON schema, provide migration script.

4. If adding formulas for new areas, follow current formula file schema and chapter ID mapping.

5. Keep graceful degradation:
   - app must remain usable with Ollama offline.

---

## 15. Known Technical Debt / Risks

1. File-based persistence (JSON) is simple but not ideal for concurrent writes.
2. No full automated test suite yet (route + business-logic tests recommended).
3. Some historical text encoding artifacts exist in parts of content strings.
4. `lesson_service.py` still contains legacy formatter helpers; current active formatter path is `math_text_service.py`.

---

## 16. Recommended Next Improvements

1. Add `pytest` suite:
   - route health tests
   - quiz grading tests
   - progress XP/level tests
   - formula mapping tests for all M1 chapters

2. Add schema validation at startup:
   - verify all chapters in catalog have matching exam items/formula sheet where expected

3. Introduce SQLite migration path for progress and knowledge metadata.

4. Add admin diagnostics page:
   - missing chapter examples
   - missing formula sheets
   - low item-count chapters

5. Normalize remaining text encoding artifacts in content files.

---

## 17. One-Block Handoff Prompt for Another AI

Use this as first message for a new AI collaborator:

```text
You are continuing work on Bac Tutor in C:\Users\meduz\Desktop\test\bactutor_app_v2.
Stack: Flask + Jinja + CSS/JS, local JSON persistence.
Key entrypoint: app.py.
Main services: catalog_service, lesson_service, quiz_service, progress_service, exam_bank_service, content_store, llm_service, formula_sheet_service, math_text_service.
Data contracts are in data/catalog.json, exam_bank.json, chapter_examples.json, progress.json, knowledge_feed.jsonl, knowledge_vectors.json, custom_lessons.json, and math_m1_subiect1/2/3_formulas.json.
Lesson page expects math-rendered HTML fields from quiz_service and uses formula sheets + formula drills.
Do not break ID contracts (subject_id/subiect_id/chapter_id) or the lesson template field contract.
Maintain offline usability when Ollama is unavailable.
If schema changes are needed, add explicit migration scripts.
```

