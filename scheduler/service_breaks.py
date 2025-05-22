from typing import List, Dict
import json
from pathlib import Path

BREAKS_FILE = Path('service_breaks.json')


def load_breaks() -> List[Dict]:
    if BREAKS_FILE.exists():
        with open(BREAKS_FILE, 'r') as f:
            return json.load(f)
    return []


def add_break(entry: Dict):
    data = load_breaks()
    data.append(entry)
    with open(BREAKS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

