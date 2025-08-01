import json
import os
from typing import Any

from jproperties import Properties

config = Properties()


def load_config() -> dict[str, str]:
    if os.path.exists('config.properties'):
        with open('config.properties', 'rb') as configFile:
            config.load(configFile)
    else:
        with open('config.properties', 'wb') as configFile:
            config.store(configFile, encoding="utf-8")

    config.setdefault("langPath", "lang")
    config.setdefault("lang", "eng.json")
    config.setdefault("felyneNumber", "1")
    config.setdefault("orderBy", "None")
    config.setdefault("showNoEffect", "True")
    config.setdefault("showNegativeBonuses", "True")

    return {
        "felyneNumber": int(config.get("felyneNumber").data),
        "orderBy": config.get("orderBy").data if config.get("orderBy").data != "None" else None,
        "showNoEffect": json.loads(config.get("showNoEffect").data.lower()),
        "showNegativeBonuses": json.loads(config.get("showNegativeBonuses").data.lower()),
    }


def load_data() -> dict[str, Any]:
    lang_file_path = os.path.join(config["langPath"].data, config["lang"].data)
    if os.path.exists(lang_file_path):
        with open(lang_file_path, 'r') as langFile:
            return json.load(langFile)
    else:
        raise FileNotFoundError(f"Could not find language file : {lang_file_path}")


def save_config(data: dict[str, Any]):
    config["felyneNumber"] = data["felyneNumber"]
    config["orderBy"] = data["orderBy"]
    config["showNoEffect"] = data["showNoEffect"]
    config["showNegativeBonuses"] = data["showNegativeBonuses"]

    with open('config.properties', 'wb') as configFile:
        config.store(configFile, encoding="utf-8")
