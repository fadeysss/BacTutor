from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
PROGRESS_PATH = DATA_DIR / 'progress.json'


def load_progress() -> dict:
    if not PROGRESS_PATH.exists():
        return {'students': {}}
    with PROGRESS_PATH.open(encoding='utf-8') as fh:
        return json.load(fh)


def save_progress(payload: dict) -> None:
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PROGRESS_PATH.open('w', encoding='utf-8') as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)


def ensure_student_id(session) -> str:
    student_id = session.get('student_id')
    if not student_id:
        student_id = uuid.uuid4().hex
        session['student_id'] = student_id
    return student_id


def _default_student() -> dict:
    return {
        'xp': 0,
        'quizzes_taken': 0,
        'average_score': 0.0,
        'chapters_viewed': [],
        'subjects': {},
        'recent_activity': [],
        'created_at': datetime.now(timezone.utc).isoformat(),
    }


def get_student(student_id: str) -> dict:
    payload = load_progress()
    students = payload.setdefault('students', {})
    if student_id not in students:
        students[student_id] = _default_student()
        save_progress(payload)
    return students[student_id]


def level_from_xp(xp: int) -> str:
    if xp >= 220:
        return 'Avansat'
    if xp >= 90:
        return 'Intermediar'
    return 'Începător'


def xp_to_next_level(xp: int) -> int:
    if xp < 90:
        return 90 - xp
    if xp < 220:
        return 220 - xp
    return 0


def mark_view(student_id: str, subject_id: str, subiect_id: str, chapter_id: str) -> None:
    payload = load_progress()
    student = payload.setdefault('students', {}).setdefault(student_id, _default_student())
    key = f"{subject_id}:{subiect_id}:{chapter_id}"
    if key not in student['chapters_viewed']:
        student['chapters_viewed'].append(key)
    student['recent_activity'] = ([{
        'type': 'lesson_view',
        'subject_id': subject_id,
        'subiect_id': subiect_id,
        'chapter_id': chapter_id,
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }] + student.get('recent_activity', []))[:18]
    save_progress(payload)


def record_quiz(student_id: str, subject_id: str, subiect_id: str, chapter_id: str, score: int, total: int) -> dict:
    payload = load_progress()
    student = payload.setdefault('students', {}).setdefault(student_id, _default_student())
    percent = round((score / total) * 100) if total else 0
    xp_gain = 10 + score * 8
    student['xp'] += xp_gain

    quizzes_taken_before = student.get('quizzes_taken', 0)
    student['quizzes_taken'] = quizzes_taken_before + 1
    previous_average = student.get('average_score', 0.0)
    student['average_score'] = round(((previous_average * quizzes_taken_before) + percent) / student['quizzes_taken'], 1)

    subject = student.setdefault('subjects', {}).setdefault(subject_id, {
        'quizzes_taken': 0,
        'average_score': 0.0,
        'chapters': {},
    })
    subject_quizzes_before = subject.get('quizzes_taken', 0)
    subject['quizzes_taken'] = subject_quizzes_before + 1
    subject['average_score'] = round(((subject.get('average_score', 0.0) * subject_quizzes_before) + percent) / subject['quizzes_taken'], 1)

    chapter = subject.setdefault('chapters', {}).setdefault(chapter_id, {
        'attempts': 0,
        'best_score': 0,
        'last_score': 0,
        'subiect_id': subiect_id,
    })
    chapter['attempts'] += 1
    chapter['last_score'] = percent
    chapter['best_score'] = max(chapter.get('best_score', 0), percent)
    chapter['updated_at'] = datetime.now(timezone.utc).isoformat()
    chapter['subiect_id'] = subiect_id

    key = f"{subject_id}:{subiect_id}:{chapter_id}"
    if key not in student['chapters_viewed']:
        student['chapters_viewed'].append(key)

    student['recent_activity'] = ([{
        'type': 'quiz',
        'subject_id': subject_id,
        'subiect_id': subiect_id,
        'chapter_id': chapter_id,
        'score': percent,
        'xp_gain': xp_gain,
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }] + student.get('recent_activity', []))[:18]
    save_progress(payload)
    return {
        'xp_gain': xp_gain,
        'percent': percent,
        'level': level_from_xp(student['xp']),
        'xp_to_next_level': xp_to_next_level(student['xp']),
    }


def summarize_student(student_id: str, subjects: list[dict]) -> dict:
    student = get_student(student_id)
    summary = {
        'xp': student.get('xp', 0),
        'level': level_from_xp(student.get('xp', 0)),
        'xp_to_next_level': xp_to_next_level(student.get('xp', 0)),
        'quizzes_taken': student.get('quizzes_taken', 0),
        'average_score': student.get('average_score', 0.0),
        'chapters_viewed_count': len(student.get('chapters_viewed', [])),
        'recent_activity': student.get('recent_activity', []),
        'subjects': [],
    }
    total_chapters = 0
    completed_chapters = 0
    weak_spots = []
    for subject in subjects:
        subject_total = sum(len(subiect.get('chapters', [])) for subiect in subject.get('subiecte', []))
        total_chapters += subject_total
        student_subject = student.get('subjects', {}).get(subject['id'], {})
        chapters = student_subject.get('chapters', {})
        completed = sum(1 for item in chapters.values() if item.get('best_score', 0) >= 70)
        completed_chapters += completed
        avg = student_subject.get('average_score', 0.0)
        subject_summary = {
            'id': subject['id'],
            'title': subject['title'],
            'short_title': subject.get('short_title', subject['title']),
            'completed': completed,
            'total': subject_total,
            'average_score': avg,
            'quizzes_taken': student_subject.get('quizzes_taken', 0),
            'progress_percent': round((completed / subject_total) * 100) if subject_total else 0,
        }
        summary['subjects'].append(subject_summary)
        for chapter_id, chapter_stats in chapters.items():
            weak_spots.append({
                'subject_id': subject['id'],
                'chapter_id': chapter_id,
                'score': chapter_stats.get('last_score', 0),
                'subiect_id': chapter_stats.get('subiect_id', ''),
            })
    summary['overall_completion_percent'] = round((completed_chapters / total_chapters) * 100) if total_chapters else 0
    weak_spots.sort(key=lambda item: item['score'])
    summary['weak_spots'] = weak_spots[:3]
    return summary
