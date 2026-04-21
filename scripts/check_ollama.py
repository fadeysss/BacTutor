from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from services.llm_service import get_ollama_status


def main() -> None:
    status = get_ollama_status()
    print('[OK] Ollama status')
    print(f"Enabled: {status.get('enabled')}")
    print(f"Healthy: {status.get('healthy')}")
    print(f"Chat model: {status.get('chat_model')}")
    print(f"Embed model: {status.get('embed_model')}")
    models = status.get('available_models', [])
    if models:
        print('Available models:')
        for model in models:
            print(f' - {model}')


if __name__ == '__main__':
    main()
