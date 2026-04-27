from __future__ import annotations

import html
import re
from collections import Counter

from .chapter_examples_service import get_chapter_example
from .content_store import search_knowledge, tokenize
from .exam_bank_service import list_exam_items
from .formula_sheet_service import get_formula_sheet
from .llm_service import generate_with_ollama, get_ollama_status
from .math_text_service import format_math_list_html, format_math_text_html

PERSONA = {
    'uman': {
        'recipe_title': 'Cum înveți repede și bine la română',
        'steps': [
            'Pornește din teză sau idee centrală, nu din detalii izolate.',
            'Leagă fiecare afirmație de un exemplu concret din text sau din operă.',
            'Închide fiecare răspuns cu o propoziție care arată de ce contează ideea.',
        ],
    },
    'matematica': {
        'recipe_title': 'Rutina de rezolvare pentru mate',
        'steps': [
            'Scrie datele, condițiile și ce ți se cere înainte de calcule.',
            'Rezolvă pe pași scurți și verifică semnul, domeniul și unitățile de sens.',
            'Compară răspunsul final cu un control rapid: substituție, desen sau estimare.',
        ],
    },
    'informatica': {
        'recipe_title': 'Rutina de rezolvare pentru info',
        'steps': [
            'Clarifică inputul, outputul și restricțiile din enunț.',
            'Alege structura de date minimă și descrie algoritmul înainte de cod.',
            'Testează pe caz mic, caz-limită și un exemplu reprezentativ.',
        ],
    },
}

FOCUS_MODE = {
    'Începător': {
        'label': 'Focus Sprint · pas cu pas',
        'description': 'Ai explicații scurte, exemplu rezolvat și un set final de grile M1, ordonat de la bază la tricky.',
        'ai_prompt': 'explică foarte clar, cu cuvinte simple și fără a sări pași',
    },
    'Intermediar': {
        'label': 'Focus Sprint · examen ghidat',
        'description': 'Pui accent pe capcane, pe justificarea pașilor și pe un set de antrenament M1 apropiat de ritmul de examen.',
        'ai_prompt': 'explică clar, dar păstrează ritm de examen și insistă pe strategie',
    },
    'Avansat': {
        'label': 'Focus Sprint · exam mode',
        'description': 'Primești rezumat dens, strategie și un set M1 cu itemi mai agresivi pe capcanele clasice de bac.',
        'ai_prompt': 'explică sintetic, orientat pe strategie și capcane subtile',
    },
}

DRILL_DIFFICULTY_LABELS = {
    'beginner': 'baza',
    'intermediate': 'standard',
    'advanced': 'tricky',
}


def _decode_unicode_escapes(text: str) -> str:
    if '\\u' not in text and '\\U' not in text:
        return text

    def repl_u(match: re.Match[str]) -> str:
        return chr(int(match.group(1), 16))

    def repl_U(match: re.Match[str]) -> str:
        return chr(int(match.group(1), 16))

    # Decode only valid escaped unicode sequences and keep the rest untouched.
    value = re.sub(r'\\u([0-9a-fA-F]{4})', repl_u, text)
    value = re.sub(r'\\U([0-9a-fA-F]{8})', repl_U, value)
    return value


def _format_formula_html(formula: str) -> str:
    # Decode escaped unicode sequences from JSON and render power/subscript nicely.
    value = _decode_unicode_escapes(formula)
    value = html.escape(value)
    value = re.sub(r'\^\{([^}]+)\}', r'<sup>\1</sup>', value)
    value = re.sub(r'\^\(([^)]+)\)', r'<sup>\1</sup>', value)
    value = re.sub(r'\^([A-Za-z0-9+\-]+)', r'<sup>\1</sup>', value)
    value = re.sub(r'_\{([^}]+)\}', r'<sub>\1</sub>', value)
    value = re.sub(r'_\(([^)]+)\)', r'<sub>\1</sub>', value)
    value = re.sub(r'_([A-Za-z0-9+\-]+)', r'<sub>\1</sub>', value)
    value = value.replace('*', ' · ')
    value = re.sub(r'\s{2,}', ' ', value).strip()
    return value


def _generic_example(chapter: dict) -> dict:
    return {
        'micro_recap': chapter.get('summary', ''),
        'attention_hook': chapter.get('coach_tip', ''),
        'concrete_example': {
            'title': f'Exemplu aplicat · {chapter.get("title", "Capitol")}',
            'statement': chapter.get('practice_prompt', ''),
            'steps': chapter.get('starter_tasks', [])[:3] or [chapter.get('objective', '')],
        },
        'quick_checks': [
            f"Poți reformula pe scurt ce urmărește capitolul «{chapter.get('title', '')}»?",
            'Știi care este capcana principală înainte să intri în quiz?',
        ],
        'memory_hook': chapter.get('common_mistake', ''),
        'sprint_plan': ['recitești ideea de bază', 'parcurgi exemplul', 'treci la quiz'],
    }


def _build_revision_cards(chapter: dict, chapter_example: dict) -> list[dict]:
    keywords = chapter.get('keywords', [])[:4]
    cards = [
        {
            'label': '1 minut',
            'text': chapter_example.get('micro_recap') or chapter.get('summary', ''),
        },
        {
            'label': 'Capcană',
            'text': chapter.get('common_mistake', ''),
        },
        {
            'label': 'Reține',
            'text': chapter_example.get('memory_hook') or chapter.get('coach_tip', ''),
        },
    ]
    if keywords:
        cards.append({
            'label': 'Cuvinte-cheie',
            'text': ', '.join(keywords),
        })
    return cards


def _build_formula_drills(subject: dict, subiect: dict, chapter: dict, limit: int = 4) -> list[dict]:
    items = list_exam_items(subject.get('id', ''), subiect.get('id', ''), chapter.get('id', ''))
    if not items:
        return []
    ranked = sorted(
        items,
        key=lambda item: (
            int(item.get('year', 0) or 0),
            {'beginner': 0, 'intermediate': 1, 'advanced': 2}.get(item.get('difficulty', 'intermediate'), 1),
            item.get('prompt', ''),
        ),
        reverse=True,
    )
    drills = []
    for item in ranked:
        drills.append({
            'prompt': format_math_text_html(item.get('prompt', '')),
            'hint': format_math_text_html(item.get('hint', '')),
            'source_label': item.get('source_label', ''),
            'source_year': item.get('year'),
            'difficulty_label': DRILL_DIFFICULTY_LABELS.get(item.get('difficulty', 'intermediate'), 'standard'),
        })
        if len(drills) >= limit:
            break
    return drills


def build_lesson_bundle(subject: dict, subiect: dict, chapter: dict, student_level: str,
                        chapter_stats: dict | None = None) -> dict:
    discipline = subject.get('discipline_type', 'uman')
    study_recipe = PERSONA.get(discipline, PERSONA['uman'])
    focus_mode = FOCUS_MODE.get(student_level, FOCUS_MODE['Începător'])
    query = ' '.join([chapter['title'], chapter['summary'], ' '.join(chapter.get('keywords', []))])
    knowledge_cards = search_knowledge(
        query,
        subject_id=subject.get('id', ''),
        subiect_id=subiect.get('id', ''),
        chapter_id=chapter.get('id', ''),
        limit=5,
    )
    chapter_example = get_chapter_example(subject.get('id', ''), subiect.get('id', ''), chapter.get('id', '')) or _generic_example(chapter)
    formula_sheet = get_formula_sheet(subject.get('id', ''), subiect.get('id', ''), chapter.get('id', ''))
    if formula_sheet:
        formula_sheet = dict(formula_sheet)
        formula_sheet['formulas'] = format_math_list_html(formula_sheet.get('formulas', []))
        formula_sheet['tips'] = format_math_list_html(formula_sheet.get('tips', []))
    formula_drills = _build_formula_drills(subject, subiect, chapter, limit=4)
    explanation_sections = [
        {'title': 'Recapitulare de 60 de secunde', 'text': chapter_example.get('micro_recap') or chapter['summary']},
        {'title': 'Ce trebuie să stăpânești', 'text': chapter['objective']},
        {'title': 'Unde se pierde punctaj', 'text': chapter['common_mistake']},
        {'title': 'Cum aplici imediat', 'text': chapter['practice_prompt']},
        {'title': 'Sfat rapid de tutor', 'text': chapter['coach_tip']},
    ]
    return {
        'subject': subject,
        'subiect': subiect,
        'chapter': chapter,
        'student_level': student_level,
        'chapter_stats': chapter_stats or {},
        'focus_mode': focus_mode,
        'study_recipe_title': study_recipe['recipe_title'],
        'study_steps': study_recipe['steps'],
        'knowledge_cards': knowledge_cards,
        'explanation_sections': explanation_sections,
        'starter_tasks': chapter.get('starter_tasks', []),
        'attention_hook': chapter_example.get('attention_hook', ''),
        'concrete_example': chapter_example.get('concrete_example', {}),
        'quick_checks': chapter_example.get('quick_checks', []),
        'memory_hook': chapter_example.get('memory_hook', ''),
        'sprint_plan': chapter_example.get('sprint_plan', []),
        'revision_cards': _build_revision_cards(chapter, chapter_example),
        'formula_sheet': formula_sheet,
        'formula_drills': formula_drills,
        'ollama_status': get_ollama_status(),
    }


def answer_question(subject: dict, subiect: dict, chapter: dict, question: str, student_level: str) -> str:
    snippets = search_knowledge(
        f"{chapter['title']} {question}",
        subject_id=subject.get('id', ''),
        subiect_id=subiect.get('id', ''),
        chapter_id=chapter.get('id', ''),
        limit=4,
    )
    chapter_example = get_chapter_example(subject.get('id', ''), subiect.get('id', ''), chapter.get('id', '')) or _generic_example(chapter)
    focus_prompt = FOCUS_MODE.get(student_level, FOCUS_MODE['Începător'])['ai_prompt']

    system_prompt = (
        'Ești Bac Tutor, un profesor răbdător pentru bacalaureat în România. '
        'Răspunde doar în limba română. '
        'Structură obligatorie: 1) Idee pe scurt, 2) Explicație clară, 3) Exemplu concret, 4) Ce să reții pentru bac. '
        'Fără divagații, fără bibliografie inventată, fără expresii pompoase. '
        f'Ton: {focus_prompt}. '
        'Ține cont de faptul că elevul are atenție scurtă: fraze scurte, pași clari, exemple utile.'
    )
    context_parts = [
        f"Materie: {subject.get('title')}",
        f"Subiect: {subiect.get('title')}",
        f"Capitol: {chapter.get('title')}",
        f"Rezumat: {chapter.get('summary')}",
        f"Obiectiv: {chapter.get('objective')}",
        f"Capcană: {chapter.get('common_mistake')}",
        f"Exemplu aplicat: {chapter_example.get('concrete_example', {}).get('statement', '')}",
        f"Pași de exemplu: {' | '.join(chapter_example.get('concrete_example', {}).get('steps', []))}",
    ]
    if snippets:
        context_parts.append('Fragmente utile din materialele încărcate:')
        for item in snippets:
            context_parts.append(f"- {item.get('title', 'Fragment')}: {item.get('snippet', '')}")
    user_prompt = (
        f"Nivel elev: {student_level}\n"
        f"Întrebare: {question}\n\n"
        f"Context:\n{'\n'.join(context_parts)}\n\n"
        'Răspunde în maximum 260 de cuvinte. Include un exemplu nou sau reformulează exemplul primit dacă este suficient.'
    )
    llm_answer = generate_with_ollama(system_prompt, user_prompt)
    if llm_answer:
        return llm_answer

    fallback_parts = [
        f"Idee pe scurt: pentru «{chapter['title']}», ținta este să {chapter['objective']}.",
        f"Explicație: ai grijă în special la {chapter['common_mistake']}.",
    ]
    example = chapter_example.get('concrete_example', {})
    if example:
        fallback_parts.append(f"Exemplu: {example.get('statement', '')}")
        steps = example.get('steps', [])[:3]
        if steps:
            fallback_parts.append('Pași: ' + ' '.join(steps))
    if snippets:
        fallback_parts.append(f"Din materialele tale: {snippets[0].get('snippet', '')}")
    fallback_parts.append(f"Ce să reții: {chapter_example.get('memory_hook') or chapter.get('coach_tip')}")
    return '\n\n'.join(part for part in fallback_parts if part)


def _extract_keywords(text: str, limit: int = 8) -> list[str]:
    tokens = tokenize(text)
    freq = Counter(tokens)
    return [word for word, _ in freq.most_common(limit)]


def build_personal_lesson_bundle(title: str, text: str) -> dict:
    paragraphs = [part.strip() for part in re.split(r'\n{2,}|(?<=[.!?])\s+', text) if part.strip()]
    summary = paragraphs[:3]
    keywords = _extract_keywords(text)
    tasks = [
        f"Explică în 5-7 rânduri ce ai înțeles din lecția «{title}» folosind 3 dintre cuvintele: {', '.join(keywords[:5])}.",
        'Construiește o fișă flash: idee-cheie, exemplu, greșeală de evitat.',
        'Transformă lecția într-un mini-plan de recapitulare: 1 minut, 3 minute, 10 minute.',
    ]
    return {
        'title': title,
        'summary': summary,
        'keywords': keywords,
        'tasks': tasks,
        'micro_recap': summary[0] if summary else '',
    }


def answer_personal_question(title: str, text: str, question: str) -> str:
    system_prompt = (
        'Ești Bac Tutor. Răspunde doar pe baza lecției personale furnizate. '
        'Structură: 1) idee pe scurt, 2) explicație clară, 3) ce să reții. '
        'Maximum 220 de cuvinte.'
    )
    context = text[:7000]
    user_prompt = (
        f"Lecție: {title}\nÎntrebare: {question}\n\n"
        f"Textul lecției:\n{context}\n\n"
        'Răspunde simplu, clar și practic.'
    )
    llm_answer = generate_with_ollama(system_prompt, user_prompt)
    if llm_answer:
        return llm_answer

    sentences = re.split(r'(?<=[.!?])\s+', text)
    scored = []
    q_tokens = set(tokenize(question))
    for sentence in sentences:
        sentence_tokens = set(tokenize(sentence))
        score = len(q_tokens & sentence_tokens)
        if score:
            scored.append((score, sentence.strip()))
    scored.sort(reverse=True)
    best = [item[1] for item in scored[:3]]
    if not best:
        best = [text[:220] + ('…' if len(text) > 220 else '')]
    return (
        f"Idee pe scurt: {' '.join(best[:1])}\n\n"
        f"Explicație: {' '.join(best)}\n\n"
        'Ce să reții: reformulează răspunsul cu cuvintele tale și încearcă să dai un exemplu propriu.'
    )
