from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OLD_ID = "matematica_m2"
NEW_ID = "matematica_m1"
OLD_TITLE = "Matematică M2"
NEW_TITLE = "Matematică M1"


def migrate_catalog() -> None:
    path = DATA_DIR / "catalog.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for subject in payload.get("subjects", []):
        if subject.get("id") == OLD_ID:
            subject["id"] = NEW_ID
            subject["title"] = NEW_TITLE
            subject["short_title"] = NEW_TITLE
            subject["track"] = "profil real - matematică-informatică"
            subject["badge"] = "M1"
            subject["description"] = "Capitole grupate pedagogic pentru bac M1 (mate-info), cu accent pe metode, raționament, redactare clară și tipare de exerciții."
            for subiect in subject.get("subiecte", []):
                for chapter in subiect.get("chapters", []):
                    chapter["keywords"] = ["m1" if kw == "m2" else kw for kw in chapter.get("keywords", [])]
                    if "mate-info" not in chapter.get("keywords", []):
                        chapter.setdefault("keywords", []).insert(1, "mate-info")
            changed = True
    if changed:
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def migrate_feed() -> None:
    path = DATA_DIR / "knowledge_feed.jsonl"
    if not path.exists():
        return
    lines = []
    changed = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        entry = json.loads(raw)
        if entry.get("subject_id") == OLD_ID:
            entry["id"] = entry.get("id", "").replace("seed-matematica_m2-", "seed-matematica_m1-")
            entry["subject_id"] = NEW_ID
            entry["subject_title"] = NEW_TITLE
            entry["title"] = entry.get("title", "").replace(OLD_TITLE, NEW_TITLE)
            entry["text"] = re.sub(r"\bm2\b", "m1", entry.get("text", "").replace(OLD_TITLE, NEW_TITLE))
            entry["keywords"] = ["m1" if kw == "m2" else kw for kw in entry.get("keywords", [])]
            changed = True
        lines.append(json.dumps(entry, ensure_ascii=False))
    if changed:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def migrate_progress() -> None:
    path = DATA_DIR / "progress.json"
    if not path.exists():
        return
    payload = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for student in payload.get("students", {}).values():
        subjects = student.setdefault("subjects", {})
        if OLD_ID in subjects and NEW_ID not in subjects:
            subjects[NEW_ID] = subjects.pop(OLD_ID)
            changed = True
        elif OLD_ID in subjects and NEW_ID in subjects:
            old = subjects.pop(OLD_ID)
            new = subjects[NEW_ID]
            new["quizzes_taken"] = new.get("quizzes_taken", 0) + old.get("quizzes_taken", 0)
            if old.get("average_score") and not new.get("average_score"):
                new["average_score"] = old.get("average_score", 0.0)
            new.setdefault("chapters", {}).update(old.get("chapters", {}))
            changed = True
        student["chapters_viewed"] = [item.replace(f"{OLD_ID}:", f"{NEW_ID}:") for item in student.get("chapters_viewed", [])]
        for activity in student.get("recent_activity", []):
            if activity.get("subject_id") == OLD_ID:
                activity["subject_id"] = NEW_ID
                changed = True
    if changed:
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    migrate_catalog()
    migrate_feed()
    migrate_progress()
    print("[OK] Updated project data from matematica_m2 to matematica_m1")
