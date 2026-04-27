from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from time import monotonic
from typing import Any

from pathlib import Path

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover
    load_dotenv = None

if load_dotenv:
    load_dotenv(Path(__file__).resolve().parent.parent / '.env')

DEFAULT_HOST = 'http://127.0.0.1:11434'
OLLAMA_STATUS_TTL_SECONDS = 20.0
_OLLAMA_STATUS_CACHE: dict[str, Any] | None = None
_OLLAMA_STATUS_CACHE_AT = 0.0


def ollama_enabled() -> bool:
    return os.getenv('OLLAMA_ENABLED', '1') == '1'


def ollama_host() -> str:
    return os.getenv('OLLAMA_HOST', os.getenv('OLLAMA_BASE_URL', DEFAULT_HOST)).rstrip('/')


def ollama_chat_model() -> str:
    return os.getenv('OLLAMA_MODEL', os.getenv('OLLAMA_CHAT_MODEL', 'gemma3'))


def ollama_embed_model() -> str:
    return os.getenv('OLLAMA_EMBED_MODEL', 'embeddinggemma')


def _post(path: str, payload: dict[str, Any], timeout: int = 60) -> dict[str, Any] | None:
    if not ollama_enabled():
        return None
    request = urllib.request.Request(
        f"{ollama_host()}{path}",
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode('utf-8'))
    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError):
        return None


def _get(path: str, timeout: int = 6) -> dict[str, Any] | None:
    if not ollama_enabled():
        return None
    request = urllib.request.Request(
        f"{ollama_host()}{path}",
        headers={'Content-Type': 'application/json'},
        method='GET',
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode('utf-8'))
    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError):
        return None


def chat(messages: list[dict[str, str]], model: str | None = None, temperature: float = 0.2,
         keep_alive: str = '10m') -> str | None:
    payload = {
        'model': model or ollama_chat_model(),
        'messages': messages,
        'stream': False,
        'keep_alive': keep_alive,
        'options': {
            'temperature': temperature,
        },
    }
    data = _post('/api/chat', payload, timeout=90)
    if not data:
        return None
    message = data.get('message') or {}
    return (message.get('content') or '').strip() or None


def generate_with_ollama(system_prompt: str, user_prompt: str) -> str | None:
    messages = [
        {'role': 'system', 'content': system_prompt.strip()},
        {'role': 'user', 'content': user_prompt.strip()},
    ]
    return chat(messages)


def embed_texts(texts: list[str], model: str | None = None) -> list[list[float]] | None:
    cleaned = [text.strip() for text in texts if text and text.strip()]
    if not cleaned:
        return []
    payload = {
        'model': model or ollama_embed_model(),
        'input': cleaned,
        'keep_alive': '15m',
    }
    data = _post('/api/embed', payload, timeout=120)
    if not data:
        return None
    vectors = data.get('embeddings')
    if isinstance(vectors, list):
        return vectors
    return None


def embed_text(text: str, model: str | None = None) -> list[float] | None:
    vectors = embed_texts([text], model=model)
    if not vectors:
        return None
    return vectors[0]


def _fetch_ollama_status() -> dict[str, Any]:
    if not ollama_enabled():
        return {
            'enabled': False,
            'healthy': False,
            'chat_model': ollama_chat_model(),
            'embed_model': ollama_embed_model(),
            'available_models': [],
        }
    data = _get('/api/tags', timeout=6)
    if not data:
        return {
            'enabled': True,
            'healthy': False,
            'chat_model': ollama_chat_model(),
            'embed_model': ollama_embed_model(),
            'available_models': [],
        }
    models = []
    for item in data.get('models', []):
        name = item.get('model') or item.get('name')
        if name:
            models.append(name)
    return {
        'enabled': True,
        'healthy': True,
        'chat_model': ollama_chat_model(),
        'embed_model': ollama_embed_model(),
        'available_models': models,
    }


def refresh_ollama_status() -> None:
    global _OLLAMA_STATUS_CACHE, _OLLAMA_STATUS_CACHE_AT
    _OLLAMA_STATUS_CACHE = None
    _OLLAMA_STATUS_CACHE_AT = 0.0


def get_ollama_status() -> dict[str, Any]:
    global _OLLAMA_STATUS_CACHE, _OLLAMA_STATUS_CACHE_AT
    now = monotonic()
    if _OLLAMA_STATUS_CACHE and (now - _OLLAMA_STATUS_CACHE_AT) < OLLAMA_STATUS_TTL_SECONDS:
        return _OLLAMA_STATUS_CACHE
    _OLLAMA_STATUS_CACHE = _fetch_ollama_status()
    _OLLAMA_STATUS_CACHE_AT = now
    return _OLLAMA_STATUS_CACHE
