# Bac Tutor

MVP web pentru pregătire la Bacalaureat, construit în Flask, cu interfață minimalist-modernă, structură pe materii / subiecte / capitole, progres pe sesiune și un knowledge feed extensibil.

## Ce conține MVP-ul

- **Materii disponibile**: Română (mate-info), Matematică M2, Informatică (mate-info), plus **Lecție personală**.
- **Navigare pedagogică**: materie → subiect → capitol.
- **Explicații pe capitol**: rezumat, obiectiv, capcană frecventă, pași de lucru și task-uri.
- **Mini-quiz**: 3 întrebări rapide, scor, XP și nivel (Începător / Intermediar / Avansat).
- **Dashboard de progres**: XP, scor mediu, activitate recentă, zone slabe.
- **Knowledge Feed**: poți adăuga manual notițe sau importa PDF-uri, iar aplicația le caută lexical și le afișează în capitolul relevant.
- **Lecție personală**: salvezi text sau PDF separat, iar tutorul generează rezumat și exerciții.
- **Integrare LLM opțională**: dacă rulezi local Ollama, tutorul poate formula răspunsuri mai naturale; altfel există un fallback local deterministic.

## Structura proiectului

```text
bactutor_app/
├── app.py
├── data/
│   ├── catalog.json
│   ├── custom_lessons.json
│   ├── knowledge_feed.jsonl
│   └── progress.json
├── scripts/
│   ├── add_knowledge.py
│   └── import_pdf.py
├── services/
│   ├── catalog_service.py
│   ├── content_store.py
│   ├── custom_lesson_service.py
│   ├── lesson_service.py
│   ├── llm_service.py
│   ├── progress_service.py
│   └── quiz_service.py
├── static/
│   ├── app.js
│   └── style.css
├── templates/
│   ├── admin.html
│   ├── base.html
│   ├── custom_lesson.html
│   ├── dashboard.html
│   ├── home.html
│   ├── lesson.html
│   └── subject.html
└── uploads/
```

## Instalare rapidă

```bash
cd bactutor_app
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Deschizi apoi `http://127.0.0.1:5000`.

## Cum „hrănești” tutorul cu informații

### Din interfață

- intri în **Knowledge Feed**;
- adaugi o notiță manuală sau imporți un PDF;
- alegi materia / subiectul / capitolul la care să se lege informația.

Toate intrările noi se salvează în `data/knowledge_feed.jsonl`.

### Din linia de comandă

Adaugă o notiță:

```bash
python scripts/add_knowledge.py   --title "Formule derivate"   --subject matematica_m2   --subiect subiectul-3   --chapter derivabilitate   --text "Reguli de derivare, lanț, produs, raport..."
```

Importă un PDF:

```bash
python scripts/import_pdf.py   --file /cale/catre/lectie.pdf   --title "Sinteza roman"   --subject romana_mate_info   --subiect subiectul-3   --chapter liviu-rebreanu-roman-realist-obiectiv
```

## Integrare Ollama (opțional)

Dacă ai Ollama pornit local, poți activa răspunsurile LLM setând variabilele:

```bash
export OLLAMA_ENABLED=1
export OLLAMA_HOST=http://127.0.0.1:11434
export OLLAMA_MODEL=llama3.1:8b
```

Dacă Ollama nu rulează, aplicația rămâne funcțională și folosește explicațiile din catalog + knowledge feed.

## Fișierele de date importante

- `data/catalog.json` — structura materiilor, subiectelor și capitolelor.
- `data/knowledge_feed.jsonl` — log extensibil cu notițe și fragmente PDF.
- `data/progress.json` — progresul pe sesiune.
- `data/custom_lessons.json` — lecțiile personale salvate de utilizatori.

## Ajustări rapide pe care le poți face

- vrei **altă structură pe capitole** → editezi `data/catalog.json`;
- vrei **M1 în loc de M2** → schimbi capitolele din catalog și descrierea materiei;
- vrei **quiz-uri mai precise** → adaugi în catalog întrebări manuale pe capitol și extinzi `quiz_service.py`;
- vrei **corectare din poză** → poți adăuga ulterior un modul OCR / vision pe ruta de lesson.

## De ce este util acest MVP

Nu este doar o pagină frumoasă: are deja structura de conținut, log-ul de cunoștințe, progresul elevului și punctele de extensie pentru LLM, PDF-uri și capitole noi.
