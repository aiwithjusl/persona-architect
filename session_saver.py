"""
session_saver.py

Handles saving the full conversation history to a timestamped text file.
Each session is logged using the persona's name and current date/time.
"""

import datetime

def save_session(persona_name, memory):
    """
    Saves the complete conversation to a local file.
    
    Args:
        persona_name (str): Name of the active persona
        memory (Memory): Memory object containing the full dialogue
    
    Creates:
        A .txt file with all dialogue history from the session
    """

    # Generate a timestamped filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"session_{persona_name}_{timestamp}.txt"

    # Write the memory history to the file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(memory.get_context())

    # Confirm that the session was saved
    print(f"\n[✔] Session saved to {filename}")
