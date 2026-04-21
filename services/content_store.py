from __future__ import annotations

import json
import math
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader

from .llm_service import embed_text, embed_texts, get_ollama_status

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
FEED_PATH = DATA_DIR / 'knowledge_feed.jsonl'
VECTORS_PATH = DATA_DIR / 'knowledge_vectors.json'

STOPWORDS = {
    'si', 'sau', 'iar', 'dar', 'din', 'pentru', 'este', 'sunt', 'care', 'aceasta', 'acest',
    'fara', 'prin', 'cum', 'la', 'de', 'pe', 'cu', 'ca', 'un', 'o', 'in', 'sa', 'se', 'mai',
    'fi', 'ale', 'al', 'ai', 'acea', 'acela', 'cele', 'cel', 'bac', 'tutor', 'materie', 'subiect',
    'capitol', 'despre', 'intr', 'sunt', 'este', 'fost', 'dupa', 'pentru', 'daca', 'care', 'unde', 'cand'
}


def ensure_feed_file() -> None:
    FEED_PATH.parent.mkdir(parents=True, exist_ok=True)
    FEED_PATH.touch(exist_ok=True)


def ensure_vectors_file() -> None:
    VECTORS_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not VECTORS_PATH.exists():
        VECTORS_PATH.write_text(json.dumps({'vectors': {}}, ensure_ascii=False, indent=2), encoding='utf-8')


def tokenize(text: str) -> list[str]:
    text = text.lower()
    tokens = re.findall(r"[a-zA-Zăâîșşțţ0-9\-]+", text)
    normalized = []
    for token in tokens:
        token = (
            token.replace('ă', 'a').replace('â', 'a').replace('î', 'i')
            .replace('ș', 's').replace('ş', 's').replace('ț', 't').replace('ţ', 't')
        )
        if len(token) > 2 and token not in STOPWORDS:
            normalized.append(token)
    return normalized


def load_entries() -> list[dict]:
    ensure_feed_file()
    entries = []
    with FEED_PATH.open(encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def load_vectors() -> dict:
    ensure_vectors_file()
    try:
        with VECTORS_PATH.open(encoding='utf-8') as fh:
            payload = json.load(fh)
    except (json.JSONDecodeError, OSError):
        payload = {'vectors': {}}
    payload.setdefault('vectors', {})
    return payload


def save_vectors(payload: dict) -> None:
    ensure_vectors_file()
    with VECTORS_PATH.open('w', encoding='utf-8') as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)


def _set_vector(entry_id: str, vector: list[float]) -> None:
    payload = load_vectors()
    payload.setdefault('vectors', {})[entry_id] = vector
    save_vectors(payload)


def _get_vector(entry_id: str) -> list[float] | None:
    payload = load_vectors()
    vector = payload.get('vectors', {}).get(entry_id)
    if isinstance(vector, list):
        return vector
    return None


def append_note(title: str, text: str, subject_id: str = '', subiect_id: str = '', chapter_id: str = '',
                source_type: str = 'manual_note', source_name: str = 'notiță adăugată manual',
                keywords: list[str] | None = None, auto_embed: bool = True) -> dict:
    ensure_feed_file()
    entry = {
        'id': uuid.uuid4().hex,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'source_type': source_type,
        'source_name': source_name,
        'subject_id': subject_id,
        'subiect_id': subiect_id,
        'chapter_id': chapter_id,
        'title': title.strip() or 'Notiță fără titlu',
        'text': text.strip(),
        'keywords': keywords or tokenize(f"{title} {text}")[:20],
    }
    with FEED_PATH.open('a', encoding='utf-8') as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + '\n')
    if auto_embed:
        vector = embed_text(entry['text'])
        if vector:
            _set_vector(entry['id'], vector)
    return entry


def chunk_text(text: str, chunk_size: int = 1400, overlap: int = 180) -> list[str]:
    cleaned = re.sub(r'\s+', ' ', text).strip()
    if not cleaned:
        return []
    chunks = []
    start = 0
    while start < len(cleaned):
        end = min(len(cleaned), start + chunk_size)
        piece = cleaned[start:end]
        if end < len(cleaned):
            last_break = max(piece.rfind('. '), piece.rfind('; '), piece.rfind(' '))
            if last_break > int(chunk_size * 0.55):
                piece = piece[:last_break + 1]
                end = start + len(piece)
        chunks.append(piece.strip())
        if end >= len(cleaned):
            break
        start = max(0, end - overlap)
    return [chunk for chunk in chunks if chunk]


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ''
        text = text.strip()
        if text:
            pages.append(f"[Pagina {index}] {text}")
    return '\n\n'.join(pages)


def import_pdf(pdf_path: str | Path, title_prefix: str | None = None, subject_id: str = '',
               subiect_id: str = '', chapter_id: str = '', source_name: str | None = None) -> list[dict]:
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    created = []
    if not chunks:
        return created
    vectors = embed_texts(chunks)
    for index, chunk in enumerate(chunks, start=1):
        title = title_prefix or Path(pdf_path).stem
        entry = append_note(
            title=f"{title} · fragment {index}",
            text=chunk,
            subject_id=subject_id,
            subiect_id=subiect_id,
            chapter_id=chapter_id,
            source_type='pdf_import',
            source_name=source_name or Path(pdf_path).name,
            auto_embed=False,
        )
        if vectors and index - 1 < len(vectors):
            _set_vector(entry['id'], vectors[index - 1])
        created.append(entry)
    return created


def _score_entry(entry: dict, query_tokens: Iterable[str], subject_id: str = '',
                 subiect_id: str = '', chapter_id: str = '') -> int:
    score = 0
    if subject_id and entry.get('subject_id') == subject_id:
        score += 6
    if subiect_id and entry.get('subiect_id') == subiect_id:
        score += 5
    if chapter_id and entry.get('chapter_id') == chapter_id:
        score += 9
    haystack = ' '.join([
        entry.get('title', ''),
        entry.get('text', ''),
        ' '.join(entry.get('keywords', [])),
        entry.get('source_name', ''),
    ]).lower()
    for token in query_tokens:
        if token in haystack:
            score += 2
    if entry.get('source_type') == 'pdf_import':
        score += 1
    return score


def _dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def _norm(a: list[float]) -> float:
    return math.sqrt(sum(x * x for x in a))


def _cosine(a: list[float], b: list[float]) -> float:
    denom = _norm(a) * _norm(b)
    if not denom:
        return 0.0
    return _dot(a, b) / denom


def search_knowledge(query: str, subject_id: str = '', subiect_id: str = '',
                     chapter_id: str = '', limit: int = 5) -> list[dict]:
    tokens = tokenize(query)
    entries = load_entries()
    vectors = load_vectors().get('vectors', {})
    query_vector = embed_text(query)
    scored = []
    for entry in entries:
        if subject_id and entry.get('subject_id') and entry.get('subject_id') != subject_id:
            continue
        if subiect_id and entry.get('subiect_id') and entry.get('subiect_id') != subiect_id:
            continue
        if chapter_id and entry.get('chapter_id') and entry.get('chapter_id') != chapter_id:
            continue
        lexical = _score_entry(entry, tokens, subject_id=subject_id, subiect_id=subiect_id, chapter_id=chapter_id)
        semantic = 0.0
        entry_vector = vectors.get(entry.get('id', ''))
        if query_vector and isinstance(entry_vector, list):
            semantic = _cosine(query_vector, entry_vector)
        combined = lexical + semantic * 12
        if combined > 0:
            snippet = entry.get('text', '')
            item = dict(entry)
            item['score'] = round(combined, 4)
            item['semantic_score'] = round(semantic, 4)
            item['snippet'] = snippet[:280] + ('…' if len(snippet) > 280 else '')
            scored.append(item)
    scored.sort(key=lambda item: (item['score'], item.get('timestamp', '')), reverse=True)
    return scored[:limit]


def list_recent_entries(limit: int = 12) -> list[dict]:
    entries = load_entries()
    entries.sort(key=lambda item: item.get('timestamp', ''), reverse=True)
    return entries[:limit]


def rebuild_missing_embeddings(limit: int | None = None) -> dict:
    entries = load_entries()
    vectors = load_vectors()
    mapping = vectors.setdefault('vectors', {})
    missing = [entry for entry in entries if entry.get('id') not in mapping and entry.get('text')]
    if limit is not None:
        missing = missing[:limit]
    texts = [entry['text'] for entry in missing]
    created = 0
    if texts:
        batch_vectors = embed_texts(texts)
        if batch_vectors:
            for entry, vector in zip(missing, batch_vectors):
                mapping[entry['id']] = vector
                created += 1
            save_vectors(vectors)
    return {
        'created': created,
        'entries': len(entries),
        'indexed': len(mapping),
        'healthy': get_ollama_status().get('healthy', False),
    }


def vector_stats() -> dict:
    entries = load_entries()
    vectors = load_vectors().get('vectors', {})
    return {
        'entries': len(entries),
        'indexed': len(vectors),
        'healthy': get_ollama_status().get('healthy', False),
    }
