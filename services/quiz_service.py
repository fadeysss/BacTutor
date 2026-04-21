from __future__ import annotations

from .exam_bank_service import get_quiz_length, pick_adaptive_exam_items

DIFFICULTY_LABELS = {
    'beginner': 'bază',
    'intermediate': 'standard M1',
    'advanced': 'tricky',
}


def build_quiz(subject: dict, subiect: dict, chapter: dict, student_level: str = 'Începător',
               chapter_stats: dict | None = None) -> list[dict]:
    items = pick_adaptive_exam_items(
        subject_id=subject.get('id', ''),
        subiect_id=subiect.get('id', ''),
        chapter_id=chapter.get('id', ''),
        student_level=student_level,
        chapter_stats=chapter_stats,
        limit=get_quiz_length(subject.get('id', ''), chapter.get('id', '')),
    )
    questions = []
    for index, item in enumerate(items, start=1):
        options = item['options']
        correct_index = int(item['correct_index'])
        questions.append({
            'id': f'q{index:02d}',
            'item_id': item.get('id', f'item-{index:02d}'),
            'number': index,
            'prompt': item['prompt'],
            'options': options,
            'correct': options[correct_index],
            'correct_index': correct_index,
            'explanation': item['explanation'],
            'hint': item.get('hint', ''),
            'worked_steps': item.get('worked_steps', []),
            'source_label': item.get('source_label', ''),
            'source_type': item.get('source_type', ''),
            'source_year': item.get('year'),
            'difficulty': item.get('difficulty', 'intermediate'),
            'difficulty_label': DIFFICULTY_LABELS.get(item.get('difficulty', 'intermediate'), 'standard'),
            'tags': item.get('tags', []),
            'bac_slot': item.get('bac_slot', ''),
        })
    return questions


def grade_quiz(questions: list[dict], answers: dict) -> dict:
    score = 0
    details = []
    for question in questions:
        selected = answers.get(question['id'], '')
        is_correct = selected == question['correct']
        score += int(is_correct)
        details.append({
            'number': question.get('number', 0),
            'prompt': question['prompt'],
            'selected': selected,
            'correct': question['correct'],
            'is_correct': is_correct,
            'explanation': question['explanation'],
            'hint': question.get('hint', ''),
            'worked_steps': question.get('worked_steps', []),
            'source_label': question.get('source_label', ''),
            'source_year': question.get('source_year'),
            'difficulty': question.get('difficulty', 'intermediate'),
            'difficulty_label': question.get('difficulty_label', 'standard'),
            'bac_slot': question.get('bac_slot', ''),
        })
    total = len(questions)
    percent = round((score / total) * 100) if total else 0
    if percent < 50:
        recommendation = 'Revino la exemplul lucrat, reține capcanele și reia încă o dată acest set M1.'
    elif percent < 80:
        recommendation = 'Baza este bună. Fixează itemii greșiți și reia capitolul pentru a stabiliza viteza de examen.'
    elif percent < 95:
        recommendation = 'Foarte bine. Mai ai nevoie de puțină finețe pe itemii greșiți ca să urci spre 10.'
    else:
        recommendation = 'Excelent. Capitolul este aproape la nivel de examen. Poți cere acum variante mai tricky sau trece la capitolul următor.'
    return {
        'score': score,
        'total': total,
        'percent': percent,
        'details': details,
        'recommendation': recommendation,
    }
