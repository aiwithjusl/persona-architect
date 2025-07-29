"""
log_importer.py

Parses and validates a JSON log file containing a list of conversation entries.
Each entry must include a 'speaker' and a 'message'.
"""

import json

def parse_log_file(path):
    """
    Parse a conversation log file and validate its format.

    Args:
        path (str): Path to the log file.

    Returns:
        list: A list of validated conversation entries.

    Raises:
        Exception: If file is not found, invalid JSON, or improperly formatted.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("Log file must contain a list of entries.")

        validated = []
        for i, entry in enumerate(data):
            if not isinstance(entry, dict):
                raise ValueError(f"Entry {i+1} is not a dictionary.")
            if "speaker" not in entry or "message" not in entry:
                raise ValueError("Each log entry must contain 'speaker' and 'message'.")
            validated.append({
                "speaker": str(entry["speaker"]),
                "message": str(entry["message"])
            })

        return validated

    except FileNotFoundError as e:
        raise Exception(f"❌ File '{path}' not found.") from e

    except json.JSONDecodeError as e:
        raise Exception(f"❌ File '{path}' is not valid JSON.") from e

    except ValueError as ve:
        raise Exception(f"❌ Invalid log format: {ve}") from ve

    except Exception as e:
        raise Exception(f"❌ Unexpected error while importing log: {e}") from e
