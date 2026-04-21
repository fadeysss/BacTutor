from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from services.content_store import append_note


def main() -> None:
    parser = argparse.ArgumentParser(description='Adaugă o notiță în knowledge feed.')
    parser.add_argument('--title', required=True)
    parser.add_argument('--text', required=True)
    parser.add_argument('--subject', default='')
    parser.add_argument('--subiect', default='')
    parser.add_argument('--chapter', default='')
    args = parser.parse_args()

    entry = append_note(
        title=args.title,
        text=args.text,
        subject_id=args.subject,
        subiect_id=args.subiect,
        chapter_id=args.chapter,
        source_type='cli_note',
        source_name='script add_knowledge.py',
    )
    print(f"[OK] Added entry {entry['id']}")


if __name__ == '__main__':
    main()
