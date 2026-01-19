import json
import sys
from pathlib import Path


def get_config_path():
    """Calculates config.json path in the app"""
    if getattr(sys, 'frozen', False):
        base_dir = Path(sys.executable).parent
    else:
        base_dir = Path(__file__).parent.parent.parent

    return base_dir / "config.json"

def get_config_file():
    config_path = get_config_path()
    
    if not config_path.exists():
        raise FileNotFoundError(f"Couldn't find config.json in: {config_path}")
        
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_database_url():
    config = get_config_file()
    return config["database"]["url"]