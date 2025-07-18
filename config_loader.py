"""
config_loader.py

Handles loading of persona configurations from JSON.
Includes logic for fallbacks and error handling.
"""

import json

def load_config(path="persona_config.json"):
    """
    Load the full config JSON from the specified path.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_persona(persona_name="default", config_path="persona_config.json"):
    """
    Loads the specified persona from the config file.
    Falls back to 'default' if not found.
    """
    config = load_config(config_path)

    if persona_name in config:
        return config[persona_name]
    else:
        print(f"[!] Persona '{persona_name}' not found. Falling back to 'default'.")
        return config["default"]
