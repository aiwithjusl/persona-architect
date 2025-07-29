"""
config_loader.py

Handles loading of persona configurations from JSON.
Includes logic for fallbacks and error handling.
"""

import json

def load_config(path="persona_config.json"):
    """
    Load the full persona configuration from a JSON file.

    Args:
        path (str): Path to the config file.

    Returns:
        dict: The full persona configuration.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_persona(persona_name="default", config_path="persona_config.json"):
    """
    Load a specific persona's traits and settings.

    Args:
        persona_name (str): The name of the persona to load.
        config_path (str): The path to the persona configuration file.

    Returns:
        dict: The loaded persona configuration.
    """
    config = load_config(config_path)
    normalized_config = {key.lower(): value for key, value in config.items()}
    requested_name = persona_name.lower()

    if requested_name in normalized_config:
        persona = normalized_config[requested_name].copy()
        persona["name"] = requested_name.title()
        return persona
    else:
        print(f"[!] Persona '{persona_name}' not found. Falling back to 'default'.")
        fallback = normalized_config.get("default", {}).copy()
        fallback["name"] = "Default"
        return fallback
