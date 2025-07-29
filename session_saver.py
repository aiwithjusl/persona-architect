# session_saver.py

"""
Handles saving the full conversation history to a timestamped text file.
Each session is saved using the persona's name and current date/time.
"""

import datetime

def save_session(persona_name, memory):
    """
    Save the complete conversation history to a timestamped text file.

    Args:
        persona_name (str): Name of the current persona.
        memory (Memory): Memory object containing the conversation history.

    Creates:
        A .txt file with all dialogue from the session.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"session_{persona_name}_{timestamp}.txt"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(memory.get_context())
        print(f"\n✅ Session saved to '{filename}'")
    except Exception as e:
        print(f"\n❌ Failed to save session: {e}")
