import json
import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from src.controllers.main_controller import MainController
from src.utils.config import get_config_path


def get_assets_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    db_url = ""
    app = QApplication(sys.argv)

    # =========================
    # SETUP assets and styles
    # =========================
    app.setWindowIcon(QIcon(get_assets_path("src/views/assets/app_icon.ico")))
    
    qss_path = get_assets_path("src/views/assets/styles.qss")
    with open(qss_path, "r") as f:
        app.setStyleSheet(f.read()) # Set ui assets

    # =========================
    # SETUP config.json
    # =========================
    config_json_path = get_config_path()
    if not os.path.exists(config_json_path):

        config = { "database": {"url": "" } }
        with open(config_json_path, 'w', encoding="utf-8") as file:
            json.dump(config, file, indent=4, ensure_ascii=False)
            print(f"db_url en el if: {db_url}")

    else:
        with open(config_json_path, 'r', encoding="utf-8") as file:
            config = json.load(file)
            db_url = config["database"]["url"]
            print(f"db_url en el else: {db_url}")

    # =========================
    # Start the app
    # ========================= 
    print(f"db_url antes de MainController: {db_url}")
    controller = MainController(db_url)
    controller.ui.show()
    sys.exit(app.exec())