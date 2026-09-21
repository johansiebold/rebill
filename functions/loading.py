import json
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "config" / "paragraph_6_eeg.json"

def load_paragraph_6_eeg_infos() -> dict:
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)

def save_paragraph_6_eeg_infos(data: dict) -> None:
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
