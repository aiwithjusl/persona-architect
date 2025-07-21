# log_importer.py

import json

def parse_log_file(path):
    try:
        with open(path, "r") as f:
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

    except FileNotFoundError:
        raise Exception(f"File '{path}' not found.")

    except json.JSONDecodeError:
        raise Exception(f"File '{path}' is not valid JSON.")

    except ValueError as ve:
        raise Exception(f"Invalid log format: {ve}")

    except Exception as e:
        raise Exception(f"Unexpected error while importing: {e}")
