from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
FORMULA_PATTERN = 'math_m1_subiect*_formulas.json'


@lru_cache(maxsize=1)
def _load_formula_index() -> dict[tuple[str, str, str], dict]:
    index: dict[tuple[str, str, str], dict] = {}
    for path in sorted(DATA_DIR.glob(FORMULA_PATTERN)):
        with path.open(encoding='utf-8') as fh:
            payload = json.load(fh)
        subject_id = payload.get('subject_id', '')
        subiect_id = payload.get('subiect_id', '')
        for chapter in payload.get('chapters', []):
            chapter_id = chapter.get('chapter_id', '')
            if not (subject_id and subiect_id and chapter_id):
                continue
            index[(subject_id, subiect_id, chapter_id)] = {
                'title': chapter.get('title', ''),
                'formulas': chapter.get('formulas', []),
                'tips': chapter.get('tips', []),
            }
    return index


def refresh_formula_sheet_cache() -> None:
    _load_formula_index.cache_clear()


def get_formula_sheet(subject_id: str, subiect_id: str, chapter_id: str) -> dict | None:
    sheet = _load_formula_index().get((subject_id, subiect_id, chapter_id))
    if not sheet:
        return None
    return {
        'title': sheet.get('title', ''),
        'formulas': list(sheet.get('formulas', [])),
        'tips': list(sheet.get('tips', [])),
    }
