from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from services.content_store import rebuild_missing_embeddings, vector_stats


def main() -> None:
    before = vector_stats()
    stats = rebuild_missing_embeddings()
    after = vector_stats()
    print('[OK] Rebuild semantic index')
    print(f"Before: {before['indexed']} / {before['entries']} indexed")
    print(f"Created: {stats['created']}")
    print(f"After: {after['indexed']} / {after['entries']} indexed")
    print(f"Ollama healthy: {after['healthy']}")


if __name__ == '__main__':
    main()
