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
    Performs case-insensitive lookup.
    Falls back to 'default' if not found.
    """
    config = load_config(config_path)

    # Normalize keys for case-insensitive matching
    normalized_config = {key.lower(): value for key, value in config.items()}
    requested_name = persona_name.lower()

    if requested_name in normalized_config:
        persona = normalized_config[requested_name]
        persona["name"] = requested_name.title()  # Standardize display name
        return persona
    else:
        print(f"[!] Persona '{persona_name}' not found. Falling back to 'default'.")
        fallback = normalized_config.get("default", {})
        fallback["name"] = "Default"
        return fallback
