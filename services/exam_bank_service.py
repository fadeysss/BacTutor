from __future__ import annotations

import json
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from random import Random

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
BANK_PATH = DATA_DIR / 'exam_bank.json'

LEVEL_TO_DIFFICULTY = {
    'Începător': 'beginner',
    'Intermediar': 'intermediate',
    'Avansat': 'advanced',
}

DIFFICULTY_ORDER = {'beginner': 0, 'intermediate': 1, 'advanced': 2}
DEFAULT_QUIZ_LENGTH = 1
MATH_M1_QUIZ_LENGTH = 20


@lru_cache(maxsize=1)
def load_exam_bank() -> dict:
    if not BANK_PATH.exists():
        return {'items': []}
    with BANK_PATH.open(encoding='utf-8') as fh:
        return json.load(fh)


def refresh_exam_bank_cache() -> None:
    load_exam_bank.cache_clear()


def list_exam_items(subject_id: str, subiect_id: str, chapter_id: str) -> list[dict]:
    items = []
    for item in load_exam_bank().get('items', []):
        if (
            item.get('subject_id') == subject_id
            and item.get('subiect_id') == subiect_id
            and item.get('chapter_id') == chapter_id
        ):
            items.append(item)
    return items


def get_quiz_length(subject_id: str, chapter_id: str = '') -> int:
    if subject_id == 'matematica_m1':
        return MATH_M1_QUIZ_LENGTH
    return DEFAULT_QUIZ_LENGTH


def _pick_target_difficulty(student_level: str, chapter_stats: dict | None = None) -> str:
    stats = chapter_stats or {}
    last_score = int(stats.get('last_score', 0) or 0)
    attempts = int(stats.get('attempts', 0) or 0)
    if attempts == 0:
        return LEVEL_TO_DIFFICULTY.get(student_level, 'beginner')
    if last_score >= 85:
        return 'advanced' if student_level == 'Avansat' else 'intermediate'
    if last_score >= 65:
        return 'intermediate'
    return 'beginner'


def _difficulty_plan(student_level: str, count: int) -> dict[str, int]:
    if count <= 1:
        return {LEVEL_TO_DIFFICULTY.get(student_level, 'beginner'): 1}

    if student_level == 'Avansat':
        weights = {'beginner': 0.2, 'intermediate': 0.45, 'advanced': 0.35}
    elif student_level == 'Intermediar':
        weights = {'beginner': 0.3, 'intermediate': 0.5, 'advanced': 0.2}
    else:
        weights = {'beginner': 0.45, 'intermediate': 0.4, 'advanced': 0.15}

    plan = {key: int(round(count * value)) for key, value in weights.items()}
    total = sum(plan.values())
    if total < count:
        ordered = ['intermediate', 'beginner', 'advanced']
        index = 0
        while total < count:
            plan[ordered[index % len(ordered)]] += 1
            total += 1
            index += 1
    elif total > count:
        ordered = ['advanced', 'intermediate', 'beginner']
        index = 0
        while total > count:
            key = ordered[index % len(ordered)]
            if plan[key] > 0:
                plan[key] -= 1
                total -= 1
            index += 1
    return plan


def _sort_items_for_quiz(items: list[dict], student_level: str) -> list[dict]:
    def sort_key(item: dict) -> tuple[int, int, str, str]:
        difficulty_rank = DIFFICULTY_ORDER.get(item.get('difficulty', 'intermediate'), 1)
        bac_slot = item.get('bac_slot', '')
        year = int(item.get('year', 0) or 0)
        prompt = item.get('prompt', '')
        return (difficulty_rank, year, bac_slot, prompt)

    ordered = sorted(items, key=sort_key)
    if student_level == 'Avansat':
        return ordered[4:] + ordered[:4] if len(ordered) > 8 else ordered
    if student_level == 'Intermediar':
        return ordered[2:] + ordered[:2] if len(ordered) > 6 else ordered
    return ordered


def pick_adaptive_exam_items(
    subject_id: str,
    subiect_id: str,
    chapter_id: str,
    student_level: str,
    chapter_stats: dict | None = None,
    limit: int | None = None,
) -> list[dict]:
    candidates = list_exam_items(subject_id, subiect_id, chapter_id)
    if not candidates:
        return []

    target_count = limit or get_quiz_length(subject_id, chapter_id)
    if len(candidates) <= target_count:
        return _sort_items_for_quiz(candidates, student_level)

    target_difficulty = _pick_target_difficulty(student_level, chapter_stats)
    plan = _difficulty_plan(student_level, target_count)
    ranked_groups: dict[str, list[dict]] = defaultdict(list)
    for item in candidates:
        ranked_groups[item.get('difficulty', 'intermediate')].append(item)

    for difficulty in ranked_groups:
        ranked_groups[difficulty] = sorted(
            ranked_groups[difficulty],
            key=lambda item: (
                abs(DIFFICULTY_ORDER.get(item.get('difficulty', 'intermediate'), 1) - DIFFICULTY_ORDER[target_difficulty]),
                -int(item.get('year', 0) or 0),
                item.get('bac_slot', ''),
                item.get('prompt', ''),
            ),
        )

    picked: list[dict] = []
    used_ids: set[str] = set()
    for difficulty in ['beginner', 'intermediate', 'advanced']:
        needed = plan.get(difficulty, 0)
        for item in ranked_groups.get(difficulty, []):
            if needed <= 0:
                break
            item_id = item.get('id', '')
            if item_id in used_ids:
                continue
            used_ids.add(item_id)
            picked.append(item)
            needed -= 1

    if len(picked) < target_count:
        fallback_sorted = sorted(
            candidates,
            key=lambda item: (
                abs(DIFFICULTY_ORDER.get(item.get('difficulty', 'intermediate'), 1) - DIFFICULTY_ORDER[target_difficulty]),
                -int(item.get('year', 0) or 0),
                item.get('bac_slot', ''),
                item.get('prompt', ''),
            ),
        )
        seed_base = f"{subject_id}:{subiect_id}:{chapter_id}:{student_level}:{chapter_stats or {}}"
        rnd = Random(seed_base)
        remainder = [item for item in fallback_sorted if item.get('id', '') not in used_ids]
        if remainder:
            rnd.shuffle(remainder)
        for item in remainder:
            if len(picked) >= target_count:
                break
            picked.append(item)

    return _sort_items_for_quiz(picked[:target_count], student_level)


def pick_adaptive_exam_item(subject_id: str, subiect_id: str, chapter_id: str, student_level: str,
                            chapter_stats: dict | None = None) -> dict | None:
    items = pick_adaptive_exam_items(
        subject_id=subject_id,
        subiect_id=subiect_id,
        chapter_id=chapter_id,
        student_level=student_level,
        chapter_stats=chapter_stats,
        limit=1,
    )
    return items[0] if items else None


def exam_bank_count() -> int:
    return len(load_exam_bank().get('items', []))


def add_exam_item(item: dict) -> dict:
    payload = load_exam_bank()
    items = payload.setdefault('items', [])
    items.append(item)
    BANK_PATH.parent.mkdir(parents=True, exist_ok=True)
    with BANK_PATH.open('w', encoding='utf-8') as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    refresh_exam_bank_cache()
    return item
