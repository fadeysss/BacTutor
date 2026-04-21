from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .content_store import append_note, extract_text_from_pdf

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
CUSTOM_PATH = DATA_DIR / 'custom_lessons.json'


def load_lessons() -> list[dict]:
    if not CUSTOM_PATH.exists():
        return []
    with CUSTOM_PATH.open(encoding='utf-8') as fh:
        payload = json.load(fh)
    lessons = payload.get('lessons', [])
    lessons.sort(key=lambda item: item.get('created_at', ''), reverse=True)
    return lessons


def save_lessons(lessons: list[dict]) -> None:
    CUSTOM_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CUSTOM_PATH.open('w', encoding='utf-8') as fh:
        json.dump({'lessons': lessons}, fh, ensure_ascii=False, indent=2)


def add_text_lesson(title: str, text: str, source_label: str = 'text lipit manual') -> dict:
    lessons = load_lessons()
    lesson = {
        'id': uuid.uuid4().hex,
        'title': title.strip() or 'Lecție personală',
        'text': text.strip(),
        'excerpt': text.strip()[:260] + ('…' if len(text.strip()) > 260 else ''),
        'source_type': 'text',
        'source_label': source_label,
        'created_at': datetime.now(timezone.utc).isoformat(),
    }
    lessons.append(lesson)
    save_lessons(lessons)
    append_note(
        title=lesson['title'],
        text=lesson['text'],
        subject_id='custom',
        source_type='custom_lesson',
        source_name=source_label,
    )
    return lesson


def add_pdf_lesson(title: str, pdf_path: str | Path) -> dict:
    text = extract_text_from_pdf(pdf_path)
    lesson_title = title.strip() or Path(pdf_path).stem
    return add_text_lesson(lesson_title, text, source_label=f'PDF personal: {Path(pdf_path).name}')


def get_lesson(lesson_id: str) -> dict | None:
    for lesson in load_lessons():
        if lesson['id'] == lesson_id:
            return lesson
    return None
