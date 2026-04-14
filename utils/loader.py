import json
import re

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    # Strip single-line comments (// ...)
    stripped = re.sub(r"//.*", "", raw)
    return json.loads(stripped)

def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()