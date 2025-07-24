# memory.py

"""
Handles conversation history by storing user and persona messages.
Used to simulate memory during multi-turn dialogues and to support
session saving at the end of the interaction.
"""

class Memory:
    def __init__(self):
        self.history = []

    def add(self, speaker, message):
        """
        Add a message to memory as a dictionary:
        { "speaker": ..., "message": ... }
        """
        if not isinstance(speaker, str) or not isinstance(message, str):
            raise ValueError("Speaker and message must be strings.")
        self.history.append({"speaker": speaker, "message": message})

    def get_context(self):
        """
        Return the full conversation as a single string.
        """
        return "\n".join(f"{entry['speaker']}: {entry['message']}" for entry in self.history)

    def get_context_summary(self):
        """
        Return a short snippet of recent conversation (last 5 lines).
        """
        if not self.history:
            return ""
        summary = []
        for entry in self.history[-5:]:
            if isinstance(entry, dict) and "speaker" in entry and "message" in entry:
                summary.append(f"{entry['speaker']}: {entry['message']}")
        return "\n".join(summary)

    def clear(self):
        self.history = []
