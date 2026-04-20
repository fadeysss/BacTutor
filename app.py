from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

from services.catalog_service import flat_catalog_options, get_chapter, get_subject, get_subiect, list_subjects
from services.content_store import append_note, import_pdf, list_recent_entries
from services.custom_lesson_service import add_pdf_lesson, add_text_lesson, get_lesson, load_lessons
from services.lesson_service import (
    answer_personal_question,
    answer_question,
    build_lesson_bundle,
    build_personal_lesson_bundle,
)
from services.progress_service import ensure_student_id, get_student, mark_view, record_quiz, summarize_student
from services.quiz_service import build_quiz, grade_quiz

ROOT = Path(__file__).resolve().parent
UPLOAD_DIR = ROOT / 'uploads'
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'bactutor-dev-secret')
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024


def parse_binding(raw_value: str) -> tuple[str, str, str]:
    parts = (raw_value or '').split('|')
    while len(parts) < 3:
        parts.append('')
    return parts[0], parts[1], parts[2]


@app.context_processor
def inject_globals():
    return {'catalog_flat': flat_catalog_options()}


@app.route('/')
def home():
    student_id = ensure_student_id(session)
    subjects = list_subjects()
    student_summary = summarize_student(student_id, subjects)
    return render_template('home.html', title='Bac Tutor', subjects=subjects, student_summary=student_summary)


@app.route('/dashboard')
def dashboard():
    student_id = ensure_student_id(session)
    subjects = list_subjects()
    student_summary = summarize_student(student_id, subjects)
    weak_spot_links = []
    for spot in student_summary.get('weak_spots', []):
        subject = get_subject(spot['subject_id'])
        subiect_id = spot.get('subiect_id', '')
        chapter_id = spot.get('chapter_id', '')
        chapter = get_chapter(spot['subject_id'], subiect_id, chapter_id) if subiect_id and chapter_id else None
        if subject and subiect_id and chapter:
            weak_spot_links.append({
                'label': f"{subject.get('short_title', subject['title'])} · {chapter['title']}",
                'score': spot.get('score', 0),
                'url': url_for('lesson_page', subject_id=subject['id'], subiect_id=subiect_id, chapter_id=chapter_id),
            })
    return render_template(
        'dashboard.html',
        title='Progres · Bac Tutor',
        student_summary=student_summary,
        weak_spot_links=weak_spot_links,
    )


@app.route('/subject/<subject_id>')
def subject_page(subject_id: str):
    student_id = ensure_student_id(session)
    subject = get_subject(subject_id)
    if not subject:
        flash('Materia cerută nu există.', 'error')
        return redirect(url_for('home'))
    student = get_student(student_id)
    overall_summary = summarize_student(student_id, list_subjects())
    subject_summary = next((item for item in overall_summary['subjects'] if item['id'] == subject_id), {
        'progress_percent': 0,
        'average_score': 0.0,
    })
    chapter_lookup = student.get('subjects', {}).get(subject_id, {}).get('chapters', {})
    total_chapters = sum(len(subiect.get('chapters', [])) for subiect in subject.get('subiecte', []))
    return render_template(
        'subject.html',
        title=f"{subject['title']} · Bac Tutor",
        subject=subject,
        subject_progress=subject_summary,
        total_chapters=total_chapters,
        chapter_lookup=chapter_lookup,
    )


@app.route('/lesson/<subject_id>/<subiect_id>/<chapter_id>', methods=['GET', 'POST'])
def lesson_page(subject_id: str, subiect_id: str, chapter_id: str):
    student_id = ensure_student_id(session)
    subject = get_subject(subject_id)
    subiect = get_subiect(subject_id, subiect_id)
    chapter = get_chapter(subject_id, subiect_id, chapter_id)
    if not (subject and subiect and chapter):
        flash('Capitolul cerut nu există.', 'error')
        return redirect(url_for('home'))

    student_summary = summarize_student(student_id, list_subjects())
    mark_view(student_id, subject_id, subiect_id, chapter_id)
    lesson = build_lesson_bundle(subject, subiect, chapter, student_summary['level'])
    quiz_questions = build_quiz(subject, subiect, chapter)
    tutor_answer = None
    quiz_result = None
    asked_question = ''

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'ask':
            asked_question = request.form.get('question', '').strip()
            if asked_question:
                tutor_answer = answer_question(subject, subiect, chapter, asked_question, student_summary['level'])
            else:
                flash('Scrie o întrebare înainte să ceri explicația.', 'error')
        elif action == 'quiz':
            quiz_result = grade_quiz(quiz_questions, request.form)
            xp_update = record_quiz(student_id, subject_id, subiect_id, chapter_id, quiz_result['score'], quiz_result['total'])
            quiz_result.update(xp_update)
            student_summary = summarize_student(student_id, list_subjects())
            flash('Quiz evaluat. Progresul a fost salvat.', 'success')

    return render_template(
        'lesson.html',
        title=f"{chapter['title']} · Bac Tutor",
        lesson=lesson,
        tutor_answer=tutor_answer,
        asked_question=asked_question,
        quiz_questions=quiz_questions,
        quiz_result=quiz_result,
        student_summary=student_summary,
    )


@app.route('/custom-lesson', methods=['GET', 'POST'])
def custom_lesson():
    ensure_student_id(session)
    custom_answer = None
    custom_question = ''
    selected_lesson = None
    lesson_bundle = None

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'save_lesson':
            title = request.form.get('title', '').strip()
            lesson_text = request.form.get('lesson_text', '').strip()
            pdf_file = request.files.get('lesson_pdf')
            if lesson_text:
                created = add_text_lesson(title, lesson_text)
                flash('Lecția personală a fost salvată.', 'success')
                return redirect(url_for('custom_lesson', lesson_id=created['id']))
            if pdf_file and pdf_file.filename:
                filename = secure_filename(pdf_file.filename)
                target = UPLOAD_DIR / filename
                pdf_file.save(target)
                created = add_pdf_lesson(title, target)
                flash('PDF-ul personal a fost importat.', 'success')
                return redirect(url_for('custom_lesson', lesson_id=created['id']))
            flash('Adaugă textul lecției sau încarcă un PDF.', 'error')
        elif action == 'ask_custom':
            lesson_id = request.form.get('lesson_id', '')
            selected_lesson = get_lesson(lesson_id)
            custom_question = request.form.get('custom_question', '').strip()
            if selected_lesson and custom_question:
                custom_answer = answer_personal_question(selected_lesson['title'], selected_lesson['text'], custom_question)
            elif not custom_question:
                flash('Scrie o întrebare pentru lecția selectată.', 'error')

    lessons = load_lessons()
    lesson_id = request.args.get('lesson_id') or request.form.get('lesson_id')
    if not selected_lesson and lesson_id:
        selected_lesson = get_lesson(lesson_id)
    if selected_lesson:
        lesson_bundle = build_personal_lesson_bundle(selected_lesson['title'], selected_lesson['text'])

    return render_template(
        'custom_lesson.html',
        title='Lecție personală · Bac Tutor',
        lessons=lessons,
        selected_lesson=selected_lesson,
        lesson_bundle=lesson_bundle,
        custom_answer=custom_answer,
        custom_question=custom_question,
    )


@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    ensure_student_id(session)
    if request.method == 'POST':
        action = request.form.get('action')
        subject_id, subiect_id, chapter_id = parse_binding(request.form.get('catalog_binding', ''))
        if action == 'add_note':
            title = request.form.get('title', '').strip()
            note_text = request.form.get('note_text', '').strip()
            if not title or not note_text:
                flash('Completează titlul și conținutul notiței.', 'error')
            else:
                append_note(title=title, text=note_text, subject_id=subject_id, subiect_id=subiect_id, chapter_id=chapter_id)
                flash('Notița a fost adăugată în knowledge feed.', 'success')
                return redirect(url_for('admin_panel'))
        elif action == 'import_pdf':
            pdf_file = request.files.get('pdf_file')
            pdf_title = request.form.get('pdf_title', '').strip()
            if not pdf_title or not pdf_file or not pdf_file.filename:
                flash('Alege un PDF și completează un titlu.', 'error')
            else:
                filename = secure_filename(pdf_file.filename)
                target = UPLOAD_DIR / filename
                pdf_file.save(target)
                created = import_pdf(target, title_prefix=pdf_title, subject_id=subject_id, subiect_id=subiect_id, chapter_id=chapter_id)
                flash(f'PDF importat cu succes. Au fost create {len(created)} fragmente în knowledge feed.', 'success')
                return redirect(url_for('admin_panel'))

    return render_template(
        'admin.html',
        title='Knowledge Feed · Bac Tutor',
        recent_entries=list_recent_entries(12),
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000)
