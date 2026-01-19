import json

from src.utils.config import get_config_path
from src.utils.logger import business_logger


class SettingsManagement:
    def __init__(self):
        pass

    def update_db_url(self, db_url: str) -> None:

        config_json_path = get_config_path()

        with open(config_json_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        config["database"]["url"] = db_url

        with open(config_json_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

        business_logger.info(f"Database URL successfully updated in config.json to: {db_url}")