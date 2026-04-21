from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
EXAMPLES_PATH = DATA_DIR / 'chapter_examples.json'


@lru_cache(maxsize=1)
def load_examples() -> dict:
    if not EXAMPLES_PATH.exists():
        return {'items': []}
    with EXAMPLES_PATH.open(encoding='utf-8') as fh:
        return json.load(fh)


def refresh_examples_cache() -> None:
    load_examples.cache_clear()


def get_chapter_example(subject_id: str, subiect_id: str, chapter_id: str) -> dict | None:
    for item in load_examples().get('items', []):
        if (
            item.get('subject_id') == subject_id
            and item.get('subiect_id') == subiect_id
            and item.get('chapter_id') == chapter_id
        ):
            return item
    return None
