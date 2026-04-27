from __future__ import annotations

from .exam_bank_service import get_quiz_length, pick_adaptive_exam_items
from .math_text_service import format_math_text_html

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
        raw_options = [str(option) for option in item.get('options', [])]
        correct_index = int(item.get('correct_index', 0))
        options = [{'value': option, 'label': format_math_text_html(option)} for option in raw_options]
        correct_value = raw_options[correct_index] if raw_options else ''
        correct_label = options[correct_index]['label'] if options else ''
        questions.append({
            'id': f'q{index:02d}',
            'item_id': item.get('id', f'item-{index:02d}'),
            'number': index,
            'prompt': item.get('prompt', ''),
            'prompt_html': format_math_text_html(item.get('prompt', '')),
            'options': options,
            'correct': correct_value,
            'correct_label': correct_label,
            'correct_index': correct_index,
            'explanation': item.get('explanation', ''),
            'explanation_html': format_math_text_html(item.get('explanation', '')),
            'hint': item.get('hint', ''),
            'hint_html': format_math_text_html(item.get('hint', '')),
            'worked_steps': item.get('worked_steps', []),
            'worked_steps_html': [format_math_text_html(step) for step in item.get('worked_steps', [])],
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
            'prompt': question.get('prompt', ''),
            'prompt_html': question.get('prompt_html') or format_math_text_html(question.get('prompt', '')),
            'selected': selected,
            'selected_html': format_math_text_html(selected) if selected else '',
            'correct': question.get('correct', ''),
            'correct_html': question.get('correct_label') or format_math_text_html(question.get('correct', '')),
            'is_correct': is_correct,
            'explanation': question.get('explanation', ''),
            'explanation_html': question.get('explanation_html') or format_math_text_html(question.get('explanation', '')),
            'hint': question.get('hint', ''),
            'hint_html': question.get('hint_html') or format_math_text_html(question.get('hint', '')),
            'worked_steps': question.get('worked_steps', []),
            'worked_steps_html': question.get('worked_steps_html') or [format_math_text_html(step) for step in question.get('worked_steps', [])],
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
