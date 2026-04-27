from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from services.content_store import import_pdf


def main() -> None:
    parser = argparse.ArgumentParser(description='Importă un PDF în knowledge feed.')
    parser.add_argument('--file', required=True)
    parser.add_argument('--title', required=True)
    parser.add_argument('--subject', default='')
    parser.add_argument('--subiect', default='')
    parser.add_argument('--chapter', default='')
    args = parser.parse_args()

    created = import_pdf(
        pdf_path=args.file,
        title_prefix=args.title,
        subject_id=args.subject,
        subiect_id=args.subiect,
        chapter_id=args.chapter,
        source_name=Path(args.file).name,
    )
    print(f"[OK] Created {len(created)} feed entries")


if __name__ == '__main__':
    main()
