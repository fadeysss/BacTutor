from __future__ import annotations

import html
import re

_RE_U4 = re.compile(r'\\u([0-9a-fA-F]{4})')
_RE_U8 = re.compile(r'\\U([0-9a-fA-F]{8})')


def decode_unicode_escapes(text: str) -> str:
    if '\\u' not in text and '\\U' not in text:
        return text
    value = _RE_U4.sub(lambda match: chr(int(match.group(1), 16)), text)
    value = _RE_U8.sub(lambda match: chr(int(match.group(1), 16)), value)
    return value


def _normalize_symbols(text: str) -> str:
    value = text
    value = value.replace('<=>', '⇔')
    value = value.replace('<->', '↔')
    value = value.replace('->', '→')
    value = value.replace('<=', '≤')
    value = value.replace('>=', '≥')
    value = value.replace('!=', '≠')
    value = re.sub(r'\bsqrt\(([^()]+)\)', r'√(\1)', value, flags=re.IGNORECASE)
    return value


def format_math_text_html(text: str) -> str:
    value = decode_unicode_escapes(str(text or ''))
    value = _normalize_symbols(value)
    value = html.escape(value)

    value = re.sub(r'\^\{([^{}]+)\}', r'<sup>\1</sup>', value)
    value = re.sub(r'\^\(([^()]+)\)', r'<sup>\1</sup>', value)
    value = re.sub(r'\^(-?\d+|[A-Za-z]{1,2})\b', r'<sup>\1</sup>', value)

    value = re.sub(r'_\{([^{}]+)\}', r'<sub>\1</sub>', value)
    value = re.sub(r'_\(([^()]+)\)', r'<sub>\1</sub>', value)
    value = re.sub(r'_(\d+|[A-Za-z]{1,2})\b', r'<sub>\1</sub>', value)

    value = re.sub(r'(?<=\S)\s*\*\s*(?=\S)', ' · ', value)
    value = re.sub(r'\s{2,}', ' ', value).strip()
    return value


def format_math_list_html(values: list[str]) -> list[str]:
    return [format_math_text_html(value) for value in values]
