from __future__ import annotations

import os
from pathlib import Path
from uuid import uuid4

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

from services.catalog_service import canonical_subject_id, flat_catalog_options, get_chapter, get_subject, get_subiect, list_subjects
from services.content_store import append_note, import_pdf, list_recent_entries, rebuild_missing_embeddings, vector_stats
from services.custom_lesson_service import add_pdf_lesson, add_text_lesson, get_lesson, load_lessons
from services.exam_bank_service import exam_bank_count
from services.lesson_service import (
    answer_personal_question,
    answer_question,
    build_lesson_bundle,
    build_personal_lesson_bundle,
)
from services.llm_service import get_ollama_status
from services.progress_service import ensure_student_id, get_student, mark_view, record_quiz, summarize_student
from services.quiz_service import build_quiz, grade_quiz

ROOT = Path(__file__).resolve().parent
UPLOAD_DIR = ROOT / 'uploads'
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_PDF_MIME_TYPES = {'application/pdf', 'application/x-pdf', 'application/octet-stream'}

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or os.urandom(32).hex()
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024


def parse_binding(raw_value: str) -> tuple[str, str, str]:
    parts = (raw_value or '').split('|')
    while len(parts) < 3:
        parts.append('')
    return parts[0], parts[1], parts[2]


def _is_pdf_signature(path: Path) -> bool:
    try:
        with path.open('rb') as fh:
            return fh.read(5) == b'%PDF-'
    except OSError:
        return False


def save_uploaded_pdf(pdf_file, prefix: str) -> Path:
    raw_filename = secure_filename((pdf_file.filename or '').strip())
    if not raw_filename:
        raise ValueError('FiÃˆâ„¢ierul selectat nu este valid.')
    if not raw_filename.lower().endswith('.pdf'):
        raise ValueError('AcceptÃ„Æ’m doar fiÃˆâ„¢iere PDF.')

    mimetype = (pdf_file.mimetype or '').lower()
    if mimetype and mimetype not in ALLOWED_PDF_MIME_TYPES:
        raise ValueError('FiÃˆâ„¢ierul ÃƒÂ®ncÃ„Æ’rcat nu pare sÃ„Æ’ fie PDF.')

    target = UPLOAD_DIR / f"{prefix}-{uuid4().hex}.pdf"
    pdf_file.save(target)
    if not _is_pdf_signature(target):
        target.unlink(missing_ok=True)
        raise ValueError('FiÃˆâ„¢ierul nu are semnÃ„Æ’turÃ„Æ’ PDF validÃ„Æ’.')
    return target


def debug_enabled() -> bool:
    return os.getenv('FLASK_DEBUG', '0') == '1'


@app.context_processor
def inject_globals():
    return {
        'catalog_flat': flat_catalog_options(),
        'global_ollama_status': get_ollama_status(),
    }


@app.errorhandler(413)
def file_too_large(_error):
    flash('FiÃˆâ„¢ierul depÃ„Æ’Ãˆâ„¢eÃˆâ„¢te limita de 20MB.', 'error')
    return redirect(request.referrer or url_for('home'))


@app.route('/')
def home():
    student_id = ensure_student_id(session)
    subjects = list_subjects()
    student_summary = summarize_student(student_id, subjects)
    recommended_start = None
    preferred_order = ['matematica_m1', 'romana_mate_info', 'informatica_mate_info']
    ordered_subjects = sorted(subjects, key=lambda item: preferred_order.index(item['id']) if item['id'] in preferred_order else len(preferred_order))
    for subject in ordered_subjects:
        subiecte = subject.get('subiecte', [])
        if not subiecte:
            continue
        chapters = subiecte[0].get('chapters', [])
        if not chapters:
            continue
        recommended_start = {
            'label': f"{subject.get('short_title', subject['title'])} · {chapters[0]['title']}",
            'url': url_for('lesson_page', subject_id=subject['id'], subiect_id=subiecte[0]['id'], chapter_id=chapters[0]['id']),
        }
        break
    return render_template(
        'home.html',
        title='Bac Tutor',
        subjects=subjects,
        student_summary=student_summary,
        recommended_start=recommended_start,
    )


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
                'label': f"{subject.get('short_title', subject['title'])} Â· {chapter['title']}",
                'score': spot.get('score', 0),
                'url': url_for('lesson_page', subject_id=subject['id'], subiect_id=subiect_id, chapter_id=chapter_id),
            })
    return render_template(
        'dashboard.html',
        title='Progres Â· Bac Tutor',
        student_summary=student_summary,
        weak_spot_links=weak_spot_links,
    )


@app.route('/subject/<subject_id>')
def subject_page(subject_id: str):
    student_id = ensure_student_id(session)
    canonical_id = canonical_subject_id(subject_id)
    if canonical_id != subject_id:
        return redirect(url_for('subject_page', subject_id=canonical_id))
    subject = get_subject(canonical_id)
    if not subject:
        flash('Materia cerutÄƒ nu existÄƒ.', 'error')
        return redirect(url_for('home'))
    student = get_student(student_id)
    overall_summary = summarize_student(student_id, list_subjects())
    subject_summary = next((item for item in overall_summary['subjects'] if item['id'] == canonical_id), {
        'progress_percent': 0,
        'average_score': 0.0,
    })
    chapter_lookup = student.get('subjects', {}).get(canonical_id, {}).get('chapters', {})
    total_chapters = sum(len(subiect.get('chapters', [])) for subiect in subject.get('subiecte', []))
    return render_template(
        'subject.html',
        title=f"{subject['title']} Â· Bac Tutor",
        subject=subject,
        subject_progress=subject_summary,
        total_chapters=total_chapters,
        chapter_lookup=chapter_lookup,
    )


@app.route('/lesson/<subject_id>/<subiect_id>/<chapter_id>', methods=['GET', 'POST'])
def lesson_page(subject_id: str, subiect_id: str, chapter_id: str):
    student_id = ensure_student_id(session)
    canonical_id = canonical_subject_id(subject_id)
    if canonical_id != subject_id:
        return redirect(url_for('lesson_page', subject_id=canonical_id, subiect_id=subiect_id, chapter_id=chapter_id))
    subject = get_subject(canonical_id)
    subiect = get_subiect(canonical_id, subiect_id)
    chapter = get_chapter(canonical_id, subiect_id, chapter_id)
    if subject and not chapter:
        for candidate_subiect in subject.get('subiecte', []):
            for candidate_chapter in candidate_subiect.get('chapters', []):
                if candidate_chapter.get('id') == chapter_id:
                    return redirect(url_for('lesson_page', subject_id=canonical_id, subiect_id=candidate_subiect['id'], chapter_id=chapter_id))
    if not (subject and subiect and chapter):
        flash('Capitolul cerut nu existÄƒ.', 'error')
        return redirect(url_for('home'))

    mark_view(student_id, canonical_id, subiect_id, chapter_id)
    student_summary = summarize_student(student_id, list_subjects())
    chapter_stats = get_student(student_id).get('subjects', {}).get(canonical_id, {}).get('chapters', {}).get(chapter_id, {})
    lesson = build_lesson_bundle(subject, subiect, chapter, student_summary['level'], chapter_stats=chapter_stats)
    quiz_questions = build_quiz(subject, subiect, chapter, student_summary['level'], chapter_stats=chapter_stats)
    tutor_answer = None
    quiz_result = None
    asked_question = ''
    submitted_answers = {}

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'ask':
            asked_question = request.form.get('question', '').strip()
            if asked_question:
                tutor_answer = answer_question(subject, subiect, chapter, asked_question, student_summary['level'])
            else:
                flash('Scrie o Ã®ntrebare Ã®nainte sÄƒ ceri explicaÈ›ia.', 'error')
        elif action == 'smart_help':
            preset = request.form.get('preset', '').strip()
            prompt_map = {
                'simplify': 'ExplicÄƒ-mi foarte simplu, ca pentru un elev care abia fixeazÄƒ ideea.',
                'example': 'DÄƒ-mi un exemplu nou, lucrat clar, pas cu pas.',
                'strategy': 'Spune-mi cum se abordeazÄƒ la bac, unde se pierde punctaj È™i ce verific la final.',
            }
            asked_question = prompt_map.get(preset, '')
            if asked_question:
                tutor_answer = answer_question(subject, subiect, chapter, asked_question, student_summary['level'])
        elif action == 'quiz':
            submitted_answers = request.form.to_dict(flat=True)
            quiz_result = grade_quiz(quiz_questions, submitted_answers)
            xp_update = record_quiz(student_id, canonical_id, subiect_id, chapter_id, quiz_result['score'], quiz_result['total'])
            quiz_result.update(xp_update)
            student_summary = summarize_student(student_id, list_subjects())
            if canonical_id == 'matematica_m1' and quiz_result['total'] > 1:
                flash('Setul M1 a fost evaluat È™i progresul a fost salvat.', 'success')
            else:
                flash('Mini-quiz evaluat. Progresul a fost salvat.', 'success')

    return render_template(
        'lesson.html',
        title=f"{chapter['title']} Â· Bac Tutor",
        lesson=lesson,
        tutor_answer=tutor_answer,
        asked_question=asked_question,
        quiz_questions=quiz_questions,
        quiz_result=quiz_result,
        submitted_answers=submitted_answers,
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
                flash('LecÈ›ia personalÄƒ a fost salvatÄƒ.', 'success')
                return redirect(url_for('custom_lesson', lesson_id=created['id']))
            if pdf_file and pdf_file.filename:
                try:
                    target = save_uploaded_pdf(pdf_file, prefix='custom-lesson')
                    created = add_pdf_lesson(title, target)
                    flash('PDF-ul personal a fost importat.', 'success')
                    return redirect(url_for('custom_lesson', lesson_id=created['id']))
                except ValueError as exc:
                    flash(str(exc), 'error')
                except Exception:
                    flash('PDF-ul nu a putut fi procesat. VerificÄƒ fiÈ™ierul È™i Ã®ncearcÄƒ din nou.', 'error')
            flash('AdaugÄƒ textul lecÈ›iei sau Ã®ncarcÄƒ un PDF.', 'error')
        elif action == 'ask_custom':
            lesson_id = request.form.get('lesson_id', '')
            selected_lesson = get_lesson(lesson_id)
            custom_question = request.form.get('custom_question', '').strip()
            if selected_lesson and custom_question:
                custom_answer = answer_personal_question(selected_lesson['title'], selected_lesson['text'], custom_question)
            elif not custom_question:
                flash('Scrie o Ã®ntrebare pentru lecÈ›ia selectatÄƒ.', 'error')

    lessons = load_lessons()
    lesson_id = request.args.get('lesson_id') or request.form.get('lesson_id')
    if not selected_lesson and lesson_id:
        selected_lesson = get_lesson(lesson_id)
    if selected_lesson:
        lesson_bundle = build_personal_lesson_bundle(selected_lesson['title'], selected_lesson['text'])

    return render_template(
        'custom_lesson.html',
        title='LecÈ›ie personalÄƒ Â· Bac Tutor',
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
                flash('CompleteazÄƒ titlul È™i conÈ›inutul notiÈ›ei.', 'error')
            else:
                append_note(title=title, text=note_text, subject_id=subject_id, subiect_id=subiect_id, chapter_id=chapter_id)
                flash('NotiÈ›a a fost adÄƒugatÄƒ Ã®n knowledge feed.', 'success')
                return redirect(url_for('admin_panel'))
        elif action == 'import_pdf':
            pdf_file = request.files.get('pdf_file')
            pdf_title = request.form.get('pdf_title', '').strip()
            if not pdf_title or not pdf_file or not pdf_file.filename:
                flash('Alege un PDF È™i completeazÄƒ un titlu.', 'error')
            else:
                try:
                    target = save_uploaded_pdf(pdf_file, prefix='knowledge')
                    created = import_pdf(target, title_prefix=pdf_title, subject_id=subject_id, subiect_id=subiect_id, chapter_id=chapter_id)
                    flash(f'PDF importat cu succes. Au fost create {len(created)} fragmente Ã®n knowledge feed.', 'success')
                    return redirect(url_for('admin_panel'))
                except ValueError as exc:
                    flash(str(exc), 'error')
                except Exception:
                    flash('PDF-ul nu a putut fi procesat. ÃŽncarcÄƒ un PDF valid, needitat.', 'error')
        elif action == 'rebuild_vectors':
            stats = rebuild_missing_embeddings()
            flash(f"Index semantic actualizat: {stats['created']} intrÄƒri noi, {stats['indexed']} indexate din {stats['entries']}.", 'info')
            return redirect(url_for('admin_panel'))

    return render_template(
        'admin.html',
        title='Materiale de studiu Â· Bac Tutor',
        recent_entries=list_recent_entries(12),
        knowledge_stats=vector_stats(),
        exam_item_count=exam_bank_count(),
        ollama_status=get_ollama_status(),
    )


if __name__ == '__main__':
    app.run(debug=debug_enabled(), port=5000)
