from __future__ import annotations

import argparse
import uuid
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from services.exam_bank_service import add_exam_item


DEFAULT_LABEL = 'Item adăugat manual în banca de exerciții'


def main() -> None:
    parser = argparse.ArgumentParser(description='Adaugă un item de quiz aplicativ în banca de exerciții.')
    parser.add_argument('--subject', required=True)
    parser.add_argument('--subiect', required=True)
    parser.add_argument('--chapter', required=True)
    parser.add_argument('--year', type=int, required=True)
    parser.add_argument('--prompt', required=True)
    parser.add_argument('--option', action='append', dest='options', required=True,
                        help='Folosește de 4 ori argumentul --option pentru cele 4 variante de răspuns.')
    parser.add_argument('--correct-index', type=int, required=True)
    parser.add_argument('--difficulty', default='intermediate', choices=['beginner', 'intermediate', 'advanced'])
    parser.add_argument('--source-type', default='official_exam')
    parser.add_argument('--source-label', default=DEFAULT_LABEL)
    parser.add_argument('--explanation', required=True)
    parser.add_argument('--hint', default='')
    parser.add_argument('--worked-step', action='append', dest='worked_steps', default=[])
    parser.add_argument('--tag', action='append', dest='tags', default=[])
    args = parser.parse_args()

    if len(args.options) != 4:
        raise SystemExit('Trebuie să furnizezi exact 4 variante prin --option.')
    if args.correct_index < 0 or args.correct_index > 3:
        raise SystemExit('--correct-index trebuie să fie între 0 și 3.')

    item = {
        'id': f"manual-{uuid.uuid4().hex[:10]}",
        'subject_id': args.subject,
        'subiect_id': args.subiect,
        'chapter_id': args.chapter,
        'year': args.year,
        'source_type': args.source_type,
        'source_label': args.source_label,
        'difficulty': args.difficulty,
        'prompt': args.prompt,
        'options': args.options,
        'correct_index': args.correct_index,
        'explanation': args.explanation,
        'hint': args.hint,
        'worked_steps': args.worked_steps,
        'tags': args.tags,
    }
    created = add_exam_item(item)
    print(f"[OK] Added item {created['id']} for {created['chapter_id']}")


if __name__ == '__main__':
    main()
