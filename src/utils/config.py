import json
from pathlib import Path

def get_config():
    config_path = Path(__file__).parent.parent.parent / "config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_database_url():
    config = get_config()
    return config["database"]["url"]
