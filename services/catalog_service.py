from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
CATALOG_PATH = DATA_DIR / 'catalog.json'
LEGACY_SUBJECT_ALIASES = {'matematica_m2': 'matematica_m1'}


def canonical_subject_id(subject_id: str) -> str:
    return LEGACY_SUBJECT_ALIASES.get(subject_id, subject_id)


@lru_cache(maxsize=1)
def load_catalog() -> dict:
    with CATALOG_PATH.open(encoding='utf-8') as fh:
        return json.load(fh)


def refresh_catalog_cache() -> None:
    load_catalog.cache_clear()


def list_subjects() -> list[dict]:
    return load_catalog().get('subjects', [])


def get_subject(subject_id: str) -> dict | None:
    subject_id = canonical_subject_id(subject_id)
    for subject in list_subjects():
        if subject['id'] == subject_id:
            return subject
    return None


def get_subiect(subject_id: str, subiect_id: str) -> dict | None:
    subject = get_subject(subject_id)
    if not subject:
        return None
    for subiect in subject.get('subiecte', []):
        if subiect['id'] == subiect_id:
            return subiect
    return None


def get_chapter(subject_id: str, subiect_id: str, chapter_id: str) -> dict | None:
    subiect = get_subiect(subject_id, subiect_id)
    if not subiect:
        return None
    for chapter in subiect.get('chapters', []):
        if chapter['id'] == chapter_id:
            return chapter
    return None


def flatten_subject_chapters(subject: dict) -> list[dict]:
    rows = []
    for subiect in subject.get('subiecte', []):
        for chapter in subiect.get('chapters', []):
            rows.append({'subiect': subiect, 'chapter': chapter})
    return rows


def flat_catalog_options() -> list[dict]:
    options = []
    for subject in list_subjects():
        options.append({
            'label': f"{subject['title']} · Materie (general)",
            'value': f"{subject['id']}||",
        })
        for subiect in subject.get('subiecte', []):
            options.append({
                'label': f"{subject['title']} · {subiect['title']} (general)",
                'value': f"{subject['id']}|{subiect['id']}|",
            })
            for chapter in subiect.get('chapters', []):
                options.append({
                    'label': f"{subject['title']} · {subiect['title']} · {chapter['title']}",
                    'value': f"{subject['id']}|{subiect['id']}|{chapter['id']}",
                })
    return options
