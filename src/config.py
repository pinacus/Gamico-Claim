import json
from pathlib import Path


CONFIG_FILE = Path("Config/config.json")
LEGACY_DISCORD_FILE = Path("Config/discord.json")
LEGACY_SESSION_FILE = Path("Config/session.json")


def load_config():
    config = {"Discord": {}, "Session": {}}

    if CONFIG_FILE.is_file():
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            saved_config = json.load(file)
        config["Discord"].update(saved_config.get("Discord", {}))
        config["Session"].update(saved_config.get("Session", {}))

    if not config["Discord"] and LEGACY_DISCORD_FILE.is_file():
        with open(LEGACY_DISCORD_FILE, "r", encoding="utf-8") as file:
            config["Discord"].update(json.load(file))

    if not config["Session"] and LEGACY_SESSION_FILE.is_file():
        with open(LEGACY_SESSION_FILE, "r", encoding="utf-8") as file:
            config["Session"].update(json.load(file))

    return config


def save_config(config):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=2, ensure_ascii=False)
